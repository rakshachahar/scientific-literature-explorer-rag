def build_context(docs, max_chars=4000):
    """
    Combine retrieved chunks into a single context string.
    Hard limit to avoid huge prompts.
    """
    context = ""
    for doc in docs:
        if len(context) + len(doc.page_content) > max_chars:
            break
        context += doc.page_content.strip() + "\n\n"
    return context.strip()
