import os
import re

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"filename": filename, "text": text})
    print(f"Loaded {len(docs)} documents")
    return docs

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'Helpful\s*👍\s*\d+\s*👎\s*\d+', '', text)
    text = re.sub(r'\b(Advertisement|Share|Report|Helpful)\b', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks

def ingest():
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["filename"],
                "chunk_index": i
            })
    print(f"Total chunks: {len(all_chunks)}")
    print("\n--- 5 SAMPLE CHUNKS ---")
    for i, chunk in enumerate(all_chunks[:5]):
        print(f"\nChunk {i+1} (from {chunk['source']}):")
        print(chunk["text"])
    return all_chunks

if __name__ == "__main__":
    ingest()