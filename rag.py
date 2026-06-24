import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from groq import Groq

load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = SentenceTransformer("BAAI/bge-m3", local_files_only=True)
qdrant = QdrantClient(path="./qdrant_storage")
groq_client = Groq(api_key=GROQ_API_KEY)


def retrieve(question, top_k=5):
    embedding = model.encode(question, normalize_embeddings=True)
    results = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    query=embedding.tolist(),
    limit=top_k
    ).points
    return [
        {"text": r.payload["text"], "source": r.payload["source"], "score": r.score}
        for r in results
    ]


def generate_answer(question, chunks):
    context = ""
    for chunk in chunks:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"

    system_prompt = """Tu es TextilBot, un assistant expert en conformité réglementaire textile.
Tu réponds aux questions sur les normes textiles en te basant uniquement sur les documents fournis.
Règles :
- Réponds en français
- Cite toujours la source
- Si l'information n'est pas dans le contexte, dis-le clairement
- Sois précis et professionnel"""

    user_prompt = f"""Contexte documentaire :
{context}

Question : {question}

Réponds de manière précise en citant les sources."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=1024
    )
    return response.choices[0].message.content


def ask_textilbot(question, top_k=5):
    chunks = retrieve(question, top_k=top_k)
    answer = generate_answer(question, chunks)
    return answer

if __name__ == "__main__":
    question = "Which textile products are exempt from mandatory fibre labelling?"
    print("❓ Question:", question)
    print("⏳ Recherche en cours...")
    answer = ask_textilbot(question)
    print("\n🤖 TextilBot:")
    print(answer)