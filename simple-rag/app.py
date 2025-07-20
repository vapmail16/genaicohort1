import streamlit as st
from vector_store_simple import SimpleVectorStore
from simple_text_cleaner import create_simple_text_cleaner
from config import REMOVE_STOPWORDS, REMOVE_NUMBERS
import openai
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import numpy as np

# Use the new OpenAI client for v1+ API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="PDF Q&A with LLM (RAG Demo)", layout="wide")
st.title("Ask Questions About Your PDF (RAG + LLM Demo)")

st.write("""
Type a question about your PDF. The app will retrieve the most relevant chunks from your vector database and use an LLM to generate an answer.
""")

@st.cache_resource(show_spinner=False)
def get_vector_store():
    return SimpleVectorStore()

@st.cache_resource(show_spinner=False)
def get_text_cleaner():
    return create_simple_text_cleaner(remove_numbers=REMOVE_NUMBERS)

def extract_keywords(text, max_keywords=10):
    """Extract keywords from text using TF-IDF"""
    # Simple keyword extraction - split into words and filter
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    # Remove common stopwords
    stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an', 'as', 'from', 'not', 'no', 'yes', 'if', 'then', 'else', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'you', 'your', 'yours', 'yourself', 'yourselves', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'what', 'which', 'who', 'whom', 'whose', 'whichever', 'whoever', 'whomever', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves'}
    keywords = [word for word in words if word not in stopwords]
    # Return top keywords by frequency
    from collections import Counter
    keyword_counts = Counter(keywords)
    return [word for word, count in keyword_counts.most_common(max_keywords)]

def keyword_search(query, documents, top_k=5):
    """Perform keyword-based search"""
    query_keywords = set(extract_keywords(query))
    
    results = []
    for doc in documents:
        doc_keywords = set(extract_keywords(doc['text']))
        # Calculate keyword overlap
        overlap = len(query_keywords.intersection(doc_keywords))
        total_keywords = len(query_keywords.union(doc_keywords))
        if total_keywords > 0:
            keyword_score = overlap / total_keywords
        else:
            keyword_score = 0.0
        
        results.append({
            'text': doc['text'],
            'score': keyword_score,
            'matched_keywords': list(query_keywords.intersection(doc_keywords)),
            'search_type': 'keyword'
        })
    
    # Sort by keyword score and return top_k
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

def euclidean_search(query, documents, top_k=5, score_threshold=0.1):
    """Perform Euclidean distance-based search using scikit-learn for efficient batch processing"""
    if not documents:
        return []
    
    # Create TF-IDF vectorizer for text representation
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95
    )
    
    # Prepare documents for vectorization
    doc_texts = [doc['text'] for doc in documents]
    doc_texts.append(query)  # Add query to the corpus
    
    # Fit and transform the documents
    try:
        tfidf_matrix = vectorizer.fit_transform(doc_texts)
        
        # Get query vector (last row) and document vectors (all except last)
        query_vector = tfidf_matrix[-1:].toarray()
        doc_vectors = tfidf_matrix[:-1].toarray()
        
        # Calculate Euclidean distances using scikit-learn for efficient batch processing
        distances = euclidean_distances(query_vector, doc_vectors)[0]
        
        # Convert distances to similarity scores (lower distance = higher similarity)
        # Normalize distances to 0-1 range and invert (1 - normalized_distance)
        max_distance = np.max(distances) if np.max(distances) > 0 else 1
        similarity_scores = 1 - (distances / max_distance)
        
        # Create results with distance and similarity information
        results = []
        for i, (doc, distance, similarity) in enumerate(zip(documents, distances, similarity_scores)):
            if similarity >= score_threshold:
                results.append({
                    'text': doc['text'],
                    'euclidean_distance': distance,
                    'similarity_score': similarity,
                    'search_type': 'euclidean'
                })
        
        # Sort by ascending Euclidean distance (closest first)
        results.sort(key=lambda x: x['euclidean_distance'])
        return results[:top_k]
        
    except Exception as e:
        st.error(f"Error in Euclidean search: {str(e)}")
        return []

def hybrid_search(query, vector_store, text_cleaner, vector_weight=0.6, keyword_weight=0.4, top_k=5, score_threshold=0.1):
    """Perform hybrid search combining vector and keyword search"""
    # Get vector search results
    cleaned_query = text_cleaner.clean_text(query, remove_stopwords=REMOVE_STOPWORDS)
    vector_results = vector_store.search(cleaned_query, limit=top_k*2, score_threshold=score_threshold)
    
    # Get keyword search results
    keyword_results = keyword_search(query, vector_results, top_k*2)
    
    # Create a mapping of text to results for easy lookup
    vector_map = {r['text']: r for r in vector_results}
    keyword_map = {r['text']: r for r in keyword_results}
    
    # Combine results
    combined_results = []
    all_texts = set(vector_map.keys()) | set(keyword_map.keys())
    
    for text in all_texts:
        vector_score = vector_map.get(text, {}).get('score', 0.0)
        keyword_score = keyword_map.get(text, {}).get('score', 0.0)
        
        # Normalize scores to 0-1 range
        vector_score = max(0, min(1, vector_score))
        keyword_score = max(0, min(1, keyword_score))
        
        # Calculate combined score
        combined_score = (vector_weight * vector_score) + (keyword_weight * keyword_score)
        
        # Get matched keywords
        matched_keywords = keyword_map.get(text, {}).get('matched_keywords', [])
        
        combined_results.append({
            'text': text,
            'combined_score': combined_score,
            'vector_score': vector_score,
            'keyword_score': keyword_score,
            'matched_keywords': matched_keywords,
            'search_type': 'hybrid'
        })
    
    # Sort by combined score and return top_k
    combined_results.sort(key=lambda x: x['combined_score'], reverse=True)
    return combined_results[:top_k]

