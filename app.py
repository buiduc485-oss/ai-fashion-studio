import time
import streamlit as st
from gradio_client import Client, handle_file

# 1. Cấu hình trang web
st.set_page_config(
    page_title="AI Fashion Studio - Studio Thử Đồ AI HD",
    page_icon="👗",
    layout="wide"
)

# 2. Phông nền Ảnh Studio Thời Trang Cao Cấp (Luxury Runway Background)
st.markdown("""
    <style>
    /* Phông nền ảnh thời trang Runway / Studio chuẩn HD */
    .stApp {
        background-image: linear-gradient(rgba(10, 10, 15, 0.75), rgba(10, 10, 15, 0.75)), 
                          url('https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }

    /* Tiêu đề sang trọng */
    .title-box {
        text-align: center;
        padding: 15px 0 10px 0;
    }
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #ffffff, #ffd700, #ff758c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Khung Glassmorphic kính mờ độ nét cao */
    div[data-testid="stColumn"] {
        background: rgba(18, 18, 28, 0.70);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7);
    }

    /* Nút bấm Thử đồ */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: #ffffff;
        font-size: 18px;
        font-weight: 800;
        border-radius: 10px;
        padding: 14px 20px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 75, 43, 0.8);
    }

    /* Nút Shopee Affiliate */
    .shopee-btn {
        display: block;
        width: 100%;
        text-align: center;
        padding: 15px;
        background: linear-gradient(90deg, #ee4d2d, #ff7337);
        color: #ffffff !important;
        text-decoration: none;
        font-size: 17px;
        font-weight: 800;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(238, 77, 45, 0.6);
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="title-box">
        <div class="main-title">✨ AI FASHION STUDIO VIP ✨</div>
        <div class="sub-title">Thử Đồ Ảo Chuẩn HD — Giữ Nguyên Độ Sắc Nét 100%</div>
    </div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_ai_client():
    try:
        return Client("yisol/IDM-VTON")
    except Exception:
        return None

ai_client = get_ai_client()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📸 1. Tải Hoặc Dán Ảnh Gốc (HD)")
    person_img = st.file_uploader("👤 Ảnh Người Mẫu (Chất lượng cao)", type=["jpg", "png", "jpeg"])
    garment_img = st.file_uploader("👗 Ảnh Trang Phục / Phụ Kiện", type=["jpg", "png", "jpeg"])
    
    st.markdown("### 🏷️ 2. Chọn Nhóm Trang Phục")
    category = st.selectbox(
        "Loại trang phục:",
        [
            "Topwear (Áo, Sơ mi, Blazer, Áo phông)",
            "Bottomwear (Quần, Váy, Quần short)",
            "Full Outfit (Đầm dạ hội, Bộ suit, Trang phục trọn bộ)",
            "Swimwear / Beachwear (Bikini & Đồ đi biển)",
            "Accessories & Shoes (Giày dép, Phụ kiện)"
        ]
    )
    
    btn_submit = st.button("🚀 THỬ ĐỒ NGAY (SIÊU SẮC NÉT)", type="primary")

with col2:
    st.markdown("### 🪄 3. Kết Quả Phối Đồ AI HD")
    if btn_submit:
        if not person_img or not garment_img:
            st.warning("⚠️ Vui lòng tải hoặc dán đủ 2 ảnh!")
        elif ai_client is None:
            st.error("❌ Máy chủ AI đang bận, vui lòng thử lại sau vài giây!")
        else:
            with st.spinner("⏳ Đang xử lý ở độ phân giải gốc HD..."):
                time.sleep(1)
                
                # Giữ nguyên 100% file gốc không nén để đảm bảo nét căng
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
                    st.image(result[0], caption="🎉 Kết quả xử lý độ phân giải HD nét căng!", use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Lỗi xử lý AI: {e}")

    st.markdown("---")
    st.markdown("### 🛒 Mua Ngay Mẫu Này")
    st.markdown(
        '<a href="https://shopee.vn" target="_blank" class="shopee-btn">'
        '🛒 Tìm Mua Ngay Trên Shopee (Nhận Ưu Đãi)'
        '</a>',
        unsafe_allow_html=True
    )
