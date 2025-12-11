"""
Dashboard Page - Overview and quick stats
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from frontend.services.analytics_service import analytics_service
from frontend.config.settings import STATUS_COLORS
from frontend.components.sidebar_navigation import apply_sidebar_navigation_css

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# Apply sidebar navigation CSS
apply_sidebar_navigation_css()

# Custom CSS with better fonts and responsive design
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
    
    /* Main content container */
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
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main > div {
            padding-top: 1rem;
        }
        
        /* Make metrics stack on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column;
        }
        
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 1rem;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
    }
    
    </style>
""", unsafe_allow_html=True)

st.title("💼 Job Tracker Application")
st.markdown("---")

try:
    # Get analytics data
    analytics = analytics_service.get_analytics()
    summary = analytics.get("summary", {})
    by_status = analytics.get("by_status", [])
    by_source = analytics.get("by_source", [])
    timeline = analytics.get("timeline", [])
    
    # Summary metrics with custom styling
    st.markdown("""
    <h2 style='font-size: 32px; font-weight: 800; color: #111827; 
               margin-bottom: 25px; letter-spacing: -1px;'>
        Tổng quan nhanh
    </h2>
    """, unsafe_allow_html=True)
    
    # Row 1: Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0; font-size: 18px;'>📝 Tổng đơn ứng tuyển</h3>
            <h1 style='color: white; margin: 10px 0; font-size: 48px; font-weight: bold;'>{}</h1>
            <p style='color: #e0e0e0; margin: 0; font-size: 14px;'>Tất cả đơn đã nộp</p>
        </div>
        """.format(summary.get("total_applications", 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0; font-size: 18px;'>⚡ Đang xử lý</h3>
            <h1 style='color: white; margin: 10px 0; font-size: 48px; font-weight: bold;'>{}</h1>
            <p style='color: #e0e0e0; margin: 0; font-size: 14px;'>Applied → Offer</p>
        </div>
        """.format(summary.get("active_applications", 0)), unsafe_allow_html=True)
    
    with col3:
        success_rate = summary.get('success_rate', 0)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0; font-size: 18px;'>🎯 Tỷ lệ thành công</h3>
            <h1 style='color: white; margin: 10px 0; font-size: 48px; font-weight: bold;'>{:.1f}%</h1>
            <p style='color: #e0e0e0; margin: 0; font-size: 14px;'>Hired / (Hired + Rejected)</p>
        </div>
        """.format(success_rate), unsafe_allow_html=True)
    
    st.markdown("")  # Add spacing
    
    # Row 2: Enhanced Jobs by key stages with beautiful gradient cards
    st.markdown("""
    <h3 style='font-size: 22px; font-weight: 700; color: #1f2937; 
               margin: 25px 0 20px 0; letter-spacing: -0.5px;'>
        Phân bố jobs theo giai đoạn
    </h3>
    """, unsafe_allow_html=True)
    
    # Calculate jobs by stage from by_status
    status_dict = {item['status']: item['count'] for item in by_status} if by_status else {}
    jobs_applied = status_dict.get('Applied', 0)
    jobs_screening = status_dict.get('Screening', 0)
    jobs_interview = status_dict.get('Interview', 0)
    jobs_offer = status_dict.get('Offer', 0)
    jobs_hired = status_dict.get('Hired', 0)
    jobs_rejected = status_dict.get('Rejected', 0)
    total_jobs = summary.get('total_applications', 0)
    
    # Calculate percentages
    applied_pct = (jobs_applied / total_jobs * 100) if total_jobs > 0 else 0
    screening_pct = (jobs_screening / total_jobs * 100) if total_jobs > 0 else 0
    interview_pct = (jobs_interview / total_jobs * 100) if total_jobs > 0 else 0
    offer_pct = (jobs_offer / total_jobs * 100) if total_jobs > 0 else 0
    hired_pct = (jobs_hired / total_jobs * 100) if total_jobs > 0 else 0
    rejected_pct = (jobs_rejected / total_jobs * 100) if total_jobs > 0 else 0
    
    # Row 1: Active stages (Applied → Offer)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.25);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                    border: 2px solid rgba(255,255,255,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;'>
                <div style='background: rgba(255,255,255,0.2); 
                           padding: 10px; border-radius: 12px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 28px;'>📝</span>
                </div>
                <div style='background: rgba(255,255,255,0.25); 
                           padding: 5px 12px; border-radius: 20px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 12px; font-weight: 700; color: white;'>
                        {applied_pct:.0f}%
                    </span>
                </div>
            </div>
            <div style='color: rgba(255,255,255,0.9); font-size: 13px; 
                       font-weight: 600; margin-bottom: 8px; text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                Đã nộp đơn
            </div>
            <div style='color: white; font-size: 42px; font-weight: 900; 
                       line-height: 1; margin-bottom: 8px;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                {jobs_applied}
            </div>
            <div style='color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 500;'>
                Jobs đang chờ xử lý
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    box-shadow: 0 8px 16px rgba(118, 75, 162, 0.25);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                    border: 2px solid rgba(255,255,255,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;'>
                <div style='background: rgba(255,255,255,0.2); 
                           padding: 10px; border-radius: 12px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 28px;'>🔍</span>
                </div>
                <div style='background: rgba(255,255,255,0.25); 
                           padding: 5px 12px; border-radius: 20px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 12px; font-weight: 700; color: white;'>
                        {screening_pct:.0f}%
                    </span>
                </div>
            </div>
            <div style='color: rgba(255,255,255,0.9); font-size: 13px; 
                       font-weight: 600; margin-bottom: 8px; text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                Đang screening
            </div>
            <div style='color: white; font-size: 42px; font-weight: 900; 
                       line-height: 1; margin-bottom: 8px;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                {jobs_screening}
            </div>
            <div style='color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 500;'>
                Hồ sơ đang được xem xét
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    box-shadow: 0 8px 16px rgba(240, 147, 251, 0.25);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                    border: 2px solid rgba(255,255,255,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;'>
                <div style='background: rgba(255,255,255,0.2); 
                           padding: 10px; border-radius: 12px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 28px;'>💬</span>
                </div>
                <div style='background: rgba(255,255,255,0.25); 
                           padding: 5px 12px; border-radius: 20px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 12px; font-weight: 700; color: white;'>
                        {interview_pct:.0f}%
                    </span>
                </div>
            </div>
            <div style='color: rgba(255,255,255,0.9); font-size: 13px; 
                       font-weight: 600; margin-bottom: 8px; text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                Đang phỏng vấn
            </div>
            <div style='color: white; font-size: 42px; font-weight: 900; 
                       line-height: 1; margin-bottom: 8px;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                {jobs_interview}
            </div>
            <div style='color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 500;'>
                Jobs đang trong vòng PV
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    box-shadow: 0 8px 16px rgba(79, 172, 254, 0.25);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                    border: 2px solid rgba(255,255,255,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;'>
                <div style='background: rgba(255,255,255,0.2); 
                           padding: 10px; border-radius: 12px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 28px;'>🎁</span>
                </div>
                <div style='background: rgba(255,255,255,0.25); 
                           padding: 5px 12px; border-radius: 20px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 12px; font-weight: 700; color: white;'>
                        {offer_pct:.0f}%
                    </span>
                </div>
            </div>
            <div style='color: rgba(255,255,255,0.9); font-size: 13px; 
                       font-weight: 600; margin-bottom: 8px; text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                Đã có offer
            </div>
            <div style='color: white; font-size: 42px; font-weight: 900; 
                       line-height: 1; margin-bottom: 8px;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                {jobs_offer}
            </div>
            <div style='color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 500;'>
                Offers đang cân nhắc
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    # Row 2: Outcome stages (Hired & Rejected)
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    box-shadow: 0 8px 16px rgba(67, 233, 123, 0.25);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                    border: 2px solid rgba(255,255,255,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;'>
                <div style='background: rgba(255,255,255,0.2); 
                           padding: 10px; border-radius: 12px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 28px;'>✅</span>
                </div>
                <div style='background: rgba(255,255,255,0.25); 
                           padding: 5px 12px; border-radius: 20px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 12px; font-weight: 700; color: white;'>
                        {hired_pct:.0f}%
                    </span>
                </div>
            </div>
            <div style='color: rgba(255,255,255,0.9); font-size: 13px; 
                       font-weight: 600; margin-bottom: 8px; text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                Đã nhận việc
            </div>
            <div style='color: white; font-size: 42px; font-weight: 900; 
                       line-height: 1; margin-bottom: 8px;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                {jobs_hired}
            </div>
            <div style='color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 500;'>
                Jobs đã chấp nhận
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    box-shadow: 0 8px 16px rgba(239, 68, 68, 0.25);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                    border: 2px solid rgba(255,255,255,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;'>
                <div style='background: rgba(255,255,255,0.2); 
                           padding: 10px; border-radius: 12px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 28px;'>❌</span>
                </div>
                <div style='background: rgba(255,255,255,0.25); 
                           padding: 5px 12px; border-radius: 20px;
                           backdrop-filter: blur(10px);'>
                    <span style='font-size: 12px; font-weight: 700; color: white;'>
                        {rejected_pct:.0f}%
                    </span>
                </div>
            </div>
            <div style='color: rgba(255,255,255,0.9); font-size: 13px; 
                       font-weight: 600; margin-bottom: 8px; text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                Bị từ chối
            </div>
            <div style='color: white; font-size: 42px; font-weight: 900; 
                       line-height: 1; margin-bottom: 8px;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                {jobs_rejected}
            </div>
            <div style='color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 500;'>
                Jobs không phù hợp
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Summary insight card
        active_jobs = jobs_applied + jobs_screening + jobs_interview + jobs_offer
        active_pct = (active_jobs / total_jobs * 100) if total_jobs > 0 else 0
        completed_jobs = jobs_hired + jobs_rejected
        completed_pct = (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                    padding: 25px 20px; border-radius: 16px; 
                    border: 2px solid #667eea40;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);'>
            <div style='margin-bottom: 20px;'>
                <div style='color: #667eea; font-size: 14px; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;'>
                    💼 Tổng quan Pipeline
                </div>
                <div style='color: #1f2937; font-size: 32px; font-weight: 900; 
                           line-height: 1; margin-bottom: 5px;'>
                    {total_jobs} <span style='font-size: 16px; font-weight: 600; color: #6b7280;'>jobs</span>
                </div>
            </div>
            <div style='display: flex; gap: 20px; margin-top: 20px;'>
                <div style='flex: 1;'>
                    <div style='color: #6b7280; font-size: 12px; font-weight: 600; margin-bottom: 8px;'>
                        🔄 Đang xử lý
                    </div>
                    <div style='display: flex; align-items: baseline; gap: 8px;'>
                        <span style='color: #667eea; font-size: 28px; font-weight: 900;'>{active_jobs}</span>
                        <span style='color: #667eea; font-size: 14px; font-weight: 700;'>({active_pct:.0f}%)</span>
                    </div>
                    <div style='background: #e5e7eb; height: 6px; border-radius: 3px; 
                               overflow: hidden; margin-top: 8px;'>
                        <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                                   height: 100%; width: {active_pct}%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
                <div style='flex: 1;'>
                    <div style='color: #6b7280; font-size: 12px; font-weight: 600; margin-bottom: 8px;'>
                        ✓ Đã hoàn thành
                    </div>
                    <div style='display: flex; align-items: baseline; gap: 8px;'>
                        <span style='color: #10b981; font-size: 28px; font-weight: 900;'>{completed_jobs}</span>
                        <span style='color: #10b981; font-size: 14px; font-weight: 700;'>({completed_pct:.0f}%)</span>
                    </div>
                    <div style='background: #e5e7eb; height: 6px; border-radius: 3px; 
                               overflow: hidden; margin-top: 8px;'>
                        <div style='background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); 
                                   height: 100%; width: {completed_pct}%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")  # Add spacing
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h3 style='font-size: 24px; font-weight: 700; color: #1f2937; 
                   margin-bottom: 20px; letter-spacing: -0.5px;'>
            Thống kê theo trạng thái
        </h3>
        """, unsafe_allow_html=True)
        if by_status:
            df_status = pd.DataFrame(by_status)
            # Filter out None/null status and ensure valid data
            df_status = df_status[df_status['status'].notna()]
            if not df_status.empty:
                df_status['count'] = pd.to_numeric(df_status['count'], errors='coerce').fillna(0).astype(int)
                
                # Map English status to Vietnamese
                status_vn_map = {
                    'Applied': 'Đã nộp',
                    'Screening': 'Sàng lọc',
                    'Interview': 'Phỏng vấn',
                    'Offer': 'Nhận offer',
                    'Hired': 'Đã nhận việc',
                    'Rejected': 'Bị từ chối'
                }
                df_status['status_vn'] = df_status['status'].map(status_vn_map).fillna(df_status['status'])
                
                # Create beautiful bar chart with plotly
                fig_status = px.bar(
                    df_status,
                    x='status_vn',
                    y='count',
                    labels={'status_vn': 'Trạng thái', 'count': 'Số lượng đơn'},
                    title='',
                    color='count',
                    color_continuous_scale='Blues',
                    text='count'
                )
                fig_status.update_traces(textposition='outside')
                fig_status.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Trạng thái",
                    yaxis_title="Số lượng đơn ứng tuyển",
                    hovermode='x unified'
                )
                st.plotly_chart(fig_status, use_container_width=True)
                
                # Show table with better labels
                with st.expander("📊 Xem bảng chi tiết"):
                    df_display = df_status.copy()
                    
                    # Use Vietnamese status names for display
                    df_display['status'] = df_display['status_vn']
                    df_display = df_display.drop(columns=['status_vn'])
                    
                    # Create column mapping based on what columns exist
                    column_mapping = {
                        'status': 'Trạng thái',
                        'count': 'Số lượng đơn',
                        'percentage': 'Tỷ lệ (%)'
                    }
                    
                    # Rename columns that exist
                    df_display.columns = [column_mapping.get(col, col) for col in df_display.columns]
                    
                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.info("Chưa có dữ liệu hợp lệ")
        else:
            st.info("Chưa có dữ liệu")
    
    with col2:
        st.markdown("""
        <h3 style='font-size: 24px; font-weight: 700; color: #1f2937; 
                   margin-bottom: 20px; letter-spacing: -0.5px;'>
            Thống kê theo nguồn tuyển dụng
        </h3>
        """, unsafe_allow_html=True)
        if by_source:
            df_source = pd.DataFrame(by_source)
            # Filter out None/null source and ensure valid data
            df_source = df_source[df_source['source'].notna()]
            if not df_source.empty:
                df_source['total_applications'] = pd.to_numeric(df_source['total_applications'], errors='coerce').fillna(0).astype(int)
                
                # Create beautiful horizontal bar chart with plotly
                fig_source = px.bar(
                    df_source.sort_values('total_applications', ascending=True),
                    x='total_applications',
                    y='source',
                    labels={'source': 'Nguồn tuyển dụng', 'total_applications': 'Số lượng đơn'},
                    title='',
                    orientation='h',
                    color='total_applications',
                    color_continuous_scale='Greens',
                    text='total_applications'
                )
                fig_source.update_traces(textposition='outside')
                fig_source.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Số lượng đơn ứng tuyển",
                    yaxis_title="Nguồn tuyển dụng",
                    hovermode='y unified'
                )
                st.plotly_chart(fig_source, use_container_width=True)
                
                # Show table with better labels
                with st.expander("📊 Xem bảng chi tiết"):
                    df_display = df_source.copy()
                    
                    # Create column mapping based on what columns exist
                    column_mapping = {
                        'source': 'Nguồn tuyển dụng',
                        'total_applications': 'Tổng số đơn',
                        'hired_count': 'Đã nhận việc',
                        'rejected_count': 'Bị từ chối',
                        'in_progress_count': 'Đang xử lý',
                        'success_rate': 'Tỷ lệ thành công (%)'
                    }
                    
                    # Rename columns that exist
                    df_display.columns = [column_mapping.get(col, col) for col in df_display.columns]
                    
                    # Sort by total applications
                    if 'Tổng số đơn' in df_display.columns:
                        df_display = df_display.sort_values('Tổng số đơn', ascending=False)
                    
                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.info("Chưa có dữ liệu hợp lệ")
        else:
            st.info("Chưa có dữ liệu")
    
    # Timeline
    st.markdown("---")
    st.markdown("""
    <h2 style='font-size: 32px; font-weight: 800; color: #111827; 
               margin-top: 10px; margin-bottom: 25px; letter-spacing: -1px;'>
        Xu hướng hoạt động theo thời gian
    </h2>
    """, unsafe_allow_html=True)
    
    if timeline:
        df_timeline = pd.DataFrame(timeline)
        
        # Calculate actual insights from by_status (not timeline sum which can be duplicate)
        status_dict = {item['status']: item['count'] for item in by_status} if by_status else {}
        
        # Get real counts from status breakdown
        total_apps = summary.get('total_applications', 0)  # Total applications from summary
        total_interviews_status = status_dict.get('Interview', 0)  # Jobs currently in Interview status
        total_offers_status = status_dict.get('Offer', 0)  # Jobs currently in Offer status
        total_hired = status_dict.get('Hired', 0)  # Jobs that got hired
        
        # For timeline visualization - keep timeline sums
        timeline_apps = df_timeline['applications'].sum() if 'applications' in df_timeline.columns else 0
        timeline_interviews = df_timeline['interviews'].sum() if 'interviews' in df_timeline.columns else 0
        timeline_offers = df_timeline['offers'].sum() if 'offers' in df_timeline.columns else 0
        timeline_hired = df_timeline['hired'].sum() if 'hired' in df_timeline.columns else 0
        
        # Calculate conversion rates using summary data (more accurate)
        # Interview rate: jobs that reached interview stage / total jobs
        jobs_reached_interview = (status_dict.get('Interview', 0) + status_dict.get('Offer', 0) + 
                                   status_dict.get('Hired', 0) + status_dict.get('Rejected', 0))
        interview_rate = (jobs_reached_interview / total_apps * 100) if total_apps > 0 else 0
        
        # Offer rate: jobs that got offer / jobs that reached interview
        jobs_got_offer = status_dict.get('Offer', 0) + status_dict.get('Hired', 0)
        offer_rate = (jobs_got_offer / jobs_reached_interview * 100) if jobs_reached_interview > 0 else 0
        
        # Quick insights above chart (use timeline data for display)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style='background: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 4px solid #1f77b4;'>
                <p style='margin: 0; color: #666; font-size: 12px;'>Tổng đơn nộp (6 tháng)</p>
                <h2 style='margin: 5px 0; color: #1f77b4;'>{timeline_apps}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: #fff5f0; padding: 15px; border-radius: 10px; border-left: 4px solid #ff7f0e;'>
                <p style='margin: 0; color: #666; font-size: 12px;'>Tổng buổi PV (6 tháng)</p>
                <h2 style='margin: 5px 0; color: #ff7f0e;'>{timeline_interviews}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: #f0fff4; padding: 15px; border-radius: 10px; border-left: 4px solid #2ca02c;'>
                <p style='margin: 0; color: #666; font-size: 12px;'>Tổng offers nhận được</p>
                <h2 style='margin: 5px 0; color: #2ca02c;'>{timeline_offers}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: #f5f0ff; padding: 15px; border-radius: 10px; border-left: 4px solid #9467bd;'>
                <p style='margin: 0; color: #666; font-size: 12px;'>Đã nhận việc</p>
                <h2 style='margin: 5px 0; color: #9467bd;'>{timeline_hired}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")  # Spacing
        
        # Create comprehensive multi-line chart with enhanced styling
        fig_timeline = go.Figure()
        
        # Add line for applications
        if 'applications' in df_timeline.columns:
            fig_timeline.add_trace(go.Scatter(
                x=df_timeline['period'],
                y=df_timeline['applications'],
                mode='lines+markers',
                name='Đơn ứng tuyển',
                line=dict(color='#667eea', width=4, shape='spline'),
                marker=dict(size=12, color='#667eea', line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)',
                hovertemplate='<b>Đơn ứng tuyển</b><br>%{y} đơn<extra></extra>'
            ))
        
        # Add line for interviews
        if 'interviews' in df_timeline.columns:
            fig_timeline.add_trace(go.Scatter(
                x=df_timeline['period'],
                y=df_timeline['interviews'],
                mode='lines+markers',
                name='Buổi phỏng vấn',
                line=dict(color='#f093fb', width=4, shape='spline'),
                marker=dict(size=12, color='#f093fb', line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(240, 147, 251, 0.1)',
                hovertemplate='<b>Buổi phỏng vấn</b><br>%{y} buổi<extra></extra>'
            ))
        
        # Add line for offers
        if 'offers' in df_timeline.columns:
            fig_timeline.add_trace(go.Scatter(
                x=df_timeline['period'],
                y=df_timeline['offers'],
                mode='lines+markers',
                name='Offers',
                line=dict(color='#4facfe', width=4, shape='spline'),
                marker=dict(size=12, color='#4facfe', line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(79, 172, 254, 0.1)',
                hovertemplate='<b>Offers</b><br>%{y} offer<extra></extra>'
            ))
        
        # Add line for hired
        if 'hired' in df_timeline.columns:
            fig_timeline.add_trace(go.Scatter(
                x=df_timeline['period'],
                y=df_timeline['hired'],
                mode='lines+markers',
                name='Đã nhận việc',
                line=dict(color='#43e97b', width=4, shape='spline'),
                marker=dict(size=12, color='#43e97b', line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(67, 233, 123, 0.1)',
                hovertemplate='<b>Đã nhận việc</b><br>%{y} job<extra></extra>'
            ))
        
        # Add line for rejected
        if 'rejected' in df_timeline.columns:
            fig_timeline.add_trace(go.Scatter(
                x=df_timeline['period'],
                y=df_timeline['rejected'],
                mode='lines+markers',
                name='Bị từ chối',
                line=dict(color='#ef4444', width=4, shape='spline'),
                marker=dict(size=12, color='#ef4444', line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(239, 68, 68, 0.1)',
                hovertemplate='<b>Bị từ chối</b><br>%{y} đơn<extra></extra>'
            ))
        
        fig_timeline.update_layout(
            xaxis_title="Tháng",
            yaxis_title="Số lượng",
            hovermode='x unified',
            height=450,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        # Add grid for better readability
        fig_timeline.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig_timeline.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Key insights section
        st.markdown("""
        <h3 style='font-size: 22px; font-weight: 700; color: #1f2937; 
                   margin-top: 25px; margin-bottom: 20px; letter-spacing: -0.5px;'>
            Phân tích tỷ lệ chuyển đổi
        </h3>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 12px; color: white;'>
                <h4 style='margin: 0 0 10px 0;'>📊 Tỷ lệ đến phỏng vấn</h4>
                <h2 style='margin: 0; font-size: 36px;'>{interview_rate:.1f}%</h2>
                <p style='margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;'>
                    {jobs_reached_interview} jobs đến PV / {total_apps} đơn nộp
                </p>
                <p style='margin: 5px 0 0 0; font-size: 12px; opacity: 0.8;'>
                    {'✨ Tốt!' if interview_rate >= 40 else '📈 Có thể cải thiện' if interview_rate >= 25 else '💪 Tiếp tục cố gắng!'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px; border-radius: 12px; color: white;'>
                <h4 style='margin: 0 0 10px 0;'>🎯 Tỷ lệ nhận offer</h4>
                <h2 style='margin: 0; font-size: 36px;'>{offer_rate:.1f}%</h2>
                <p style='margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;'>
                    {jobs_got_offer} jobs có offer / {jobs_reached_interview} jobs PV
                </p>
                <p style='margin: 5px 0 0 0; font-size: 12px; opacity: 0.8;'>
                    {'🎉 Xuất sắc!' if offer_rate >= 30 else '👍 Khá tốt' if offer_rate >= 15 else '💼 Cần cải thiện kỹ năng PV'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")  # Spacing
        
        # Detailed table
        with st.expander("📊 Xem bảng dữ liệu chi tiết"):
            df_display = df_timeline.copy()
            column_mapping = {
                'period': 'Tháng',
                'applications': 'Đơn nộp',
                'interviews': 'Buổi PV',
                'offers': 'Offers',
                'hired': 'Đã nhận việc',
                'rejected': 'Bị từ chối'
            }
            df_display.columns = [column_mapping.get(col, col) for col in df_display.columns]
            
            # Add conversion rate columns
            if all(col in df_display.columns for col in ['Đơn nộp', 'Buổi PV']):
                df_display['Tỷ lệ PV (%)'] = (df_display['Buổi PV'] / df_display['Đơn nộp'] * 100).fillna(0).round(1)
            
            if all(col in df_display.columns for col in ['Buổi PV', 'Offers']):
                df_display['Tỷ lệ Offer (%)'] = (df_display['Offers'] / df_display['Buổi PV'] * 100).fillna(0).round(1)
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("Chưa có dữ liệu timeline")
    
    # Pipeline Flow Visualization
    st.markdown("---")
    st.markdown("""
    <h2 style='font-size: 32px; font-weight: 800; color: #111827; 
               margin-top: 10px; margin-bottom: 25px; letter-spacing: -1px;'>
        Pipeline ứng tuyển
    </h2>
    """, unsafe_allow_html=True)
    
    if by_status:
        # Prepare data
        status_dict = {item['status']: item['count'] for item in by_status}
        
        # Define pipeline stages in typical order
        pipeline_order = ['Applied', 'Screening', 'Interview', 'Offer', 'Hired', 'Rejected']
        status_vn_map = {
            'Applied': 'Đã nộp',
            'Screening': 'Sàng lọc',
            'Interview': 'Phỏng vấn',
            'Offer': 'Nhận offer',
            'Hired': 'Đã nhận việc',
            'Rejected': 'Bị từ chối'
        }
        
        # Calculate total applications (should be sum of all statuses)
        total_applications = sum(status_dict.values())
        
        # Create enhanced horizontal pipeline visualization
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 35px; border-radius: 20px; margin-bottom: 30px;
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);'>
            <div style='text-align: center; margin-bottom: 25px;'>
                <h3 style='font-size: 24px; font-weight: 800; color: white; margin: 0; 
                           letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    Luồng chuyển đổi trạng thái
                </h3>
                <p style='font-size: 14px; color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-weight: 500;'>
                    Tổng {total_applications} đơn ứng tuyển
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create pipeline stages
        pipeline_cols = st.columns(5)
        pipeline_colors = {
            'Applied': '#667eea',
            'Screening': '#764ba2', 
            'Interview': '#f093fb',
            'Offer': '#4facfe',
            'Hired': '#10b981'
        }
        
        # Background gradient for each stage
        bg_gradients = {
            'Applied': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'Screening': 'linear-gradient(135deg, #764ba2 0%, #f093fb 100%)',
            'Interview': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'Offer': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'Hired': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
        }
        
        for idx, (status, col) in enumerate(zip(pipeline_order[:5], pipeline_cols)):
            count = status_dict.get(status, 0)
            percentage = (count / total_applications * 100) if total_applications > 0 else 0
            status_vn = status_vn_map[status]
            color = pipeline_colors[status]
            bg_gradient = bg_gradients[status]
            
            with col:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='background: {bg_gradient}; 
                                border-radius: 16px; 
                                padding: 25px 12px;
                                box-shadow: 0 8px 16px rgba(0,0,0,0.15);
                                position: relative;
                                margin-bottom: 10px;
                                transform: translateY(0);
                                transition: transform 0.2s ease;
                                border: 2px solid rgba(255,255,255,0.2);'>
                        <div style='font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.9); 
                                    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>
                            {status_vn}
                        </div>
                        <div style='font-size: 40px; font-weight: 900; color: white; 
                                    line-height: 1; margin: 10px 0;
                                    text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                            {count}
                        </div>
                        <div style='background: rgba(255,255,255,0.25); 
                                    padding: 6px 14px; border-radius: 20px; 
                                    display: inline-block; margin-top: 8px;
                                    backdrop-filter: blur(10px);'>
                            <span style='font-size: 14px; font-weight: 700; color: white;'>
                                {percentage:.1f}%
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add arrow between stages (outside the column)
                if idx < 4:
                    st.markdown("""
                    <div style='text-align: center; margin: -5px 0 0 0;'>
                        <span style='font-size: 36px; color: #ffc1cc; 
                                     filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
                                     display: inline-block;'>
                            ➤
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Rejected box below
        rejected_count = status_dict.get('Rejected', 0)
        rejected_pct = (rejected_count / total_applications * 100) if total_applications > 0 else 0
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if rejected_count > 0:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                        padding: 20px; border-radius: 12px; border-left: 5px solid #ef4444; 
                        margin-bottom: 30px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <span style='font-size: 14px; font-weight: 600; color: #991b1b;'>
                            ❌ Bị từ chối tại các giai đoạn
                        </span>
                    </div>
                    <div style='text-align: right;'>
                        <span style='font-size: 28px; font-weight: 800; color: #ef4444;'>{rejected_count}</span>
                        <span style='font-size: 14px; font-weight: 600; color: #ef4444; margin-left: 8px;'>
                            ({rejected_pct:.1f}%)
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Create two columns for detailed metrics
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Conversion metrics below funnel - Enhanced version
            st.markdown("""
            <h3 style='font-size: 22px; font-weight: 700; color: #1f2937; 
                       margin-top: 30px; margin-bottom: 20px; letter-spacing: -0.5px;'>
                Tỷ lệ chuyển đổi giữa các giai đoạn
            </h3>
            """, unsafe_allow_html=True)
            
            # Calculate conversion between stages with Vietnamese labels
            status_vn_map = {
                'Applied': 'Đã nộp',
                'Screening': 'Sàng lọc', 
                'Interview': 'Phỏng vấn',
                'Offer': 'Nhận offer',
                'Hired': 'Đã nhận việc'
            }
            
            # Only calculate conversions for the 5 main pipeline stages (exclude Rejected)
            main_pipeline = ['Applied', 'Screening', 'Interview', 'Offer', 'Hired']
            conversions = []
            for i in range(len(main_pipeline) - 1):
                current_stage = main_pipeline[i]
                next_stage = main_pipeline[i + 1]
                current_count = status_dict.get(current_stage, 0)
                next_count = status_dict.get(next_stage, 0)
                
                rate = (next_count / current_count * 100) if current_count > 0 else 0
                conversions.append({
                    'from': status_vn_map.get(current_stage, current_stage),
                    'to': status_vn_map.get(next_stage, next_stage),
                    'from_count': current_count,
                    'to_count': next_count,
                    'rate': rate
                })
            
            # Display in 2x2 grid for better visualization
            row1_cols = st.columns(2)
            row2_cols = st.columns(2)
            all_cols = [row1_cols[0], row1_cols[1], row2_cols[0], row2_cols[1]]
            
            for idx, conv in enumerate(conversions):
                with all_cols[idx]:
                    # Color and icon based on rate with better thresholds
                    if conv['rate'] >= 60:
                        color = '#10b981'  # green-500
                        bg_gradient = 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)'
                        badge = 'Tuyệt vời'
                        badge_color = '#059669'
                    elif conv['rate'] >= 40:
                        color = '#3b82f6'  # blue-500
                        bg_gradient = 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)'
                        badge = 'Tốt'
                        badge_color = '#2563eb'
                    elif conv['rate'] >= 20:
                        color = '#f59e0b'  # amber-500
                        bg_gradient = 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)'
                        badge = 'Trung bình'
                        badge_color = '#d97706'
                    else:
                        color = '#ef4444'  # red-500
                        bg_gradient = 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)'
                        badge = 'Cần cải thiện'
                        badge_color = '#dc2626'
                    
                    st.markdown(f"""
                    <div style='background: {bg_gradient}; 
                                padding: 20px; 
                                border-radius: 12px; 
                                border: 2px solid {color}30;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.07);
                                margin-bottom: 15px;
                                transition: transform 0.2s;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                            <span style='font-size: 12px; font-weight: 600; color: {badge_color}; 
                                       background: white; padding: 4px 10px; border-radius: 12px;'>
                                {badge}
                            </span>
                            <span style='font-size: 11px; color: #6b7280; font-weight: 500;'>
                                Giai đoạn {idx + 1}
                            </span>
                        </div>
                        <div style='text-align: center; margin: 15px 0;'>
                            <div style='font-size: 40px; font-weight: 800; color: {color}; 
                                       line-height: 1; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                {conv['rate']:.1f}<span style='font-size: 24px;'>%</span>
                            </div>
                        </div>
                        <div style='background: white; padding: 10px; border-radius: 8px; margin-top: 12px;'>
                            <div style='font-size: 13px; color: #374151; font-weight: 600; margin-bottom: 6px;'>
                                {conv['from']} → {conv['to']}
                            </div>
                            <div style='font-size: 12px; color: #6b7280;'>
                                {conv['to_count']} / {conv['from_count']} chuyển tiếp
                            </div>
                            <div style='background: #e5e7eb; height: 6px; border-radius: 3px; 
                                       overflow: hidden; margin-top: 8px;'>
                                <div style='background: {color}; height: 100%; width: {conv['rate']:.1f}%; 
                                           transition: width 0.3s ease;'></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <h3 style='font-size: 22px; font-weight: 700; color: #1f2937; 
                       margin-bottom: 20px; letter-spacing: -0.5px;'>
                Phân bố trạng thái
            </h3>
            """, unsafe_allow_html=True)
            
            # Show each status with count and percentage
            # Map English status to Vietnamese
            status_vn_map = {
                'Applied': 'Đã nộp',
                'Screening': 'Sàng lọc',
                'Interview': 'Phỏng vấn',
                'Offer': 'Nhận offer',
                'Hired': 'Đã nhận việc',
                'Rejected': 'Bị từ chối'
            }
            
            # Show all 6 statuses including Rejected
            for status in ['Applied', 'Screening', 'Interview', 'Offer', 'Hired', 'Rejected']:
                status_vn = status_vn_map.get(status, status)
                count = status_dict.get(status, 0)
                percentage = (count / total_applications * 100) if total_applications > 0 else 0
                icon = STATUS_COLORS.get(status, '⚪')
                
                # Color coding based on status
                if status == 'Hired':
                    color = '#43e97b'
                    bg_color = '#f0fdf4'
                elif status == 'Offer':
                    color = '#4facfe'
                    bg_color = '#eff6ff'
                elif status == 'Interview':
                    color = '#f093fb'
                    bg_color = '#fdf4ff'
                elif status == 'Screening':
                    color = '#764ba2'
                    bg_color = '#f5f3ff'
                elif status == 'Rejected':
                    color = '#ef4444'
                    bg_color = '#fee2e2'
                else:  # Applied
                    color = '#667eea'
                    bg_color = '#eef2ff'
                
                st.markdown(f"""
                <div style='background: {bg_color}; padding: 12px; border-radius: 8px; 
                            margin-bottom: 10px; border-left: 4px solid {color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-weight: 600; font-size: 14px;'>{icon} {status_vn}</span>
                        <span style='font-size: 20px; font-weight: bold; color: {color};'>{count}</span>
                    </div>
                    <div style='margin-top: 8px;'>
                        <div style='background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden;'>
                            <div style='background: {color}; height: 100%; width: {percentage}%; transition: width 0.3s;'></div>
                        </div>
                        <span style='font-size: 12px; color: #6b7280; margin-top: 4px; display: block;'>
                            {percentage:.1f}% của tổng
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Overall success insight (remove duplicate rejected display)
            st.markdown("---")
            hired_count = status_dict.get('Hired', 0)
            rejected_count = status_dict.get('Rejected', 0)
            completed_applications = hired_count + rejected_count
            
            # Success rate based on completed applications only (Hired + Rejected)
            success_rate = (hired_count / completed_applications * 100) if completed_applications > 0 else 0
            
            if success_rate >= 50:
                emoji = '🎉'
                message = 'Xuất sắc!'
                color = '#10b981'
            elif success_rate >= 30:
                emoji = '🌟'
                message = 'Rất tốt!'
                color = '#43e97b'
            elif success_rate >= 15:
                emoji = '👍'
                message = 'Tiến triển tốt'
                color = '#4facfe'
            else:
                emoji = '💪'
                message = 'Tiếp tục cố gắng!'
                color = '#667eea'
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}20 0%, {color}10 100%); 
                        padding: 20px; border-radius: 12px; text-align: center; border: 2px solid {color}40;'>
                <div style='font-size: 48px; margin-bottom: 10px;'>{emoji}</div>
                <div style='font-size: 32px; font-weight: bold; color: {color};'>
                    {success_rate:.1f}%
                </div>
                <div style='font-size: 14px; color: #6b7280; margin-top: 5px;'>
                    Tỷ lệ thành công tổng thể
                </div>
                <div style='font-size: 11px; color: #9ca3af; margin-top: 3px;'>
                    {hired_count} nhận việc / {completed_applications} đơn hoàn thành
                </div>
                <div style='font-size: 12px; color: {color}; font-weight: 600; margin-top: 8px;'>
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Chưa có dữ liệu để hiển thị pipeline funnel")

except Exception as e:
    st.warning("⚠️ Không thể kết nối với backend API. Vui lòng đảm bảo server đang chạy!")
    st.code(f"Error: {str(e)}")
    st.info("👉 Chạy backend bằng lệnh: `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`")
    
    # Show status legend even if API fails
    st.markdown("---")
    st.subheader("📌 Trạng thái Pipeline")
    
    cols = st.columns(len(STATUS_COLORS))
    for idx, (status, icon) in enumerate(STATUS_COLORS.items()):
        with cols[idx]:
            st.markdown(f"{icon} **{status}**")
