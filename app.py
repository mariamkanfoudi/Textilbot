import streamlit as st
from rag import ask_textilbot
from datetime import datetime

st.set_page_config(
    page_title="TextilBot",
    page_icon="🧵",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f5f0eb;
        background-image: 
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(139, 90, 43, 0.05) 10px,
                rgba(139, 90, 43, 0.05) 20px
            ),
            repeating-linear-gradient(
                -45deg,
                transparent,
                transparent 10px,
                rgba(101, 67, 33, 0.05) 10px,
                rgba(101, 67, 33, 0.05) 20px
            );
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(5px);
    }
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
    }
    h1 {
        color: #5c3317 !important;
        font-family: 'Georgia', serif !important;
        text-align: center !important;
    }
    .stCaption {
        color: #8b5e3c !important;
        text-align: center !important;
    }
    .fabric-header {
        background: repeating-linear-gradient(
            90deg,
            #c8a882 0px,
            #c8a882 2px,
            #e8d5b7 2px,
            #e8d5b7 20px
        ),
        repeating-linear-gradient(
            0deg,
            #c8a882 0px,
            #c8a882 2px,
            transparent 2px,
            transparent 20px
        );
        height: 8px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
</style>
<div class="fabric-header"></div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────
with st.sidebar:
    st.title("🧵 TextilBot 🧵")
    st.caption("Assistant conformité réglementaire textile")
    st.divider()

    st.subheader("💡 Questions exemples")
    example_questions = [
        "Quelles informations doivent figurer sur l'étiquette d'un produit multi-fibres ?",
        "Quels produits textiles sont exemptés d'étiquetage obligatoire ?",
        "Quel pourcentage de fibres étrangères est autorisé dans un produit pur ?",
        "Un distributeur peut-il être considéré comme fabricant ?",
        "Que signifie l'étiquetage inclusif ?",
        "What are the labelling requirements for corsetry products?",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True, key=q):
            st.session_state.pending_question = q

    st.divider()

    if st.session_state.get("messages"):
        st.subheader("📥 Exporter")
        conversation_text = f"TextilBot — Conversation exportée le {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        conversation_text += "=" * 60 + "\n\n"
        for msg in st.session_state.messages:
            role = "👤 Utilisateur" if msg["role"] == "user" else "🤖 TextilBot"
            conversation_text += f"{role}:\n{msg['content']}\n\n" + "-" * 40 + "\n\n"

        st.download_button(
            label="📄 Télécharger la conversation",
            data=conversation_text,
            file_name=f"textilbot_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

# ── Main ──────────────────────────────────────────
st.title("🧵 TextilBot 🧵")
st.caption("Assistant expert en conformité réglementaire textile — EU 1007/2011")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            col1, col2, col3 = st.columns([1, 1, 8])
            feedback_key = f"feedback_{i}"
            current = st.session_state.feedback.get(feedback_key)
            with col1:
                if st.button("👍", key=f"up_{i}", help="Bonne réponse"):
                    st.session_state.feedback[feedback_key] = "positive"
                    st.rerun()
            with col2:
                if st.button("👎", key=f"down_{i}", help="Mauvaise réponse"):
                    st.session_state.feedback[feedback_key] = "negative"
                    st.rerun()
            with col3:
                if current == "positive":
                    st.success("✅ Merci pour votre retour !")
                elif current == "negative":
                    st.warning("⚠️ Merci, nous améliorerons cette réponse.")

if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            answer = ask_textilbot(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

if prompt := st.chat_input("Posez votre question sur la conformité textile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            answer = ask_textilbot(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()