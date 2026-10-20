METRO — Agentic AI Sales Assistant

An AI-powered sales intelligence assistant that answers business questions using sales data and Standard Operating Procedure (SOP) documents.

Project Overview

METRO helps users analyse sales performance and retrieve policy information through a conversational AI interface. It combines data-analysis tools with Retrieval-Augmented Generation (RAG) to provide useful answers from structured sales data and unstructured SOP documents.

Key Features

- Sales Analytics: Analyse total sales and product performance.
- Regional Insights: Explore sales across different regions.
- Conversational AI: Ask business questions in natural language.
- RAG-Based SOP Search: Retrieve information from sales policy documents.
- Interactive Dashboard: Visualise sales metrics and charts.
- Chat History: View previous messages during the session.
- Cloud Deployment: Access the application through Streamlit Cloud.

Technology Stack

- Python
- Streamlit
- LangGraph
- LangChain
- Groq API
- FAISS
- Pandas
- GitHub
- Streamlit Community Cloud

Architecture

1. The user submits a question through the Streamlit interface.
2. The LangGraph agent processes the question and determines the appropriate action.
3. Sales-related questions use Python tools to analyse the sales CSV file.
4. SOP-related questions retrieve relevant information from the SOP knowledge base using RAG.
5. The agent generates a response using the configured language model.
6. The application displays the answer and sales analytics in the dashboard.

Project Structure

agentic-ai-sales-assistant/
├── app.py
├── agent.py
├── tools.py
├── rag.py
├── data/
│   ├── sales_data.csv
│   └── sales_sop.txt
├── requirements.txt
├── README.md
└── .gitignore

Run Locally

1. Clone the repository:
   
   "git clone https://github.com/Ajinkya566/agentic-ai-sales-assistant.git"

2. Open the project directory:
   
   "cd agentic-ai-sales-assistant"

3. Install dependencies:
   
   "pip install -r requirements.txt"

4. Configure the required API key in your local environment or Streamlit secrets.

5. Start the application:
   
   "streamlit run app.py"

Example Questions

- What are the total sales?
- Which product has the highest sales?
- What is the return period for a product?
- What is the return policy for damaged products?

Testing

The application was manually tested for:

- Total sales queries
- Highest-sales product queries
- SOP return-policy queries

Results should be revalidated whenever the code, data, model, or deployment configuration changes.

Security Notes

- Never commit API keys or secrets to GitHub.
- Keep ".env" out of version control.
- Configure deployment secrets in Streamlit Community Cloud.

Disclaimer

This is a demonstration project using sample sales data and SOP documents. Business results depend on the configured dataset and knowledge base.