import streamlit as st
from loaders.pdf_loader import load_and_split_pdf
from embeddings.embedder import get_embedding_model
from vectorstore.faiss_store import create_faiss_index
from rag.retriever import get_retriever
from rag.context_builder import build_context
from rag.scaledown_client import compress_prompt
from rag.generator import generate_answer
import tempfile

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Scientific Literature Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# TIGHTENED PREMIUM CSS
# -------------------------------------------------
st.markdown("""
<style>

/* ---------- Background ---------- */
.stApp {
    background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 50%, #ecfeff 100%);
    font-family: "Inter", sans-serif;
}

/* ---------- HERO ---------- */
.hero {
    text-align: center;
    padding: 40px 20px 10px 20px;   /* REDUCED SPACE */
}

.hero-title {
    font-size: 54px;
    font-weight: 800;
    background: linear-gradient(90deg, #1e3a8a, #0d9488);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 19px;
    color: #475569;
    max-width: 720px;
    margin: 8px auto 0 auto;   /* TIGHT */
    line-height: 1.6;
}

/* ---------- STEP CARDS ---------- */
.step-card {
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 26px;              /* REDUCED */
    margin: 18px auto;          /* REDUCED GAP BETWEEN STEPS */
    max-width: 880px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.06);
    border: 1px solid rgba(255,255,255,0.4);
}

/* ---------- STEP TITLES ---------- */
.step-title {
    font-size: 24px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 12px;   /* TIGHT */
}

/* ---------- UPLOADER LABEL BIGGER ---------- */
.upload-label {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* ---------- QUESTION LABEL BIGGER ---------- */
.question-label {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* ---------- INPUT ---------- */
.stTextInput input {
    border-radius: 12px;
    border: 1px solid #dbe2ef;
    padding: 12px;
    background: #f9fbff;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    border-radius: 14px;
    padding: 12px 28px;
    font-weight: 600;
    color: white;
    border: none;
    background: linear-gradient(90deg, #1e3a8a, #0d9488);
    box-shadow: 0 8px 20px rgba(30,58,138,0.25);
}

/* ---------- ANSWER PANEL ---------- */
.answer-panel {
    background: linear-gradient(135deg, #ffffff, #f1f5ff);
    border-radius: 20px;
    padding: 28px;
    border-left: 6px solid #0d9488;
    box-shadow: 0 12px 28px rgba(0,0,0,0.08);
    max-width: 880px;
    margin: 20px auto 30px auto;   /* TIGHT + CENTERED */
}

.answer-title {
    font-size: 24px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 14px;
}

.answer-text {
    font-size: 17px;
    line-height: 1.7;
    color: #334155;
    text-align: left;   /* FIXED ALIGNMENT */
    white-space: pre-wrap;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO (NO EXTRA BOX BELOW — REMOVED)
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">🔬 Scientific Literature Explorer</div>
    <div class="hero-subtitle">
        Query scientific PDFs using Retrieval-Augmented Generation.
        Upload research, ask questions, and generate grounded answers.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# STEP 1 — UPLOAD
# -------------------------------------------------
st.markdown('<div class="step-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="step-title">📂 Step 1 — Upload Research Paper</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="upload-label">Upload PDF</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "",
    type=["pdf"]
)

if uploaded_file:
    st.success("PDF uploaded successfully.")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 2 — QUESTION
# -------------------------------------------------
question = None
ask_btn = False

if uploaded_file:

    st.markdown('<div class="step-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="step-title">❓ Step 2 — Ask a Question</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-label">Enter your question about the paper</div>',
        unsafe_allow_html=True
    )

    question = st.text_input("")

    ask_btn = st.button("Generate Answer")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STEP 3 — ANSWER
# -------------------------------------------------
if ask_btn and uploaded_file and question:

    with st.spinner("Analyzing document and generating answer..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        chunks = load_and_split_pdf(pdf_path)
        embedding_model = get_embedding_model()
        vectorstore = create_faiss_index(chunks, embedding_model)
        retriever = get_retriever(vectorstore)
        retrieved_docs = retriever.invoke(question)
        context = build_context(retrieved_docs)
        compressed_prompt = compress_prompt(context, question)
        answer = generate_answer(compressed_prompt)

    st.markdown(f"""
    <div class="answer-panel">
        <div class="answer-title">📌 Answer</div>
        <div class="answer-text">{answer}</div>
    </div>
    """, unsafe_allow_html=True)
