from django.urls import path
from .views import home, ask_question, upload_document

urlpatterns = [
    path("", home, name="home"),
    path("upload/", upload_document, name="upload_document"),
    path("ask/", ask_question, name="ask_question"),
]
