# 🕵️ AuditGraph: Autonomous Corporate Due Diligence Agent

**Author:**  Venkata Narendra Nuka

AuditGraph is an advanced **Agentic GraphRAG (Retrieval-Augmented Generation)** system designed to automate forensic accounting and corporate due diligence.

It combines **unstructured financial data** (PDF contracts, 10-K reports, internal emails) with a **Neo4j Knowledge Graph** to detect complex fraud patterns such as:

* Related-party transactions
* Shell company fund transfers
* Hidden ownership structures

---

## 🚀 Key Features

### 🔗 Multi-Modal GraphRAG Architecture

* Goes beyond vector search by modeling **explicit relationships**
* Tracks:

  * Ownership structures
  * Board memberships
  * Financial transfers
* Enables **multi-hop reasoning across disconnected datasets**

---

### 🧠 Cognitive Data Engineering

* Uses **Gemini (`gemini-flash-latest`)** for intelligent parsing
* Processes complex PDFs via `pypdf`
* Converts raw text → structured **JSON ontology**

---

### 🛡️ Robust Extraction Pipeline

* Handles inconsistent LLM outputs safely
* Uses:

  * AST parsing
  * Regex fallback mechanisms
* Ensures **zero pipeline breakage during ingestion**

---

### 🔍 Automated Forensic Analysis

* Cypher-based inference engine
* Detects:

  * Undisclosed liabilities
  * Conflicts of interest
* Cross-references entities across the graph

---

### 📊 Interactive Dashboard

* Built with **Streamlit**
* Features:

  * Real-time graph visualization
  * One-click fraud detection
  * Analyst-friendly UI

---

## 🛠️ Technology Stack

| Category          | Tools Used               |
| ----------------- | ------------------------ |
| Language          | Python 3.x               |
| Graph Database    | Neo4j                    |
| LLM Orchestration | LangChain, Google Gemini |
| Data Processing   | PyPDF                    |
| Frontend          | Streamlit                |

---

## 📂 Project Structure

```text
AuditGraph/
│
├── app/
│   └── ui.py                  # Streamlit Dashboard UI
│
├── data/
│   └── raw/
│       ├── contracts/
│       ├── financials/
│       └── internal/
│
├── src/
│   ├── graph/
│   │   ├── builder.py
│   │   └── neo4j_client.py
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   └── parser.py
│   │
│   └── config.py
│
├── tests/
├── .env
├── main.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/AuditGraph.git
cd AuditGraph
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Mac/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Neo4j

* Install **Neo4j Desktop**
* Create a new DB (e.g., `AuditGraphDB`)
* Start the database

---

### 5️⃣ Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

---

## 🏃 Running the System

### ▶️ Step 1: Ingest Documents

1. Add PDFs into:

```
data/raw/
```

2. Run:

```bash
python main.py
```

This will:

* Parse documents
* Extract entities via LLM
* Build the Neo4j graph

---

### 📊 Step 2: Launch Dashboard

```bash
streamlit run app/ui.py
```

Open:

```
http://localhost:8501
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🧠 Use Cases

* Corporate due diligence
* Fraud detection
* Financial investigations
* Risk analysis

---

## ⚠️ Notes

* Ensure Neo4j is running before ingestion
* Keep `.env` file private (already git-ignored)
* Large PDFs may increase processing time

---

## 📌 Future Improvements

* Add real-time streaming ingestion
* Enhance graph visualization (D3.js integration)
* Deploy as a cloud-based SaaS

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📜 License

MIT License

---

⭐ If you found this project useful, consider starring the repo!
