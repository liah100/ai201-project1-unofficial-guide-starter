import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq
from embed import build_vector_store, retrieve

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Building vector store...")
collection, model = build_vector_store()
print("Ready!")

def ask(question):
    chunks = retrieve(question, collection, model, k=5)
    
    context = ""
    sources = []
    for chunk in chunks:
        context += f"\n---\n{chunk['text']}"
        if chunk['source'] not in sources:
            sources.append(chunk['source'])
    
    prompt = f"""You are a helpful assistant for RIT students looking for information about math professors.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Do not use any outside knowledge.

Documents:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    source_list = "\n".join(f"• {s}" for s in sources)
    
    return answer, source_list

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    answer, sources = ask(question)
    return answer, sources

with gr.Blocks(title="RIT Math Professor Unofficial Guide") as demo:
    gr.Markdown("# 🎓 RIT Math Professor Unofficial Guide")
    gr.Markdown("Ask anything about RIT math professors based on real student reviews.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. What do students say about Professor Agyingi?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Sources", lines=8)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()