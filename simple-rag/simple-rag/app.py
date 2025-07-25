import streamlit as st
from vector_store import VectorStore
from simple_text_cleaner import create_simple_text_cleaner
from config import REMOVE_STOPWORDS, REMOVE_NUMBERS
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

@st.cache_resource(show_spinner=False)
def get_text_cleaner():
    return create_simple_text_cleaner(remove_numbers=REMOVE_NUMBERS)

vs = get_vector_store()
text_cleaner = get_text_cleaner()

question = st.text_input("Enter your question:")
score_threshold = st.slider("Score threshold (lower = more results, higher = stricter)", 0.0, 1.0, 0.3, 0.05)
top_k = st.slider("Number of chunks to use as context", 1, 10, 5)

if question:
    # Clean the query to match the cleaned ingested data
    cleaned_question = text_cleaner.clean_text(question, remove_stopwords=REMOVE_STOPWORDS)
    
    # Show cleaning info in debug mode
    with st.expander("🔧 Text Cleaning Info (Debug)"):
        st.write(f"**Original Query:** {question}")
        st.write(f"**Cleaned Query:** {cleaned_question}")
        st.write(f"**Stopwords Removed:** {REMOVE_STOPWORDS}")
        st.write(f"**Numbers Removed:** {REMOVE_NUMBERS}")
    
    with st.spinner("Searching for the most relevant chunk(s)..."):
        results = vs.search(cleaned_question, limit=top_k, score_threshold=score_threshold)
    if results:
        # Deduplicate chunks to avoid repetition
        unique_chunks = []
        seen_texts = set()
        for r in results:
            # Normalize text for comparison (remove extra spaces, newlines)
            normalized_text = ' '.join(r['text'].split())
            if normalized_text not in seen_texts:
                unique_chunks.append(r)
                seen_texts.add(normalized_text)
        
        context = "\n\n".join([r['text'] for r in unique_chunks])
        st.markdown("#### Retrieved Chunks")
        for i, r in enumerate(unique_chunks, 1):
            st.markdown(f"**Chunk {i} (Score: {r['score']:.4f})**\n\n{r['text']}\n\n---")
        st.markdown("#### LLM Answer")
        with st.spinner("Generating answer with LLM..."):
            prompt = f"""Based on the following text, answer this question:

Text: {context}

Question: {question}

Answer:"""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.1,
            )
            answer = response.choices[0].message.content
            st.success(answer)
    else:
        st.warning("No relevant chunk found. Try lowering the score threshold or re-ingesting with a larger chunk size/overlap.") 