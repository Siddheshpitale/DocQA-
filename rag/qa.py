import os
from groq import Groq

# Get API key from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, retrieved_chunks):
    """
    Generate answer using Groq API with improved prompting and formatting
    
    Args:
        query: User's question
        retrieved_chunks: List of retrieved document chunks with metadata
    
    Returns:
        Dictionary with 'answer' and 'sources'
    """
    if not retrieved_chunks:
        return {
            "answer": "The requested information was not found in the provided documents.",
            "sources": []
        }
    
    # Build context with source information
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks):
        doc_name = chunk["metadata"]["document"]
        page_num = chunk["metadata"]["page"]
        chunk_id = chunk["metadata"]["chunk_id"]
        text = chunk["text"]
        
        context_parts.append(
            f"[Source {i+1}: {doc_name}, Page {page_num}, Chunk {chunk_id}]\n{text}\n"
        )
    
    context = "\n".join(context_parts)
    
    # Ultra-strict prompt emphasizing line breaks
    prompt = f"""You are a document question-answering assistant. Answer questions using ONLY the information provided in the context below.

ABSOLUTELY CRITICAL FORMATTING RULES - MUST FOLLOW:

1. EACH bullet point MUST be on a SEPARATE line
2. NEVER EVER put two bullets on the same line
3. Put a blank line after each section heading
4. Use bullet character: •
5. Use **text** for bold headings

CORRECT FORMAT (FOLLOW THIS EXACTLY):

**Section Title**

• First point here
• Second point here  
• Third point here

**Next Section**

• Another point here
• One more point here

WRONG FORMAT (NEVER DO THIS):
**Section** • Point 1 • Point 2 • Point 3

CONTENT RULES:
1. Use ONLY information from the context provided
2. Be comprehensive and include all relevant information
3. Organize information into clear sections with **bold** headings
4. Each bullet point should be complete and informative

CONTEXT:
{context}

QUESTION: {query}

ANSWER (remember: SEPARATE LINE for EACH bullet point):"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant. CRITICAL RULE: Each bullet point MUST be on its own separate line.

CORRECT format:
**Title**

• Point one
• Point two
• Point three

WRONG format:
**Title** • Point one • Point two

You MUST put each bullet on a new line. This is absolutely required."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # Lower temperature for consistent formatting
            max_tokens=1500,
            top_p=0.9
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Format and convert to HTML
        formatted_answer = format_with_html(answer)
        
    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "sources": []
        }
    
    # Extract unique sources
    sources = []
    seen = set()
    for chunk in retrieved_chunks:
        key = (chunk["metadata"]["document"], chunk["metadata"]["page"], chunk["metadata"]["chunk_id"])
        if key not in seen:
            seen.add(key)
            sources.append({
                "document": chunk["metadata"]["document"],
                "page": chunk["metadata"]["page"],
                "chunk_id": chunk["metadata"]["chunk_id"]
            })
    
    return {
        "answer": formatted_answer,
        "sources": sources
    }


def format_with_html(raw_answer):
    """
    Format answer with proper line breaks and convert markdown to HTML
    
    Args:
        raw_answer: Raw answer text from LLM
    
    Returns:
        HTML-formatted answer
    """
    if not raw_answer:
        return "No answer generated."
    
    # First pass: convert numbered lists to bullets
    lines = raw_answer.strip().split('\n')
    converted_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Convert numbered lists to bullets
        if stripped and len(stripped) > 2 and stripped[0].isdigit():
            if '. ' in stripped[:4] or ') ' in stripped[:4]:
                for i, char in enumerate(stripped):
                    if char in ['.', ')'] and i < len(stripped) - 1 and stripped[i + 1] == ' ':
                        content = stripped[i + 2:].strip()
                        indent = len(line) - len(line.lstrip())
                        converted_lines.append(' ' * indent + '• ' + content)
                        break
                else:
                    converted_lines.append(line)
            else:
                converted_lines.append(line)
        else:
            converted_lines.append(line)
    
    # Second pass: FORCE split any line with multiple bullets
    final_lines = []
    
    for line in converted_lines:
        # Check if line contains bullet character
        if '•' in line:
            # Count how many bullets
            bullet_count = line.count('•')
            
            if bullet_count > 1:
                # Multiple bullets on same line - FORCE SPLIT
                parts = line.split('•')
                base_indent = len(parts[0]) - len(parts[0].lstrip()) if parts[0].strip() else 0
                
                for i, part in enumerate(parts):
                    cleaned = part.strip()
                    if cleaned:
                        if i == 0:
                            # First part might be a heading or text before bullets
                            if cleaned.startswith('**') or cleaned.startswith('#'):
                                final_lines.append(cleaned)
                                final_lines.append('')
                            else:
                                if cleaned:
                                    final_lines.append(cleaned)
                        else:
                            # Add each bullet on its own line
                            final_lines.append(' ' * base_indent + '• ' + cleaned)
            else:
                # Single bullet - keep as is
                final_lines.append(line)
        else:
            # No bullets - keep as is
            final_lines.append(line)
    
    # Third pass: ensure proper spacing around headings
    spaced_lines = []
    for i, line in enumerate(final_lines):
        stripped = line.strip()
        
        # Check if it's a heading
        is_heading = (stripped.startswith('**') and stripped.endswith('**') and len(stripped) > 4) or stripped.startswith('#')
        
        # Add blank line before heading (except first line)
        if is_heading and spaced_lines and spaced_lines[-1].strip():
            spaced_lines.append('')
        
        spaced_lines.append(line)
        
        # Add blank line after heading
        if is_heading and i + 1 < len(final_lines):
            next_line = final_lines[i + 1].strip()
            if next_line:
                spaced_lines.append('')
    
    # Fourth pass: Convert markdown to HTML
    html_lines = []
    
    for line in spaced_lines:
        # Convert **bold** to <strong>bold</strong>
        while '**' in line:
            # Find first **
            start = line.find('**')
            if start != -1:
                # Find closing **
                end = line.find('**', start + 2)
                if end != -1:
                    # Extract the text between ** **
                    bold_text = line[start + 2:end]
                    # Replace with <strong> tags
                    line = line[:start] + f'<strong>{bold_text}</strong>' + line[end + 2:]
                else:
                    # No closing **, break
                    break
            else:
                break
        
        # Convert ### to <h3>, ## to <h2>, # to <h1>
        if line.strip().startswith('###'):
            text = line.strip()[3:].strip()
            line = f'<h3>{text}</h3>'
        elif line.strip().startswith('##'):
            text = line.strip()[2:].strip()
            line = f'<h2>{text}</h2>'
        elif line.strip().startswith('#'):
            text = line.strip()[1:].strip()
            line = f'<h1>{text}</h1>'
        
        html_lines.append(line)
    
    # Fifth pass: clean up excessive blank lines
    cleaned_lines = []
    blank_count = 0
    
    for line in html_lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 1:
                cleaned_lines.append(line)
        else:
            blank_count = 0
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)