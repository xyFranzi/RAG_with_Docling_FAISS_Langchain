import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# ========== 初始化 ==========
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
INDEX_PATH = "./faiss_index"

# 加载向量数据库
embeddings = OpenAIEmbeddings(api_key=api_key)
db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever()
llm = ChatOpenAI(api_key=api_key)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# ========== 页面设置 ==========
st.set_page_config(page_title="RAG Chatbot", page_icon="💬", layout="wide")
st.title("RAG Assistant here!")

# ========== 聊天状态管理 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 显示历史消息 ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========== 用户输入 ==========
if prompt := st.chat_input("pls enter your question here..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 查询 RAG 系统
    with st.chat_message("assistant"):
        with st.spinner("thinking..."):
            result = qa.invoke({"query": prompt})
            response = result["result"]
            st.markdown(response)

    # 保存助手回复
    st.session_state.messages.append({"role": "assistant", "content": response})
