import streamlit as st
from vector_store import VectorStore
import openai
import os

# Use the new OpenAI client for v1+ API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="PDF Q&A with LLM (RAG Demo)", layout="wide")
st.title("Ask Questions About Your PDF (RAG + LLM Demo)")

st.write("""
Type a question about your PDF. The app will retrieve the most relevant chunks from your vector database and use an LLM to generate an answer.
""")

@st.cache_resource(show_spinner=False)
def get_vector_store():
    return VectorStore()

vs = get_vector_store()

question = st.text_input("Enter your question:")
score_threshold = st.slider("Score threshold (lower = more results, higher = stricter)", 0.0, 1.0, 0.3, 0.05)
top_k = st.slider("Number of chunks to use as context", 1, 10, 5)

if question:
    with st.spinner("Searching for the most relevant chunk(s)..."):
        results = vs.search(question, limit=top_k, score_threshold=score_threshold)
    if results:
        context = "\n\n".join([r['text'] for r in results])
        st.markdown("#### Retrieved Chunks")
        for i, r in enumerate(results, 1):
            st.markdown(f"**Chunk {i} (Score: {r['score']:.4f})**\n\n{r['text']}\n\n---")
        st.markdown("#### LLM Answer")
        with st.spinner("Generating answer with LLM..."):
            prompt = (
                "Answer the following question using ONLY the context below. "
                "If the context does not contain enough information, say 'I don't know based on the provided context.'\n\n"
                f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for answering questions about a document."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.2,
            )
            answer = response.choices[0].message.content
            st.success(answer)
    else:
        st.warning("No relevant chunk found. Try lowering the score threshold or re-ingesting with a larger chunk size/overlap.") 