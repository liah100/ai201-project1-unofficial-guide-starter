import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest

def build_vector_store():
    print("Loading chunks...")
    chunks = ingest()

    print("\nLoading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        client.delete_collection("rit_professors")
    except:
        pass
    
    collection = client.create_collection("rit_professors")

    print("Embedding and storing chunks...")
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )

    print(f"\nStored {len(chunks)} chunks in ChromaDB")
    return collection, model

def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    collection, model = build_vector_store()
    
    print("\n--- RETRIEVAL TEST ---")
    test_queries = [
        "What do students say about Professor Agyingi's teaching style?",
        "Is Professor Timberlake difficult?",
        "Which professor is the most lenient grader?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retrieve(query, collection, model)
        for r in results[:2]:
            print(f"  [{r['distance']:.3f}] ({r['source']}) {r['text'][:150]}")