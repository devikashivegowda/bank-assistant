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

    def retrieve(self, query, k=5):
        query_vector = self.embed_model.encode([query])
        _, indices = self.index.search(np.array(query_vector).astype('float32'), k)

        query_lower = query.lower()
        results = []

        for i in indices[0]:
            chunk = self.chunks[i]

            if "interest" in query_lower and "INTEREST_RATE" in chunk:
                results.append(chunk)
            elif "tenure" in query_lower and "TENURE" in chunk:
                results.append(chunk)
            elif "eligibility" in query_lower and "ELIGIBILITY" in chunk:
                results.append(chunk)
            else:
                results.append(chunk)

        return "\n".join(results[:3])

    def query(self, user_input):
        context = self.retrieve(user_input)
        
        # NEW: More flexible but still safe prompt
        system_prompt = f"""
        You are a professional Bank of Maharashtra Loan Assistant.

        Your job is to provide DETAILED, structured, and helpful explanations.

        IMPORTANT RULES:
        start with a short introduction then give detailed explanation
        1. Always elaborate the answer clearly.
        2. Use bullet points or numbered format where possible.
        3. Explain each factor in simple terms.
        4. If eligibility is asked:
        - Explain criteria
        - Mention different categories (salaried, self-employed, etc.)
        5. Do NOT give short answers.
        6. Do NOT say "not mentioned" or "refer to website".
        7. Keep answers user-friendly and professional.

        CONTEXT:
        {context}
        """
    
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Explain in detail: {user_input}"
                }
            ],
            temperature=0.2
        )

        # 👉 Extract answer
        answer = completion.choices[0].message.content
        if "click" in answer.lower() or "visit" in answer.lower():
            answer = "Bank of Maharashtra offers competitive home loan interest rates. These rates vary depending on factors like loan amount, tenure, and applicant profile. The bank also provides benefits such as flexible repayment options and concessions for certain categories of borrowers."


        # 👉 Fix bad responses (fallback logic)
        if "not explicitly" in answer.lower() or "not mentioned" in answer.lower():
            answer = "Bank of Maharashtra offers competitive home loan interest rates. The exact rate varies depending on applicant profile and loan type. You can check the official website for the latest rates."

        return answer    

def setup_rag_chain():
    return LoanAssistantRAG()

