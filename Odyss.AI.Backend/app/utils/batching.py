from typing import List
from app.utils.prompts import summary_prompt_builder
from app.utils.ml_connection import query_mixtral_with_ssh_async
from app.models.user import TextChunk
import unicodedata
import re

# Funktion zur Bereinigung und Normalisierung des Textes
def clean_and_normalize_text(text: str) -> str:
    # Unicode-Normalisierung (NFKC für Kompatibilitätszeichen)
    text = unicodedata.normalize("NFKC", text)
    
    # Entferne überflüssige Leerzeichen und Zeilenumbrüche
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Optional: in Kleinbuchstaben konvertieren (entfernen, falls nicht gewünscht)
    text = text.lower()
    
    # Entferne unerwünschte Sonderzeichen
    text = re.sub(r'[{}[\]<>()]', '', text)
    
    return text

# Funktion zur Bereinigung der TextChunks
def preprocess_text_chunks(chunks: List[TextChunk]) -> List[TextChunk]:
    for chunk in chunks:
        chunk.text = clean_and_normalize_text(chunk.text)
    return chunks

# Zählt die Wörter in einem Text
def count_words(text: str) -> int:
    return len(text.split())

# Batching-Funktion mit maximal 1000 Wörtern pro Batch
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

# Hauptfunktion, die Batches verarbeitet und eine finale Zusammenfassung erstellt
async def create_summary_with_batches(chunks: List[TextChunk], max_words: int = 1000, token_limit: int = 8192):
    # Bereinige und normalisiere die TextChunks
    chunks = preprocess_text_chunks(chunks)
    
    # Teile die bereinigten TextChunks in Batches von maximal 1000 Wörtern
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