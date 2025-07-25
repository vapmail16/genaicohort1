import streamlit as st
from hybrid_vector_store import HybridVectorStore
from simple_text_cleaner import create_simple_text_cleaner
from config import REMOVE_STOPWORDS, REMOVE_NUMBERS
import openai
import os

# Use the new OpenAI client for v1+ API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Hybrid Search RAG Demo", layout="wide")
st.title("Hybrid Search RAG Demo (Vector + Keyword Search)")

st.write("""
This demo shows hybrid search combining vector similarity and keyword matching for better document retrieval.
""")

@st.cache_resource(show_spinner=False)
def get_vector_store():
    return HybridVectorStore()

@st.cache_resource(show_spinner=False)
def get_text_cleaner():
    return create_simple_text_cleaner(remove_numbers=REMOVE_NUMBERS)

vs = get_vector_store()
text_cleaner = get_text_cleaner()

# Sidebar for search configuration
st.sidebar.header("Search Configuration")

search_type = st.sidebar.selectbox(
    "Search Type",
    ["Hybrid Search", "Vector Search Only", "Keyword Search Only"],
    help="Choose the type of search to perform"
)

if search_type == "Hybrid Search":
    vector_weight = st.sidebar.slider(
        "Vector Weight", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.6, 
        step=0.1,
        help="Weight for vector similarity scores"
    )
    keyword_weight = st.sidebar.slider(
        "Keyword Weight", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.4, 
        step=0.1,
        help="Weight for keyword search scores"
    )
    st.sidebar.write(f"**Combined Weight**: {vector_weight + keyword_weight:.1f}")

score_threshold = st.sidebar.slider(
    "Score threshold", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.1, 
    step=0.05,
    help="Minimum similarity score threshold"
)

top_k = st.sidebar.slider(
    "Number of chunks", 
    min_value=1, 
    max_value=15, 
    value=5,
    help="Number of chunks to retrieve"
)

# Main content
question = st.text_input("Enter your question:")

if question:
    # Clean the query to match the cleaned ingested data
    cleaned_question = text_cleaner.clean_text(question, remove_stopwords=REMOVE_STOPWORDS)
    
    # Show cleaning info in debug mode
    with st.expander("🔧 Text Cleaning Info (Debug)"):
        st.write(f"**Original Query:** {question}")
        st.write(f"**Cleaned Query:** {cleaned_question}")
        st.write(f"**Stopwords Removed:** {REMOVE_STOPWORDS}")
        st.write(f"**Numbers Removed:** {REMOVE_NUMBERS}")
    
    # Perform search based on selected type
    with st.spinner(f"Performing {search_type.lower()}..."):
        if search_type == "Hybrid Search":
            results = vs.hybrid_search(
                cleaned_question, 
                limit=top_k, 
                vector_weight=vector_weight, 
                keyword_weight=keyword_weight
            )
        elif search_type == "Vector Search Only":
            results = vs.search(cleaned_question, limit=top_k, score_threshold=score_threshold)
        else:  # Keyword Search Only
            results = vs._keyword_search(cleaned_question, limit=top_k)
    
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
        
        # Display results with detailed scoring
        st.markdown("#### Retrieved Chunks")
        for i, r in enumerate(unique_chunks, 1):
            st.markdown(f"**Chunk {i}**")
            
            # Show different score information based on search type
            if search_type == "Hybrid Search":
                st.markdown(f"""
                - **Combined Score**: {r['score']:.4f}
                - **Vector Score**: {r.get('vector_score', 0):.4f}
                - **Keyword Score**: {r.get('keyword_score', 0):.4f}
                - **Matched Keywords**: {', '.join(r.get('matched_keywords', []))}
                """)
            else:
                st.markdown(f"- **Score**: {r['score']:.4f}")
            
            st.markdown(f"**Text**:\n{r['text']}\n\n---")
        
        # LLM Answer section
        st.markdown("#### LLM Answer")
        with st.spinner("Generating answer with LLM..."):
            try:
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
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
                st.info("The search functionality worked - you can see the relevant chunks above. The error is with the OpenAI API.")
    else:
        st.warning("No relevant chunk found. Try adjusting the search parameters or re-ingesting documents.")

# Add information about hybrid search
st.sidebar.markdown("---")
st.sidebar.markdown("### About Hybrid Search")
st.sidebar.markdown("""
**Vector Search**: Finds semantically similar content using TF-IDF embeddings.

**Keyword Search**: Finds exact keyword matches and calculates overlap scores.

**Hybrid Search**: Combines both approaches for better results:
- Captures semantic meaning (vector)
- Ensures keyword relevance (keyword)
- Configurable weights for fine-tuning
""") 