# 🔍 RAG-based Plagiarism Explanation Helper

**RAG-based Plagiarism Explanation Helper** คือเว็บแอปพลิเคชันที่ใช้เทคโนโลยี AI ขั้นสูงในการตรวจจับและวิเคราะห์การคัดลอกผลงาน (Plagiarism) โดยไม่ได้ทำแค่การเปรียบเทียบคำต่อคำ แต่ใช้กระบวนการ **RAG (Retrieval-Augmented Generation)** เพื่อทำความเข้าใจบริบทและ "อธิบาย" เหตุผลเชิงลึกว่าทำไมข้อความนั้นถึงเข้าข่ายการคัดลอก พร้อมให้คำแนะนำในการเขียนใหม่ (Paraphrasing)

---

## 🚀 การทำงานของระบบ (Workflow)

ระบบทำงานผ่าน 4 ขั้นตอนหลัก ดังนี้:

1.  **Data Ingestion**: ผู้ใช้อัปโหลดเอกสารอ้างอิง (Reference PDF) ระบบจะทำการอ่านไฟล์และตัดแบ่งข้อความออกเป็นส่วนย่อยๆ (Text Chunking)
2.  **Vector Embedding**: ข้อความที่ถูกตัดแบ่งจะถูกแปลงเป็นค่าเวกเตอร์ทางคณิตศาสตร์ด้วยโมเดล `all-MiniLM-L6-v2` และจัดเก็บลงในฐานข้อมูลเวกเตอร์ (ChromaDB)
3.  **Context Retrieval**: เมื่อผู้ใช้วางข้อความที่ต้องการตรวจ ระบบจะคำนวณความคล้ายคลึงและดึงเฉพาะส่วนที่เกี่ยวข้องที่สุดจากฐานข้อมูลออกมา
4.  **AI Analysis & Explanation**: ระบบส่งข้อความที่ตรวจพร้อมบริบทที่ดึงมาได้ไปให้ **Google Gemini 1.5 Flash** เพื่อวิเคราะห์และร่างคำอธิบายเป็นภาษาไทยที่เข้าใจง่าย



---

## 🛠️ เครื่องมือและเทคโนโลยีที่ใช้ (Tech Stack)

### **Languages & Frameworks**
* **Python 3.14**: ภาษาหลักที่ใช้ในการพัฒนาเนื่องจากมี Library ด้าน AI ที่แข็งแกร่ง
* **Streamlit**: ใช้สร้างส่วนติดต่อผู้ใช้ (User Interface) แบบ Web-based ที่รวดเร็วและสวยงาม

### **AI & Machine Learning (Orchestration)**
* **LangChain**: เฟรมเวิร์กหลักที่ใช้จัดการ "Chains" ของการทำงาน ตั้งแต่การดึงข้อมูลจนถึงการสร้างคำตอบ
* **Google Gemini API (Gemini 1.5 Flash)**: โมเดลภาษาขนาดใหญ่ (LLM) ที่ใช้ในการวิเคราะห์และให้เหตุผล
* **HuggingFace (Sentence-Transformers)**: ใช้สำหรับสร้าง Local Embeddings เพื่อความรวดเร็วและประหยัดโควตา API

### **Data Management**
* **ChromaDB**: ฐานข้อมูลเวกเตอร์แบบ Open-source สำหรับจัดเก็บและค้นหาข้อความที่มีความหมายใกล้เคียงกัน
* **PyPDF**: Library สำหรับการดึงข้อมูลข้อความจากไฟล์เอกสาร PDF

---

## 📂 โครงสร้างโปรเจค (Project Structure)

```text
rag-plagiarism-helper/
├── app.py              # ไฟล์หลักของโปรแกรม (UI + Logic)
├── requirements.txt    # รายการ Library ที่ต้องติดตั้ง
├── README.md           # คำอธิบายโปรเจค (ไฟล์นี้)
└── temp_ref.pdf        # ไฟล์ชั่วคราวขณะประมวลผล (Auto-generated)
```

---

## ⚙️ วิธีการติดตั้ง (Installation)

1. **Clone หรือ Copy โฟลเดอร์โปรเจค**
2. **สร้าง Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **ติดตั้ง Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **รันโปรแกรม:**
   ```bash
   streamlit run app.py
   ```

---

## 📝 หมายเหตุการพัฒนา
โปรเจคนี้ได้รับการออกแบบให้เป็น **Hybrid RAG** เพื่อแก้ไขปัญหาเรื่อง API Limit โดยการทำ Embedding ภายในเครื่องของผู้ใช้เอง (Local) และใช้ Cloud LLM เฉพาะขั้นตอนการวิเคราะห์ขั้นสูงเท่านั้น