vs = get_vector_store()
text_cleaner = get_text_cleaner()

# Search mode selection
search_mode = st.selectbox(
    "Choose Search Mode:",
    ["Vector Search (Cosine)", "Euclidean Distance Search", "Keyword Search", "Hybrid Search"],
    help="Vector Search: Semantic similarity using cosine similarity\nEuclidean Distance: L2 distance-based similarity\nKeyword Search: Exact keyword matching\nHybrid Search: Combines vector and keyword approaches"
)

# Hybrid search parameters (only show for hybrid mode)
if search_mode == "Hybrid Search":
    col1, col2 = st.columns(2)
    with col1:
        vector_weight = st.slider("Vector Weight", 0.0, 1.0, 0.6, 0.1, help="How much to weight semantic similarity")
    with col2:
        keyword_weight = st.slider("Keyword Weight", 0.0, 1.0, 0.4, 0.1, help="How much to weight keyword matching")
    
    # Show combined weight
    total_weight = vector_weight + keyword_weight
    if abs(total_weight - 1.0) > 0.01:
        st.warning(f"⚠️ Total weight is {total_weight:.2f}. Consider adjusting weights to sum to 1.0 for optimal results.")

question = st.text_input("Enter your question:")
score_threshold = st.slider("Score threshold (lower = more results, higher = stricter)", 0.0, 1.0, 0.1, 0.05)
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
        if search_mode in ["Keyword Search", "Hybrid Search", "Euclidean Distance Search"]:
            st.write(f"**Extracted Keywords:** {extract_keywords(question)}")
    
    with st.spinner(f"Searching using {search_mode}..."):
        if search_mode == "Vector Search (Cosine)":
            results = vs.search(cleaned_question, limit=top_k, score_threshold=score_threshold)
            # Convert to standard format
            results = [{'text': r['text'], 'score': r['score'], 'search_type': 'vector'} for r in results]
        elif search_mode == "Euclidean Distance Search":
            # Get all documents for Euclidean search
            all_docs = vs.search(cleaned_question, limit=50, score_threshold=0.0)
            results = euclidean_search(question, all_docs, top_k, score_threshold)
        elif search_mode == "Keyword Search":
            # Get all documents for keyword search
            all_docs = vs.search(cleaned_question, limit=50, score_threshold=0.0)
            results = keyword_search(question, all_docs, top_k)
        elif search_mode == "Hybrid Search":
            # Get all documents for hybrid search
            all_docs = vs.search(cleaned_question, limit=50, score_threshold=0.0)
            results = hybrid_search(question, vs, text_cleaner, vector_weight, keyword_weight, top_k, score_threshold)
    
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
        
        # Display results based on search type
        st.markdown("#### Retrieved Chunks")
        for i, r in enumerate(unique_chunks, 1):
            if search_mode == "Vector Search (Cosine)":
                st.markdown(f"**Chunk {i} (Cosine Similarity: {r['score']:.4f})**\n\n{r['text']}\n\n---")
            elif search_mode == "Euclidean Distance Search":
                st.markdown(f"**Chunk {i} (Euclidean Distance: {r['euclidean_distance']:.4f}, Similarity: {r['similarity_score']:.4f})**\n\n{r['text']}\n\n---")
            elif search_mode == "Keyword Search":
                st.markdown(f"**Chunk {i} (Keyword Score: {r['score']:.4f})**")
                if r['matched_keywords']:
                    st.markdown(f"**Matched Keywords:** {', '.join(r['matched_keywords'])}")
                st.markdown(f"\n{r['text']}\n\n---")
            elif search_mode == "Hybrid Search":
                st.markdown(f"**Chunk {i} (Combined Score: {r['combined_score']:.4f})**")
                st.markdown(f"**Vector Score:** {r['vector_score']:.4f} | **Keyword Score:** {r['keyword_score']:.4f}")
                if r['matched_keywords']:
                    st.markdown(f"**Matched Keywords:** {', '.join(r['matched_keywords'])}")
                st.markdown(f"\n{r['text']}\n\n---")
        
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
        st.warning("No relevant chunk found. Try lowering the score threshold or re-ingesting with a larger chunk size/overlap.") 