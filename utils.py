def generate_context(results):
    context = ""
    for result in results:
        context += f"Title: {result.get('title', '')}\n"
        context += f"Summary: {result.get('body', '')}\n\n"
    return context.strip()
