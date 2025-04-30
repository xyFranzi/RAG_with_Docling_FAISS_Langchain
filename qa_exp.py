from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
INDEX_PATH = "./faiss_index"

embeddings = OpenAIEmbeddings(api_key=api_key)
db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

retriever = db.as_retriever()
llm = ChatOpenAI(api_key=api_key)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# query = "Kern themen der FG Siedlungswasserwirtschaft?"
query = "How does the number of assignments per female and male professionals compare?"
answer = qa.invoke({"query": query})
print(answer["result"])

