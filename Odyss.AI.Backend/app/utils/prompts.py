from typing import List

from app.models.user import TextChunk

def summary_prompt_builder(chunks: List[TextChunk]):

    context = "".join(f"{t.text}" for i, t in enumerate(chunks))

    return [
        {
            "role": "system",
            "content": f"""
                You are a teacher tasked with summarizing an essay. After reading the essay, give a short summary about the content in the essay.

                # Essay:
                {context}

                # Instructions:
                ## Summarize:
                In clear and concise language, summarize the key points and themes presented in the essay.
                """,
        },
    ]

def qna_prompt_builder(chunks: List[TextChunk], question: str):

    context = "\n".join(f"{i+1}. Part: {t.text}" for i, t in enumerate(chunks))

    return [
            {
                "role": "system",
                "content": f"""
                    You are a teacher. Your task is to read and understand the following text.
                    After reading the text, answer the questions that follow.

                    # Text:
                    {context}

                    # Instructions:
                    ## Answer the following question:
                    {question}
                    """,
            }
    ]