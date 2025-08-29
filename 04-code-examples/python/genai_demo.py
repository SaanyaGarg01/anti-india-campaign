#!/usr/bin/env python3
"""
GenAI Demo Script - Comprehensive Examples
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# AI/ML Libraries
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GenAIProject:
    name: str
    description: str
    model_type: str
    use_case: str
    created_date: datetime
    status: str = "active"

class TextGenerationDemo:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.text_generator = pipeline("text-generation", model="gpt2")
        
    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        try:
            result = self.text_generator(prompt, max_length=max_length, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            return f"Error: {e}"
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        try:
            result = self.sentiment_analyzer(text)
            return {
                "text": text,
                "sentiment": result[0]['label'],
                "confidence": result[0]['score']
            }
        except Exception as e:
            return {"error": str(e)}

class RAGDemo:
    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.document_vectors = None
        
    def add_documents(self, documents: List[str]):
        self.documents = documents
        self.document_vectors = self.vectorizer.fit_transform(documents)
        
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.documents:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "similarity_score": float(similarities[idx]),
                "rank": len(results) + 1
            })
        
        return results

def main():
    print("🚀 GenAI Demo - Future Opportunities & Skills")
    print("=" * 50)
    
    # Initialize components
    text_gen = TextGenerationDemo()
    rag_system = RAGDemo()
    
    # Demo 1: Text Generation
    print("\n📝 Text Generation Demo")
    prompt = "The future of artificial intelligence will"
    generated_text = text_gen.generate_text(prompt, max_length=50)
    print(f"Prompt: {prompt}")
    print(f"Generated: {generated_text}")
    
    # Demo 2: Sentiment Analysis
    print("\n😊 Sentiment Analysis Demo")
    sample_texts = [
        "I love this new AI technology!",
        "This AI system is terrible and unreliable."
    ]
    
    for text in sample_texts:
        sentiment = text_gen.analyze_sentiment(text)
        print(f"Text: {text}")
        print(f"Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']:.2f})")
    
    # Demo 3: RAG System
    print("\n🔍 RAG System Demo")
    documents = [
        "AI is transforming healthcare through improved diagnosis.",
        "Machine learning predicts equipment failures in manufacturing.",
        "AI chatbots revolutionize customer service."
    ]
    
    rag_system.add_documents(documents)
    query = "How is AI improving healthcare?"
    search_results = rag_system.search_documents(query)
    
    print(f"Query: {query}")
    for result in search_results:
        print(f"Rank {result['rank']}: {result['document']}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()
