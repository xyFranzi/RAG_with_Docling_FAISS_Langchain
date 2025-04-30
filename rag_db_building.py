import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


DOC_PATH = "./test_result" # output path of docling
INDEX_PATH = "./faiss_index"


def load_documents_from_docling_json(path):
    docs = []
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            full_path = os.path.join(path, fname)
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                text_segments = []
                for t in data.get("texts", []):
                    segment = t.get("text", "").strip()
                    if segment:
                        text_segments.append(segment)
                full_text = "\n".join(text_segments)
                if full_text.strip():
                    docs.append(Document(page_content=full_text, metadata={"source": fname}))
    return docs


# chunking
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


# embed and build FAISS index
def build_vector_store():
    print("Loading documents...")
    raw_docs = load_documents_from_docling_json(DOC_PATH)

    print(f"Loaded {len(raw_docs)} documents")

    print("Splitting documents...")
    split_docs = split_documents(raw_docs)

    print(f"Split into {len(split_docs)} chunks") # 看看长度
    if not split_docs:
        print(" --- No text chunks found. --- ")
        return

    print("Embedding documents...")
    embeddings = OpenAIEmbeddings(api_key = api_key)
    db = FAISS.from_documents(split_docs, embeddings)

    print("Saving index to disk...")
    db.save_local(INDEX_PATH)
    print(f"Index saved at {INDEX_PATH}")


if __name__ == "__main__":
    build_vector_store()
