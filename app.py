import streamlit as st
from rapidocr_onnxruntime import RapidOCR
import tempfile
import os

# កំណត់ចំណងជើងវេបសាយ
st.set_page_config(page_title="OCR App", layout="centered")
st.title("កម្មវិធីអានអក្សរពីរូបភាព (Rapid OCR)")

# ទាញយកម៉ូដែល OCR (ប្រើ Cache ដើម្បីឱ្យដំណើរការលឿន)
@st.cache_resource
def load_model():
    return RapidOCR()
    
engine = load_model()

# ប្រអប់សម្រាប់បញ្ចូលរូបភាព
uploaded_file = st.file_uploader("សូមជ្រើសរើសរូបភាព", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="រូបភាពដែលបានបញ្ចូល", use_column_width=True)
    
    if st.button("ចាប់ផ្តើមអានអត្ថបទ"):
        with st.spinner("កំពុងដំណើរការ..."):
            # បង្កើតឯកសាររូបភាពបណ្តោះអាសន្ន
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # អានអត្ថបទ
            result, _ = engine(tmp_path)
            os.remove(tmp_path) # លុបឯកសារបណ្តោះអាសន្នវិញ
            
            # បង្ហាញលទ្ធផល
            if result:
                st.success("លទ្ធផលអត្ថបទ៖")
                for item in result:
                    st.write(item[1])
            else:
                st.warning("រកមិនឃើញអត្ថបទក្នុងរូបភាពនេះទេ ឬរូបភាពមិនច្បាស់។")