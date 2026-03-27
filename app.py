import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="RAG Plagiarism Helper", layout="wide")
st.title("🔍 RAG-based Plagiarism Explanation Helper")
st.caption("Hybrid RAG: Local Embeddings + Google Gemini Analysis")

# --- 2. Sidebar สำหรับ API Key ---
with st.sidebar:
    st.header("⚙️ การตั้งค่า")
    google_api_key = st.text_input("ใส่ Google Gemini API Key ของคุณ", type="password")
    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key
    else:
        st.warning("⚠️ กรุณาใส่ API Key เพื่อเริ่มใช้งาน")

# --- 3. ส่วนการอัปโหลดเอกสารอ้างอิง ---
st.subheader("📁 1. เตรียมฐานข้อมูลอ้างอิง (Reference)")
ref_file = st.file_uploader("อัปโหลดไฟล์ PDF ต้นฉบับ", type="pdf")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if ref_file and google_api_key:
    if st.button("ประมวลผลเอกสาร"):
        try:
            with st.spinner('กำลังประมวลผลฐานข้อมูล (ขั้นตอนนี้รันในเครื่องคุณ)...'):
                # บันทึกไฟล์ชั่วคราว
                with open("temp_ref.pdf", "wb") as f:
                    f.write(ref_file.getbuffer())
                
                # โหลดและตัดแบ่งข้อความ
                loader = PyPDFLoader("temp_ref.pdf")
                docs = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
                splits = text_splitter.split_documents(docs)
                
                # ใช้ Local Embeddings (ไม่พึ่งพา API ทำให้ไม่เกิด Error 404)
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                
                st.session_state.vectorstore = Chroma.from_documents(
                    documents=splits, 
                    embedding=embeddings
                )
                st.success("✅ โหลดข้อมูลสำเร็จ! AI พร้อมเปรียบเทียบแล้ว")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {str(e)}")

# --- 4. ส่วนการวิเคราะห์ ---
st.divider()
st.subheader("📝 2. ตรวจสอบข้อความ")
query_text = st.text_area("วางข้อความที่ต้องการตรวจสอบ:")

if st.button("วิเคราะห์ Plagiarism"):
    if st.session_state.vectorstore is not None and query_text:
        with st.spinner('Gemini กำลังวิเคราะห์ผลลัพธ์...'):
            try:
                retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
                
                template = """คุณคือผู้เชี่ยวชาญด้านการตรวจสอบการคัดลอกผลงาน (Plagiarism Expert)
                เปรียบเทียบ 'ข้อความที่ตรวจ' กับ 'บริบท' ต่อไปนี้:
                
                {context}
                
                ข้อความที่ตรวจ: {question}
                
                หากพบว่ามีการคัดลอก:
                1. ระบุประโยคที่คล้ายกัน
                2. อธิบายเหตุผล (ลอกมาตรงๆ หรือดัดแปลงเล็กน้อย)
                3. แนะนำวิธีเขียนใหม่ (Paraphrase) ให้เป็นตัวเอง
                
                ตอบเป็นภาษาไทยให้ละเอียดและสุภาพ
                """
                prompt = ChatPromptTemplate.from_template(template)
                
                # เรียกใช้ Gemini เฉพาะตอนวิเคราะห์ (โอกาส Error ต่ำมาก)
                model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
                def format_docs(docs):
                    return "\n\n".join(doc.page_content for doc in docs)

                rag_chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough()}
                    | prompt
                    | model
                    | StrOutputParser()
                )

                response = rag_chain.invoke(query_text)
                st.markdown("### 📊 ผลการวิเคราะห์")
                st.info(response)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("กรุณาเตรียมฐานข้อมูลและใส่ข้อความก่อน")