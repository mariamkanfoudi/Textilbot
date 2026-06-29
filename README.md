
------**🧵 TextilBot — Assistant de Conformité Réglementaire Textile**

TextilBot est un assistant conversationnel basé sur RAG (Retrieval-Augmented Generation) 
qui répond aux questions sur la conformité réglementaire textile selon le Règlement EU 1007/2011,
en français et en anglais.
----------** Application déployée**

L'application est accessible en ligne :  
👉 [https://textilbot-eigsxsrozhszp8lq5zuxjk.streamlit.app/](https://textilbot-eigsxsrozhszp8lq5zuxjk.streamlit.app/)

-------** Architecture**

PDF (EU 1007/2011) → Chunks → BAAI/bge-m3 → Qdrant Cloud


                                                    ↓
Question → BAAI/bge-m3 → Retrieval → Gemini 2.5 Flash → Réponse


-----**  Stack Technique**

- **Embeddings** : BAAI/bge-m3
- **Base vectorielle** : Qdrant Cloud
- **LLM** : Gemini 2.5 Flash (Google)
- **Interface** : Streamlit
- **Détection de langue** : langdetect
- **Source** : Règlement EU No 1007/2011

---------** Fonctionnalités**

- Réponses précises avec citation des sources (article/annexe)
- Support multilingue français / anglais
- Questions exemples dans la sidebar
- Export de la conversation en .txt
- Feedback utilisateur 👍 👎

-------** Installation locale**

bash
Python 3.11.9 requis
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

 Configurer .env
GEMINI_API_KEY=ta_clé
QDRANT_URL=ton_url
QDRANT_API_KEY=ta_clé
COLLECTION_NAME=textilbot

 Indexer le PDF (une seule fois)
py ingest.py

 Lancer l'application
py -m streamlit run app.py
```

