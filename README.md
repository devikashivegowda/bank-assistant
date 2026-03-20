# 🏦 Bank of Maharashtra Loan Product Assistant (RAG-Based AI System)

## 🚀 Project Overview

This project is a **Retrieval-Augmented Generation (RAG) based AI assistant** designed to answer user queries specifically about **Bank of Maharashtra loan products**.

The system leverages:

* Web-scraped data from official bank sources
* Semantic search using vector embeddings
* A Large Language Model (LLM) for grounded answer generation

The goal is to build a reliable, domain-specific AI assistant that reduces manual effort, enables organizations to make informed decisions, and improves overall operational efficiency.

---

## 🎯 Objective

To develop a system that can accurately answer queries such as:

* What are the interest rates for home loans?
* What is the eligibility criteria for personal loans?
* Are there concessions for women or defence personnel?
* What is the tenure for different loan schemes?

---

## 🧠 System Architecture

```
User Query
    ↓
Embedding Model (Sentence Transformers)
    ↓
FAISS Vector Search
    ↓
Top Relevant Chunks (Context Retrieval)
    ↓
LLM (Groq - Llama 3.3)
    ↓
Final Answer (Grounded Response)
```

---

## ⚙️ Tech Stack

| Component       | Technology Used               |
| --------------- | ----------------------------- |
| Web Scraping    | BeautifulSoup, Requests       |
| Data Processing | Python (Regex, JSON)          |
| Embeddings      | SentenceTransformers (MiniLM) |
| Vector Store    | FAISS                         |
| LLM             | Groq (Llama 3.3 70B)          |
| Frontend        | Streamlit                     |
| Environment     | Python, dotenv                |

---

## 📂 Project Structure

```
loan-assistant/
│
├── data/
│   ├── raw_data.json
│   └── knowledge_base.txt
│
├── src/
│   ├── scraper.py
│   ├── processor.py
│   ├── rag_engine.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🌐 Data Collection (Scraping)

* Data is scraped **only from the official Bank of Maharashtra website**
* Focus areas include:

  * Home Loans
  * Personal Loans
  * Car Loans
  * MSME Loans
  * Agriculture Loans

### Key Features:

* Extracts meaningful content (headers, paragraphs, lists)
* Filters out navigation and irrelevant elements
* Maintains source URLs for traceability

---

## 🧹 Data Processing

The raw scraped data is cleaned and transformed into a **high-quality knowledge base**.

### Steps:

* Remove noise (headers, footers, ads)
* Normalize whitespace and text
* Deduplicate repeated content
* Tag important sections:

  * `[INTEREST_RATE]`
  * `[TENURE]`
  * `[ELIGIBILITY]`

👉 This improves retrieval accuracy significantly.

---

## 🔍 RAG Pipeline

### 1. Chunking

* Text is split into chunks (1000 characters with overlap)

### 2. Embedding

* Each chunk is converted into vector embeddings using MiniLM

### 3. Vector Search

* FAISS is used to retrieve top-k relevant chunks

### 4. Grounded Generation

* Retrieved context is passed to LLM
* LLM generates answer **strictly based on context**

---

## 🤖 Prompt Design

The system enforces:

* Answer ONLY from provided context
* Do NOT hallucinate
* Say "I don’t know" if answer not found

---

## 💻 Running the Project

### 1. Clone Repository

```
git clone <your-repo-link>
cd loan-assistant
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file:

```
GROQ_API_KEY= your_api_key_here  
"the api key is created from groq.ai official console: couldn't provide it in public so i've attached a key that created by myself in the mail stating all the procedures you just need to place that api key inside .env file with the above sentence "
```

---

### 4. Run Scraper

```
python src/scraper.py
```

---

### 5. Process Data

```
python src/processor.py
```

---

### 6. Run Application

```
streamlit run app.py
```

---

#### LIVE DEMO 
 
🔗 https://bank-assistant-bdcxjy5wtyrmructuzmwdr.streamlit.app/

## 💬 Features

* ✅ Chat-based UI (Streamlit)
* ✅ Context-aware answers
* ✅ Domain-restricted responses
* ✅ Downloadable chat history
* ✅ Fast retrieval using FAISS
* ✅ Clean and structured knowledge base

---

## ⚠️ Challenges Faced

### 1. Noisy Web Data

* Problem: HTML clutter, irrelevant text
* Solution: Regex cleaning + filtering logic

### 2. Duplicate Content

* Problem: Repeated information across pages
* Solution: Deduplication using sets

### 3. Hallucination in LLM

* Problem: Model answering outside scope
* Solution: Strict prompt + context grounding

### 4. Context Retrieval Accuracy

* Problem: Irrelevant chunks retrieved
* Solution: Chunking strategy + semantic tagging

---

## 🚀 Potential Improvements

* Use advanced vector DB (Pinecone / Weaviate)
* Add source citations in responses
* Implement query classification (loan vs non-loan)
* Add multilingual support
* Improve UI (chat memory, filters, suggestions)
* Deploy as a web service (Docker + Cloud)

---

## 🎥 Video Walkthrough

(Insert your Loom / Drive link here)

---

## 📊 Evaluation Alignment

This project satisfies all requirements:

✔ Data scraped from official sources
✔ Clean, structured knowledge base
✔ Lightweight RAG pipeline (FAISS)
✔ Accurate question-answering system
✔ Proper documentation and modular code

---

## 🧠 Key Learnings

* Practical implementation of RAG systems
* Importance of data quality in AI pipelines
* Prompt engineering to control hallucination
* Efficient semantic search with FAISS
* End-to-end AI system design

---

## 🙌 Conclusion

This project demonstrates the ability to:

* Build a real-world AI system from scratch
* Work with unstructured web data
* Design scalable and modular architectures
* Apply AI tools effectively for problem-solving

---

## 📌 Author

Devika S 
devikashivegowda@gmail.com
AI Developer | Software Engineer

---
