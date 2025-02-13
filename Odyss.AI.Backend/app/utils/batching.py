from typing import List
from app.utils.prompts import summary_prompt_builder
from app.utils.ml_connection import query_mixtral_with_ssh_async
from app.models.user import TextChunk
import unicodedata
import re

def clean_and_normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    text = re.sub(r'[{}[\]<>()]', '', text)
    
    return text

def preprocess_text_chunks(chunks: List[TextChunk]) -> List[TextChunk]:
    for chunk in chunks:
        chunk.text = clean_and_normalize_text(chunk.text)
    return chunks

def count_words(text: str) -> int:
    return len(text.split())

def batch_text_chunks(chunks: List[TextChunk], max_words: int):
    batches = []
    current_batch = []
    current_word_count = 0
    
    for chunk in chunks:
        chunk_text = chunk.text
        chunk_word_count = count_words(chunk_text)
        
        if current_word_count + chunk_word_count > max_words:
            batches.append(current_batch)
            current_batch = []
            current_word_count = 0
        
        current_batch.append(chunk)
        current_word_count += chunk_word_count
    
    if current_batch:
        batches.append(current_batch)
    
    return batches


async def create_summary_with_batches(chunks: List[TextChunk], max_words: int = 1000, token_limit: int = 8192):
    try:
        chunks = preprocess_text_chunks(chunks)
        
        batches = batch_text_chunks(chunks, max_words)
        batch_summaries = []
        
        for batch in batches:
            prompt = summary_prompt_builder(batch)
            summary = await query_mixtral_with_ssh_async(prompt)
            batch_summaries.append(summary)
        
        final_text = " ".join(batch_summaries)
        
        if count_words(final_text) > token_limit:
            words = final_text.split()
            final_text = " ".join(words[:token_limit / 1.4])
        
        final_prompt = summary_prompt_builder([TextChunk(id="final_summary", text=final_text, page=0)])
        final_summary = await query_mixtral_with_ssh_async(final_prompt)
        
        return final_summary
    except Exception as e:
        print(f"Error while creating summary: {str(e)}")
        return None