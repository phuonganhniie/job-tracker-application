"""
Job Tracker Application - Streamlit Frontend
Main entry point
"""
import streamlit as st
from frontend.config.settings import STATUS_COLORS

# Page configuration
st.set_page_config(
    page_title="Job Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Main page
def main():
    st.title("💼 Job Tracker Application")
    st.markdown("---")
    
    # Welcome message
    st.markdown("""
    ### Chào mừng đến với Job Tracker! 👋
    
    Ứng dụng giúp bạn quản lý toàn bộ quá trình ứng tuyển việc làm một cách có hệ thống:
    
    #### 📋 Chức năng chính:
    - **💼 Quản lý Jobs**: Theo dõi các công việc đã/đang ứng tuyển
    - **📊 Pipeline Tracking**: Theo dõi trạng thái từ Applied → Hired
    - **🎯 Lịch phỏng vấn**: Quản lý lịch phỏng vấn chi tiết
    - **📝 Ghi chú**: Lưu thông tin quan trọng cho từng job/interview
    - **📧 Email Templates**: Mẫu email follow-up, thank you...
    - **📈 Analytics**: Báo cáo thống kê chi tiết
    
    #### 🚀 Bắt đầu:
    Chọn một trang từ sidebar bên trái để bắt đầu!
    """)


if __name__ == "__main__":
    main()
