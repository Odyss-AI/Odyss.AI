from typing import List

from app.models.user import TextChunk

def summary_prompt_builder(chunks: List[TextChunk]):

    context = "".join(f"{t.text}" for i, t in enumerate(chunks))

    return [
        {
            "role": "system",
            "content": f"""
                You are a teacher tasked with summarizing an text. After reading the text, give a short summary in one or two sentences about the content in the essay.

                # Text:
                {context}

                # Instructions:
                ## Summarize:
                In clear and concise language, summarize the key points and themes presented in the essay.
                """,
        },
    ]

def qna_prompt_builder(chunks: list, question: str):

    context = ""
    if chunks:
        for chunk, i in chunks:
            context += chunk + "\n"
            
    return [
            {
                "role": "system",
                "content": f"""
                    You are a teacher. Your task is to read and understand the following text.
                    After reading the text, answer the questions that follow. If no text is provided, please answer the question to the best of your ability.

                    # Text:
                    {context}

                    # Instructions:
                    ## In clear and concise language, answer the following question in 3-8 sentences:
                    {question}
                    """,
            }
    ]