import os
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from tqdm import tqdm

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# 1. Charger le PDF
def load_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# 2. Chunker
def chunk_text(text, source, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    chunk_id = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunk_str = " ".join(chunk_words)
        if len(chunk_words) > 30:
            chunks.append({
                "id": f"{source}_{chunk_id}",
                "text": chunk_str,
                "source": source,
                "chunk_index": chunk_id
            })
            chunk_id += 1
        i += chunk_size - overlap
    return chunks

# 3. Main
if __name__ == "__main__":
    print("📄 Chargement du PDF...")
    text = load_pdf("data/CELEX_32011R1007_EN_TXT.pdf")
    chunks = chunk_text(text, "EU_1007_2011")
    print(f"✅ {len(chunks)} chunks créés")

    print("⏳ Chargement du modèle BAAI/bge-m3...")
    model = SentenceTransformer("BAAI/bge-m3")

    print("⏳ Génération des embeddings...")
    texts = [c["text"] for c in chunks]
    embeddings = []
    for i in tqdm(range(0, len(texts), 32)):
        batch = texts[i:i+32]
        emb = model.encode(batch, normalize_embeddings=True)
        embeddings.extend(emb)

    print("⏳ Connexion à Qdrant...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE)
    )

    print("⏳ Indexation dans Qdrant...")
    for i in tqdm(range(0, len(chunks), 100)):
        batch_chunks = chunks[i:i+100]
        batch_emb = embeddings[i:i+100]
        points = [
            PointStruct(
                id=i+j,
                vector=batch_emb[j].tolist(),
                payload={
                    "text": batch_chunks[j]["text"],
                    "source": batch_chunks[j]["source"],
                    "chunk_index": batch_chunks[j]["chunk_index"]
                }
            )
            for j in range(len(batch_chunks))
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    print("Indexation terminée !")
