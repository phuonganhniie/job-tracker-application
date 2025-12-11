"""
Job Tracker Application - Streamlit Frontend
Main entry point
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from frontend.config.settings import STATUS_COLORS
from frontend.components.sidebar_navigation import apply_sidebar_navigation_css

# Page configuration
st.set_page_config(
    page_title="Job Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply sidebar navigation CSS
apply_sidebar_navigation_css()

# Custom CSS with Inter font and responsive design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'San Francisco', sans-serif;
    }
    
    .main > div {
        padding-top: 2rem;
    }
    .stApp {
        max-width: 100%;
    }
    
    .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Better text rendering */
    body {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.02em;
    }
    
    /* Hero section styling */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 900;
        color: white;
        margin: 0;
        letter-spacing: -2px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 20px;
        color: rgba(255,255,255,0.95);
        margin-top: 1rem;
        font-weight: 500;
    }
    
    /* Feature card styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 32px;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .feature-desc {
        font-size: 14px;
        color: #6b7280;
        line-height: 1.6;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
    }
    
    .stats-number {
        font-size: 36px;
        font-weight: 900;
        margin: 0;
    }
    
    .stats-label {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .hero-title {
            font-size: 32px;
        }
        
        .hero-subtitle {
            font-size: 16px;
        }
        
        .hero-section {
            padding: 2rem 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Main page
def main():
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <h1 class='hero-title'>💼 Job Tracker Application</h1>
        <p class='hero-subtitle'>
            Quản lý toàn bộ hành trình tìm việc của bạn một cách chuyên nghiệp và hiệu quả
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats (if needed later, can fetch from API)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='stats-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <div class='stats-number'>∞</div>
            <div class='stats-label'>Công việc theo dõi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stats-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <div class='stats-number'>⚡</div>
            <div class='stats-label'>Quản lý nhanh chóng</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stats-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <div class='stats-number'>📊</div>
            <div class='stats-label'>Phân tích chi tiết</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='stats-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
            <div class='stats-number'>🎯</div>
            <div class='stats-label'>Đạt mục tiêu</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features section
    st.markdown("""
    <h2 style='font-size: 32px; font-weight: 800; color: #111827; 
               margin-bottom: 25px; letter-spacing: -1px;'>
        ✨ Tính năng nổi bật
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💼</div>
            <div class='feature-title'>Quản lý Jobs</div>
            <div class='feature-desc'>
                Theo dõi tất cả các công việc đã và đang ứng tuyển với thông tin chi tiết: 
                công ty, vị trí, mức lương, nguồn tuyển dụng, deadline...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card' style='border-left-color: #f093fb;'>
            <div class='feature-icon'>📊</div>
            <div class='feature-title'>Pipeline Tracking</div>
            <div class='feature-desc'>
                Theo dõi trạng thái ứng tuyển qua từng giai đoạn: Applied → Screening → 
                Interview → Offer → Hired. Biết rõ công việc đang ở đâu.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card' style='border-left-color: #4facfe;'>
            <div class='feature-icon'>🎯</div>
            <div class='feature-title'>Lịch phỏng vấn</div>
            <div class='feature-desc'>
                Quản lý lịch phỏng vấn chi tiết với thời gian, địa điểm, link meeting, 
                người phỏng vấn và ghi chú chuẩn bị.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='border-left-color: #f59e0b;'>
            <div class='feature-icon'>📧</div>
            <div class='feature-title'>Email Templates</div>
            <div class='feature-desc'>
                Mẫu email có sẵn cho thank you letter, follow-up, negotiation, acceptance. 
                Tiết kiệm thời gian và chuyên nghiệp hơn.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card' style='border-left-color: #8b5cf6;'>
            <div class='feature-icon'>📈</div>
            <div class='feature-title'>Analytics & Reports</div>
            <div class='feature-desc'>
                Báo cáo thống kê chi tiết: tỷ lệ thành công, xu hướng theo thời gian, 
                phân tích theo nguồn tuyển dụng và trạng thái.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Getting started section
    st.markdown("""
    <h2 style='font-size: 32px; font-weight: 800; color: #111827; 
               margin-bottom: 25px; letter-spacing: -1px;'>
        🚀 Bắt đầu sử dụng
    </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%); 
                padding: 2rem; border-radius: 16px; border-left: 5px solid #667eea;'>
        <h3 style='color: #4338ca; margin-top: 0; font-size: 20px; font-weight: 700;'>
            📍 Hướng dẫn nhanh:
        </h3>
        <ol style='color: #4b5563; line-height: 2; margin: 1rem 0;'>
            <li><strong>Dashboard (🏠)</strong>: Xem tổng quan và thống kê nhanh</li>
            <li><strong>Jobs (💼)</strong>: Thêm công việc mới hoặc quản lý các job hiện có</li>
            <li><strong>Applications (📝)</strong>: Theo dõi chi tiết từng đơn ứng tuyển</li>
            <li><strong>Interviews (🎯)</strong>: Quản lý lịch phỏng vấn và ghi chú</li>
            <li><strong>Notes (📋)</strong>: Lưu trữ thông tin quan trọng</li>
            <li><strong>Email Templates (📧)</strong>: Sử dụng mẫu email có sẵn</li>
        </ol>
        <p style='color: #6b7280; font-size: 14px; margin-bottom: 0;'>
            💡 <em>Mẹo: Bắt đầu bằng cách thêm một công việc mới từ trang Jobs, 
            sau đó cập nhật trạng thái khi có tiến triển!</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
