import streamlit as st
from gradio_client import Client, handle_file

# 1. Cấu hình trang web
st.set_page_config(
    page_title="AI Fashion Studio VIP",
    page_icon="👑",
    layout="wide"
)

# 2. Phông nền Studio Thời Trang 4K Sắc Nét + Kính Mờ Đẳng Cấp
st.markdown("""
    <style>
    /* Phông nền Runway Studio 4K cực nét */
    .stApp {
        background-image: linear-gradient(rgba(5, 5, 10, 0.65), rgba(5, 5, 10, 0.65)), 
                          url('https://images.unsplash.com/photo-1469334031218-e382a71b716b?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }

    /* Tiêu đề sang trọng */
    .title-box {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900;
        font-size: 3rem;
        background: linear-gradient(90deg, #ffffff, #ffd700, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-shadow: 0 5px 25px rgba(255, 0, 127, 0.3);
    }
    .sub-title {
        color: #f1f5f9;
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing: 1px;
    }

    /* Thẻ Glassmorphism siêu nét */
    div[data-testid="stColumn"] {
        background: rgba(15, 15, 25, 0.78);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.8);
    }

    /* Nút bấm Thử Đồ siêu nổi bật */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff007f 0%, #ff4b2b 100%);
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
        border-radius: 12px;
        padding: 16px;
        border: none;
        box-shadow: 0 5px 20px rgba(255, 0, 127, 0.6);
        transition: all 0.3s ease;
        text-transform: uppercase;
        margin-top: 15px;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 30px rgba(255, 0, 127, 0.9);
    }

    /* Nút Shopee Affiliate */
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
        box-shadow: 0 5px 20px rgba(238, 77, 45, 0.6);
        text-transform: uppercase;
        margin-top: 10px;
    }
    .shopee-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(238, 77, 45, 0.9);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="title-box">
        <div class="main-title">✨ AI FASHION STUDIO VIP ✨</div>
        <div class="sub-title">Tự Động Nhận Diện & Tách Ghép Trang Phục Chuẩn HD Siêu Tốc</div>
    </div>
""", unsafe_allow_html=True)

# 3. Khởi tạo AI Engine
@st.cache_resource
def get_ai_client():
    try:
        return Client("yisol/IDM-VTON")
    except Exception:
        return None

ai_client = get_ai_client()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📸 1. Dán / Tải Ảnh Cần Ghép")
    person_img = st.file_uploader("👤 1. Ảnh Người Mẫu Của Bạn (Kéo thả hoặc Ctrl+V)", type=["jpg", "png", "jpeg"])
    garment_img = st.file_uploader("👗 2. Ảnh Trang Phục / Ảnh Người Khác Đang Mặc Đồ Đó (Ctrl+V)", type=["jpg", "png", "jpeg"])
    
    btn_submit = st.button("🚀 THỬ ĐỒ NGAY (TỰ ĐỘNG AI HD)", type="primary")

with col2:
    st.markdown("### 🪄 2. Kết Quả Phối Đồ AI HD")
    if btn_submit:
        if not person_img or not garment_img:
            st.warning("⚠️ Vui lòng tải hoặc dán đủ 2 ảnh!")
        elif ai_client is None:
            st.error("❌ Máy chủ AI đang khởi tạo. Vui lòng bấm lại sau vài giây!")
        else:
            with st.spinner("⚡ AI đang tự động nhận diện & tách ghép đồ nét căng..."):
                # Lưu file trực tiếp chuẩn gốc 100% HD không nén
                with open("temp_person.png", "wb") as f:
                    f.write(person_img.getbuffer())
                with open("temp_garment.png", "wb") as f:
                    f.write(garment_img.getbuffer())
                
                try:
                    # AI tự động trích xuất outfit từ bất kỳ bức ảnh nào
                    result = ai_client.predict(
                        dict={"background": handle_file("temp_person.png"), "layers": [], "composite": None},
                        garm_img=handle_file("temp_garment.png"),
                        garment_des="fashion item, clothing, outfit, dress, bikini or shoes",
                        is_checked=True,
                        is_checked_crop=False,
                        denoise_steps=30,
                        seed=42,
                        api_name="/tryon"
                    )
                    st.image(result[0], caption="🎉 Ghép đồ thành công - Độ nét nguyên bản!", use_container_width=True)
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
