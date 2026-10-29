import time
import streamlit as st
from gradio_client import Client, handle_file

st.set_page_config(page_title="AI Fashion Studio", page_icon="👙", layout="wide")

st.title("👙 AI Fashion & Bikini Try-On Studio")
st.write("Thử đồ ảo chuẩn AI - Tải file hoặc dán ảnh chụp màn hình trực tiếp!")

@st.cache_resource
def get_ai_client():
    try:
        return Client("yisol/IDM-VTON")
    except Exception:
        return None

ai_client = get_ai_client()

col1, col2 = st.columns(2)

with col1:
    person_img = st.file_uploader("1. Ảnh Người mẫu (Kéo thả hoặc dán ảnh)", type=["jpg", "png", "jpeg"])
    garment_img = st.file_uploader("2. Ảnh Trang phục / Bikini (Kéo thả hoặc dán ảnh)", type=["jpg", "png", "jpeg"])
    category = st.selectbox("3. Nhóm trang phục", ["Bikini / Swimwear", "Topwear (Áo)", "Bottomwear (Quần/Váy)", "Full Outfit"])
    
    btn_submit = st.button("🚀 Thử Đồ Ngay (Xem 5s Quảng Cáo)", type="primary")

with col2:
    if btn_submit:
        if not person_img or not garment_img:
            st.warning("⚠️ Vui lòng tải hoặc dán đủ 2 ảnh!")
        elif ai_client is None:
            st.error("❌ Máy chủ AI hiện chưa sẵn sàng. Vui lòng thử lại sau!")
        else:
            with st.spinner("⏳ Đang xử lý... (Vui lòng chờ 5 giây quảng cáo)"):
                time.sleep(5)
                
                with open("temp_person.png", "wb") as f:
                    f.write(person_img.getbuffer())
                with open("temp_garment.png", "wb") as f:
                    f.write(garment_img.getbuffer())
                
                try:
                    result = ai_client.predict(
                        dict={"background": handle_file("temp_person.png"), "layers": [], "composite": None},
                        garm_img=handle_file("temp_garment.png"),
                        garment_des=f"A fashion item: {category}",
                        is_checked=True,
                        is_checked_crop=False,
                        denoise_steps=30,
                        seed=42,
                        api_name="/tryon"
                    )
                    st.image(result[0], caption="🎉 Kết quả phối đồ AI thành công!")
                except Exception as e:
                    st.error(f"❌ Lỗi xử lý AI: {e}")

    st.markdown("---")
    st.markdown("### 🛍️ Bạn thích bộ trang phục này?")
    st.markdown(
        '<a href="https://shopee.vn" target="_blank">'
        '<button style="width:100%; padding:10px; background:#ee4d2d; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">'
        '🛒 Tìm mua mẫu này trên Shopee (Nhận Ưu Đãi)'
        '</button></a>',
        unsafe_allow_html=True
    )
