import time
import io
from PIL import Image
import streamlit as st
from gradio_client import Client, handle_file

# 1. Cấu hình giao diện web
st.set_page_config(
    page_title="AI Fashion Studio - Đỉnh Cao Thời Trang AI",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Phông nền sinh động, đẳng cấp & sang trọng
st.markdown("""
    <style>
    /* Phông nền Gradient thời trang cao cấp */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }

    /* Tiêu đề chính hiệu ứng chuyển màu rực rỡ */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #ff007f, #00f2fe);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 6s ease infinite;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 0.2rem;
        text-shadow: 0px 4px 20px rgba(229, 46, 113, 0.4);
    }

    .sub-title {
        text-align: center;
        color: #e0e7ff;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* Khung thẻ hiệu ứng kính mờ Glassmorphism */
    div[data-testid="stColumn"] {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* Nút bấm Thử Đồ siêu nổi bật & hào hoa */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        font-size: 19px;
        font-weight: 800;
        border-radius: 12px;
        padding: 14px 28px;
        border: none;
        box-shadow: 0 4px 20px rgba(255, 75, 43, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 8px 30px rgba(255, 75, 43, 0.8);
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%);
    }

    /* Custom chữ và nhãn */
    .stSelectbox label, .stFileUploader label {
        color: #ffffff !important;
        font-weight: 700;
        font-size: 15px;
    }

    /* Nút Shopee Affiliate bùng nổ */
    .shopee-btn {
        display: block;
        width: 100%;
        text-align: center;
        padding: 16px;
        background: linear-gradient(90deg, #ee4d2d, #ff7337);
        color: #ffffff !important;
        text-decoration: none;
        font-size: 18px;
        font-weight: 800;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(238, 77, 45, 0.6);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .shopee-btn:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(238, 77, 45, 0.9);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header sinh động
st.markdown('<div class="main-title">🔥 AI FASHION STUDIO VIP 🔥</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Thử Đồ Ảo Chuẩn AI HD — Sang Trọng • Lịch Lãm • Tuổi Teen • Bikini • Giày Dép</div>', unsafe_allow_html=True)

# 4. Kết nối API AI
@st.cache_resource
def get_ai_client():
    try:
        return Client("yisol/IDM-VTON")
    except Exception:
        return None

ai_client = get_ai_client()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📸 1. Tải Hoặc Dán Ảnh Trực Tiếp")
    person_img = st.file_uploader("👤 Ảnh Người Mẫu (Kéo thả hoặc Ctrl+V)", type=["jpg", "png", "jpeg"])
    garment_img = st.file_uploader("👗 Ảnh Trang Phục / Phụ Kiện (Kéo thả hoặc Ctrl+V)", type=["jpg", "png", "jpeg"])
    
    st.markdown("#### 🏷️ 2. Chọn Phong Cách Đa Dạng")
    category = st.selectbox(
        "Nhóm sản phẩm cần phối:",
        [
            "✨ Sang Trọng & Quý Phái (Dạ Hội, Đầm Sự Kiện)",
            "👔 Lịch Lãm & Bảnh Bao (Suit, Vest, Sơ Mi)",
            "🔥 Phong Cách Tuổi Teen & Streetwear (Năng Động)",
            "🏖️ Đồ Đi Biển & Bikini / Swimwear",
            "👠 Giày Dép, Guốc & Phụ Kiện Thời Trang",
            "👕 Thời Trang Thường Ngày (Casual Outfit)"
        ]
    )
    
    btn_submit = st.button("🚀 THỬ ĐỒ NGAY (SIÊU TỐC AI)", type="primary")

with col2:
    st.markdown("#### 🪄 3. Kết Quả Phối Đồ AI Sắc Nét")
    if btn_submit:
        if not person_img or not garment_img:
            st.warning("⚠️ Vui lòng tải hoặc dán đủ 2 ảnh người mẫu và trang phục!")
        elif ai_client is None:
            st.error("❌ Máy chủ AI đang khởi tạo. Vui lòng thử lại sau vài giây!")
        else:
            with st.spinner("⚡ AI đang tối ưu hình ảnh & phối đồ siêu tốc..."):
                # Tự động nén tối ưu dung lượng giúp AI chạy nhanh gấp đôi
                p_img = Image.open(person_img).convert("RGB")
                g_img = Image.open(garment_img).convert("RGB")
                
                p_img.save("temp_person.png", "PNG", optimize=True)
                g_img.save("temp_garment.png", "PNG", optimize=True)
                
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
                    st.image(result[0], caption="🎉 Kết quả phối đồ AI thành công!", use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Lỗi xử lý AI: {e}")

    st.markdown("---")
    st.markdown("### 🛒 Sắm Ngay Mẫu Này")
    st.markdown(
        '<a href="https://shopee.vn" target="_blank" class="shopee-btn">'
        '💥 Mua Ngay Sản Phẩm Trên Shopee (Nhận Ưu Đãi) 💥'
        '</a>',
        unsafe_allow_html=True
    )
