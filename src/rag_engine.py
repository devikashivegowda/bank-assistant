import os
import logging
import numpy as np
import faiss
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class LoanAssistantRAG:
    """
    A RAG pipeline for Bank of Maharashtra loan products using FAISS and Groq.
    """
    def __init__(self, data_path="data/knowledge_base.txt"):
        """Initializes the embedding model, FAISS index, and Groq client."""
        try:
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
            self._prepare_knowledge_base(data_path)
            logger.info("RAG Engine initialized successfully.")
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise

    def _prepare_knowledge_base(self, data_path):
        """Loads, chunks, and indexes the knowledge base."""
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Missing knowledge base: {data_path}")
            
        with open(data_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.chunks = splitter.split_text(text)
        
        embeddings = self.embed_model.encode(self.chunks)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))

    def retrieve(self, query, k=3):
        """Retrieves the top k relevant chunks for a given query."""
        query_vector = self.embed_model.encode([query])
        _, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        return "\n".join([self.chunks[i] for i in indices[0]])

    def query(self, user_input):
        """Generates an answer based on retrieved context."""
        try:
            context = self.retrieve(user_input)
            
            prompt = f"Use the context to answer: {user_input}\n\nCONTEXT:\n{context}"
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a Bank of Maharashtra Assistant. Use ONLY provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Query generation failed: {e}")
            return "I encountered an error processing your request."

def setup_rag_chain():
    return LoanAssistantRAG()