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
    
    # Quick stats
    st.markdown("---")
    st.subheader("📊 Thống kê nhanh")
    
    try:
        from frontend.services.analytics_service import analytics_service
        summary = analytics_service.get_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Tổng số đơn",
                value=summary.get("total_applications", 0)
            )
        
        with col2:
            st.metric(
                label="Đang xử lý",
                value=summary.get("active_applications", 0)
            )
        
        with col3:
            st.metric(
                label="Phỏng vấn sắp tới",
                value=summary.get("upcoming_interviews", 0)
            )
        
        with col4:
            st.metric(
                label="Tỷ lệ thành công",
                value=f"{summary.get('success_rate', 0):.1f}%"
            )
    
    except Exception as e:
        st.warning("⚠️ Không thể kết nối với backend API. Vui lòng đảm bảo server đang chạy!")
        st.code(f"Error: {str(e)}")
        st.info("👉 Chạy backend bằng lệnh: `cd backend && uvicorn main:app --reload`")
    
    # Status legend
    st.markdown("---")
    st.subheader("📌 Trạng thái Pipeline")
    
    cols = st.columns(len(STATUS_COLORS))
    for idx, (status, icon) in enumerate(STATUS_COLORS.items()):
        with cols[idx]:
            st.markdown(f"{icon} **{status}**")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Job Tracker Application v1.0.0 | Built with FastAPI + Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
