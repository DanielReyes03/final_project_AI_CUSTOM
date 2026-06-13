def apply_context(user_id, question, base_answer, context_items):
    if not context_items:
        return {"answer": base_answer, "context_used": []}

    context_lines = "\n".join(
        f"- {item['key']}: {item['value']}" for item in context_items
    )
    keys_used = [item["key"] for item in context_items]

    enriched_answer = (
        f"{base_answer}\n\n"
        f"Adaptado segun tu contexto:\n{context_lines}"
    )

    return {"answer": enriched_answer, "context_used": keys_used}
