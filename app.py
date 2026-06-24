import streamlit as st
from rag import ask_textilbot

st.set_page_config(
    page_title="TextilBot",
    page_icon="🧵",
    layout="centered"
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
    }
    
    .stCaption {
        color: #8b5e3c !important;
    }

    /* Motifs tissu en header */
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

st.title("🧵 TextilBot")
st.caption("Assistant expert en conformité réglementaire textile — EU 1007/2011")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question sur la conformité textile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            answer = ask_textilbot(prompt)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})