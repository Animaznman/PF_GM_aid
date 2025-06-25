import streamlit as st
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
import os

# --- Config ---
st.set_page_config(page_title="Pathfinder Agent", layout="centered")

st.title("🧙 Pathfinder Agent")
st.caption("Ask questions about the Pathfinder universe!")

# --- API Key ---
api_key = os.getenv("GEMINI_KEY")
if not api_key:
    api_key = st.text_input("🔐 Enter your Gemini API Key", type="password")
    if api_key:
        os.environ["GEMINI_KEY"] = api_key

# --- Load vector store ---
@st.cache_resource
def load_chain():
    emb_fn = HuggingFaceEmbeddings(
        model_name="intfloat/e5-large-v2",
        encode_kwargs={"normalize_embeddings": True},   # E5 wants norm=True
    )

    vectordb = Chroma(persist_directory="chroma_db", embedding_function=emb_fn)

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=api_key)
    chain = RetrievalQA.from_llm(llm=llm, retriever=vectordb.as_retriever())
    return chain

if api_key:
    qa_chain = load_chain()

    # --- Query Input ---
    query = st.text_input("Ask me anything about Pathfinder...")
    if query:
        with st.spinner("Consulting the scrolls..."):
            result = qa_chain.run(query)
        st.markdown("### 📜 Answer")
        st.write(result)
