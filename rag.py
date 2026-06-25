import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import google.generativeai as genai
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
model = SentenceTransformer("BAAI/bge-m3")
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-2.5-flash")

GREETINGS = {
    "hi", "hello", "hey", "yo", "good morning", "good evening",
    "bonjour", "salut", "coucou", "bonsoir", "hello there"
}


def detect_language(text: str) -> str:
    english_greetings = {"hi", "hello", "hey", "yo", "good morning", "good evening", "hello there"}
    if text.strip().lower() in english_greetings:
        return "en"
    try:
        lang = detect(text)
        return "en" if lang == "en" else "fr"
    except Exception:
        return "fr"


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


def generate_answer(question, chunks, lang_tag="FRENCH"):
    context = ""
    for chunk in chunks:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"

    prompt = f"""Tu es TextilBot, un assistant expert en conformité réglementaire textile.
Tu réponds aux questions sur les normes textiles en te basant uniquement sur les documents fournis.

RÈGLE ABSOLUE : Tu dois répondre entièrement en {lang_tag}. Ne mélange pas les langues.

Règles :
- Cite toujours la source (article ou annexe)
- Si la question n'est pas liée aux textiles, réponds poliment en une phrase courte
- Sois précis et professionnel

Contexte documentaire :
{context}

Question : {question}

Réponds en {lang_tag} en citant les sources."""

    response = gemini.generate_content(prompt)
    return response.text


def ask_textilbot(question, top_k=5):
    normalized = question.strip().lower()
    if normalized in GREETINGS:
        lang = detect_language(question)
        if lang == "en":
            return "Hi! Ask me anything about textile labeling compliance under EU 1007/2011."
        return "Bonjour ! Posez-moi une question sur la conformité textile (étiquetage, fibres, EU 1007/2011)."

    lang = detect_language(question)
    lang_tag = "ENGLISH" if lang == "en" else "FRENCH"

    chunks = retrieve(question, top_k=top_k)
    answer = generate_answer(question, chunks, lang_tag=lang_tag)
    return answer


if __name__ == "__main__":
    question = "Which textile products are exempt from mandatory fibre labelling?"
    print("❓ Question:", question)
    print("⏳ Recherche en cours...")
    answer = ask_textilbot(question)
    print("\n🤖 TextilBot:")
    print(answer)