from pathlib import Path
from functools import lru_cache

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


DATA_DIR = Path(__file__).parent / "data"
SOP_FILE = DATA_DIR / "sales_sop.txt"


@lru_cache(maxsize=1)
def create_vector_store():
    if not SOP_FILE.exists():
        raise FileNotFoundError(f"SOP file not found: {SOP_FILE}")

    # Simple keyword-based retrieval: no local Ollama needed.
    documents = TextLoader(
        str(SOP_FILE), encoding="utf-8"
    ).load()

    return documents


def search_sop(question: str) -> str:
    try:
        documents = create_vector_store()
        text = "\n".join(doc.page_content for doc in documents)
        q = question.lower()

        # Match questions to relevant policy terms.
        keywords = {
            "return": ["return", "refund", "damaged", "product"],
            "refund": ["return", "refund", "damaged", "approved"],
            "damaged": ["damaged", "48 hours", "report"],
        }

        terms = set()
        for key, values in keywords.items():
            if key in q:
                terms.update(values)

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        matches = [
            line for line in lines
            if any(term in line.lower() for term in terms)
        ]

        if matches:
            return "Information from Sales SOP:\n" + "\n".join(matches)

        return "This information is not available in the provided SOP."

    except Exception as error:
        return f"SOP search failed: {error}"