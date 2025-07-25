import os
from dotenv import load_dotenv
load_dotenv()

import json
from typing import List, Dict, Any
from vector_store import VectorStore
import openai
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RAGEvaluator:
    def __init__(self):
        self.vector_store = VectorStore()
        
    def retrieve_chunks(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks for a query."""
        results = self.vector_store.search(query, limit=top_k, score_threshold=0.3)
        return results
    
    def generate_answer(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Generate answer using retrieved chunks."""
        if not chunks:
            return "I don't have enough information to answer this question."
        
        context = "\n\n".join([chunk['text'] for chunk in chunks])
        prompt = (
            "Answer the following question using ONLY the context below. "
            "If the context does not contain enough information, say 'I don't know based on the provided context.'\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
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
        return response.choices[0].message.content
    
    def calculate_similarity_score(self, text1: str, text2: str) -> float:
        """Calculate a simple similarity score between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def evaluate_rag_performance(self, test_questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate RAG performance with comprehensive metrics."""
        print("Running RAG Evaluation...")
        results = []
        
        for i, test_case in enumerate(test_questions):
            print(f"Evaluating test case {i+1}/{len(test_questions)}: {test_case['question']}")
            
            query = test_case['question']
            expected_answer = test_case.get('expected_answer', '')
            expected_keywords = test_case.get('expected_keywords', [])
            
            # Retrieve and generate answer
            chunks = self.retrieve_chunks(query)
            generated_answer = self.generate_answer(query, chunks)
            
            # Calculate retrieval metrics
            retrieved_text = " ".join([chunk['text'] for chunk in chunks])
            found_keywords = [kw for kw in expected_keywords if kw.lower() in retrieved_text.lower()]
            keyword_recall = len(found_keywords) / len(expected_keywords) if expected_keywords else 0
            keyword_precision = len(found_keywords) / len(expected_keywords) if expected_keywords else 0
            
            # Calculate answer quality metrics
            answer_similarity = self.calculate_similarity_score(generated_answer, expected_answer)
            
            # Calculate chunk relevance scores
            chunk_scores = []
            for chunk in chunks:
                chunk_relevance = self.calculate_similarity_score(chunk['text'], query)
                chunk_scores.append(chunk_relevance)
            
            avg_chunk_relevance = sum(chunk_scores) / len(chunk_scores) if chunk_scores else 0
            
            results.append({
                'test_case_id': i + 1,
                'query': query,
                'generated_answer': generated_answer,
                'expected_answer': expected_answer,
                'retrieval_metrics': {
                    'keyword_recall': keyword_recall,
                    'keyword_precision': keyword_precision,
                    'found_keywords': found_keywords,
                    'expected_keywords': expected_keywords,
                    'retrieved_chunks': len(chunks),
                    'avg_chunk_relevance': avg_chunk_relevance
                },
                'answer_quality_metrics': {
                    'answer_similarity': answer_similarity,
                    'answer_length': len(generated_answer)
                },
                'chunks': [
                    {
                        'text': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                        'score': chunk.get('score', 0),
                        'relevance': score
                    } for chunk, score in zip(chunks, chunk_scores)
                ]
            })
        
        return results
    
    def calculate_overall_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall evaluation metrics."""
        if not results:
            return {}
        
        # Retrieval metrics
        avg_keyword_recall = sum(r['retrieval_metrics']['keyword_recall'] for r in results) / len(results)
        avg_keyword_precision = sum(r['retrieval_metrics']['keyword_precision'] for r in results) / len(results)
        avg_retrieved_chunks = sum(r['retrieval_metrics']['retrieved_chunks'] for r in results) / len(results)
        avg_chunk_relevance = sum(r['retrieval_metrics']['avg_chunk_relevance'] for r in results) / len(results)
        
        # Answer quality metrics
        avg_answer_similarity = sum(r['answer_quality_metrics']['answer_similarity'] for r in results) / len(results)
        avg_answer_length = sum(r['answer_quality_metrics']['answer_length'] for r in results) / len(results)
        
        return {
            'retrieval_metrics': {
                'average_keyword_recall': avg_keyword_recall,
                'average_keyword_precision': avg_keyword_precision,
                'average_retrieved_chunks': avg_retrieved_chunks,
                'average_chunk_relevance': avg_chunk_relevance
            },
            'answer_quality_metrics': {
                'average_answer_similarity': avg_answer_similarity,
                'average_answer_length': avg_answer_length
            },
            'total_test_cases': len(results)
        }

def main():
    # Sample test questions for evaluation
    test_questions = [
        {
            'question': 'What is the purpose of the Board mentioned in the document?',
            'expected_keywords': ['Board', 'purpose', 'supervisory', 'authority'],
            'expected_answer': 'The Board serves as a supervisory authority for data protection matters.'
        },
        {
            'question': 'What happens when a complaint is lodged?',
            'expected_keywords': ['complaint', 'lodged', 'supervisory', 'authority'],
            'expected_answer': 'The supervisory authority with which a complaint has been lodged shall inform the complainant on the decision.'
        },
        {
            'question': 'What are the time limits for decisions?',
            'expected_keywords': ['time', 'limit', 'decision', 'month'],
            'expected_answer': 'Decisions should be made without undue delay and at the latest by one month after the Board has notified its decision.'
        },
        {
            'question': 'What is the role of the European Data Protection Board?',
            'expected_keywords': ['European', 'Data', 'Protection', 'Board', 'role'],
            'expected_answer': 'The European Data Protection Board ensures the consistent application of data protection rules throughout the EU.'
        },
        {
            'question': 'How are decisions made by the Board?',
            'expected_keywords': ['decision', 'Board', 'majority', 'vote'],
            'expected_answer': 'The Board shall take decisions by a simple majority of its members.'
        }
    ]
    
    evaluator = RAGEvaluator()
    
    # Run evaluation
    detailed_results = evaluator.evaluate_rag_performance(test_questions)
    overall_metrics = evaluator.calculate_overall_metrics(detailed_results)
    
    # Print results
    print("\n" + "="*60)
    print("RAG EVALUATION RESULTS")
    print("="*60)
    
    print(f"\nOVERALL METRICS:")
    print(f"Total Test Cases: {overall_metrics['total_test_cases']}")
    
    print(f"\nRetrieval Performance:")
    print(f"- Average Keyword Recall: {overall_metrics['retrieval_metrics']['average_keyword_recall']:.3f}")
    print(f"- Average Keyword Precision: {overall_metrics['retrieval_metrics']['average_keyword_precision']:.3f}")
    print(f"- Average Retrieved Chunks: {overall_metrics['retrieval_metrics']['average_retrieved_chunks']:.1f}")
    print(f"- Average Chunk Relevance: {overall_metrics['retrieval_metrics']['average_chunk_relevance']:.3f}")
    
    print(f"\nAnswer Quality:")
    print(f"- Average Answer Similarity: {overall_metrics['answer_quality_metrics']['average_answer_similarity']:.3f}")
    print(f"- Average Answer Length: {overall_metrics['answer_quality_metrics']['average_answer_length']:.0f} characters")
    
    print(f"\nDETAILED RESULTS:")
    for result in detailed_results:
        print(f"\nTest Case {result['test_case_id']}: {result['query']}")
        print(f"  Keywords Found: {result['retrieval_metrics']['found_keywords']}")
        print(f"  Keyword Recall: {result['retrieval_metrics']['keyword_recall']:.3f}")
        print(f"  Keyword Precision: {result['retrieval_metrics']['keyword_precision']:.3f}")
        print(f"  Retrieved Chunks: {result['retrieval_metrics']['retrieved_chunks']}")
        print(f"  Chunk Relevance: {result['retrieval_metrics']['avg_chunk_relevance']:.3f}")
        print(f"  Answer Similarity: {result['answer_quality_metrics']['answer_similarity']:.3f}")
        print(f"  Generated Answer: {result['generated_answer'][:100]}...")
    
    # Save results
    from datetime import datetime
    evaluation_summary = {
        'overall_metrics': overall_metrics,
        'detailed_results': detailed_results,
        'evaluation_timestamp': str(datetime.now())
    }
    
    with open('rag_evaluation_results.json', 'w') as f:
        json.dump(evaluation_summary, f, indent=2)
    
    print(f"\nDetailed results saved to 'rag_evaluation_results.json'")
    
    # Print recommendations
    print(f"\nRECOMMENDATIONS:")
    if overall_metrics['retrieval_metrics']['average_keyword_recall'] < 0.5:
        print("- Consider improving chunking strategy or embedding model for better keyword retrieval")
    if overall_metrics['retrieval_metrics']['average_chunk_relevance'] < 0.3:
        print("- Consider adjusting similarity threshold or using different embedding model")
    if overall_metrics['answer_quality_metrics']['average_answer_similarity'] < 0.4:
        print("- Consider improving prompt engineering or using more context in generation")

if __name__ == "__main__":
    main() 