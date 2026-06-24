**TextilBot (Assistant de Conformité Réglementaire Textile)**

TextilBot est un assistant conversationnel basé sur RAG (Retrieval-Augmented Generation)
qui répond aux questions sur la conformité réglementaire textile selon le règlement EU 1007/2011.

---------⚙️ Installation ⚙️----------

bash

1.Créer l'environnement virtuel (Python 3.11)

py -3.11 -m venv venv

venv\Scripts\activate

2.Installer les dépendances

pip install qdrant-client sentence-transformers pypdf groq streamlit python-dotenv tqdm

3.Configurer les variables d'environnement

Créer un fichier .env :

GROQ_API_KEY=votre_clé_groq

COLLECTION_NAME=textilbot

4.Indexer le PDF (executé une seule fois)

py ingest.py

5.Lancer l'application

streamlit run app.py
