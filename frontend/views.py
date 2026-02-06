import os
import tempfile
import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rag.pipeline import RAGPipeline

_active_pipelines = {}
COOKIE_NAME = "docqa_client_id"


def _get_client_id(request, response=None):
    client_id = request.COOKIES.get(COOKIE_NAME)
    if not client_id:
        client_id = str(uuid.uuid4())
        if response:
            response.set_cookie(COOKIE_NAME, client_id, max_age=60 * 60 * 24)
    return client_id


def home(request):
    return render(request, "index.html")


@csrf_exempt
def upload_document(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    if not file.name.lower().endswith(".pdf"):
        return JsonResponse({"error": "Only PDF files are supported"}, status=400)

    client_id = request.COOKIES.get(COOKIE_NAME)
    if not client_id:
        client_id = str(uuid.uuid4())

    upload_dir = os.path.join(tempfile.gettempdir(), "docqa_uploads", client_id)
    os.makedirs(upload_dir, exist_ok=True)

    for f in os.listdir(upload_dir):
        os.remove(os.path.join(upload_dir, f))

    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, "wb") as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    try:
        pipeline = RAGPipeline(docs_path=upload_dir)
        _active_pipelines[client_id] = pipeline
    except Exception as e:
        return JsonResponse({"error": f"Failed to process document: {str(e)}"}, status=500)

    response = JsonResponse({
        "status": "success",
        "message": f"Document '{file.name}' uploaded and indexed successfully.",
        "filename": file.name
    })
    response.set_cookie(COOKIE_NAME, client_id, max_age=60 * 60 * 24)
    return response


@csrf_exempt
def ask_question(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    query = request.POST.get("query")
    if not query:
        return JsonResponse({"error": "Query parameter is missing"}, status=400)

    client_id = request.COOKIES.get(COOKIE_NAME)
    pipeline = _active_pipelines.get(client_id) if client_id else None

    if not pipeline:
        return JsonResponse({
            "answer": "No document loaded. Please upload a PDF document first.",
            "sources": []
        })

    try:
        response = pipeline.ask(query)
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error processing query: {str(e)}"}, status=500)
