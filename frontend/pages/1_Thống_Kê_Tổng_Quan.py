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
    
    # Summary metrics with custom styling - Enhanced header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 35px 40px; border-radius: 20px; margin-bottom: 35px;
                box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);'>
        <h2 style='font-size: 38px; font-weight: 900; color: white; 
                   margin: 0 0 10px 0; letter-spacing: -1.5px;
                   text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);'>
            ⚡ Tổng quan nhanh
        </h2>
        <p style='color: rgba(255, 255, 255, 0.85); font-size: 15px; margin: 0; font-weight: 500;'>
            Chỉ số quan trọng về quá trình ứng tuyển của bạn
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 1: Main metrics with enhanced design
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 35px 30px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                    border: 2px solid rgba(255, 255, 255, 0.15);'>
            <div style='background: rgba(255, 255, 255, 0.2); 
                       width: 60px; height: 60px; border-radius: 50%; 
                       margin: 0 auto 20px; display: flex; align-items: center; 
                       justify-content: center; font-size: 32px;
                       backdrop-filter: blur(10px);'>
                📝
            </div>
            <h3 style='color: rgba(255, 255, 255, 0.95); margin: 0 0 12px 0; 
                      font-size: 15px; font-weight: 700; text-transform: uppercase; 
                      letter-spacing: 1.5px;'>
                Tổng đơn ứng tuyển
            </h3>
            <h1 style='color: white; margin: 0 0 15px 0; font-size: 64px; font-weight: 900; 
                      line-height: 1; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);'>
                {}
            </h1>
            <p style='color: rgba(255, 255, 255, 0.8); margin: 0; font-size: 14px; font-weight: 600;'>
                Tất cả đơn đã nộp
            </p>
        </div>
        """.format(summary.get("total_applications", 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 35px 30px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
                    border: 2px solid rgba(255, 255, 255, 0.15);'>
            <div style='background: rgba(255, 255, 255, 0.2); 
                       width: 60px; height: 60px; border-radius: 50%; 
                       margin: 0 auto 20px; display: flex; align-items: center; 
                       justify-content: center; font-size: 32px;
                       backdrop-filter: blur(10px);'>
                ⚡
            </div>
            <h3 style='color: rgba(255, 255, 255, 0.95); margin: 0 0 12px 0; 
                      font-size: 15px; font-weight: 700; text-transform: uppercase; 
                      letter-spacing: 1.5px;'>
                Đang xử lý
            </h3>
            <h1 style='color: white; margin: 0 0 15px 0; font-size: 64px; font-weight: 900; 
                      line-height: 1; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);'>
                {}
            </h1>
            <p style='color: rgba(255, 255, 255, 0.8); margin: 0; font-size: 14px; font-weight: 600;'>
                Applied → Offer
            </p>
        </div>
        """.format(summary.get("active_applications", 0)), unsafe_allow_html=True)
    
    with col3:
        success_rate = summary.get('success_rate', 0)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 35px 30px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
                    border: 2px solid rgba(255, 255, 255, 0.15);'>
            <div style='background: rgba(255, 255, 255, 0.2); 
                       width: 60px; height: 60px; border-radius: 50%; 
                       margin: 0 auto 20px; display: flex; align-items: center; 
                       justify-content: center; font-size: 32px;
                       backdrop-filter: blur(10px);'>
                🎯
            </div>
            <h3 style='color: rgba(255, 255, 255, 0.95); margin: 0 0 12px 0; 
                      font-size: 15px; font-weight: 700; text-transform: uppercase; 
                      letter-spacing: 1.5px;'>
                Tỷ lệ thành công
            </h3>
            <h1 style='color: white; margin: 0 0 15px 0; font-size: 64px; font-weight: 900; 
                      line-height: 1; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);'>
                {:.1f}%
            </h1>
            <p style='color: rgba(255, 255, 255, 0.8); margin: 0; font-size: 14px; font-weight: 600;'>
                Hired / (Hired + Rejected)
            </p>
        </div>
        """.format(success_rate), unsafe_allow_html=True)
    
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
            
            # Display in 2x2 grid for conversion cards
            row1_cols = st.columns(2)
            row2_cols = st.columns(2)
            all_cols = [row1_cols[0], row1_cols[1], row2_cols[0], row2_cols[1]]
            
            for idx, conv in enumerate(conversions):
                with all_cols[idx]:
                    # Premium gradient color and icon based on rate
                    if conv['rate'] >= 60:
                        gradient = 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                        shadow = 'rgba(16, 185, 129, 0.4)'
                        badge = 'Tuyệt vời'
                        emoji = '🚀'
                    elif conv['rate'] >= 40:
                        gradient = 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                        shadow = 'rgba(59, 130, 246, 0.4)'
                        badge = 'Tốt'
                        emoji = '⭐'
                    elif conv['rate'] >= 20:
                        gradient = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                        shadow = 'rgba(245, 158, 11, 0.4)'
                        badge = 'Trung bình'
                        emoji = '💪'
                    else:
                        gradient = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
                        shadow = 'rgba(239, 68, 68, 0.4)'
                        badge = 'Cần cải thiện'
                        emoji = '📈'
                    
                    st.markdown(f"""
                    <div style='background: {gradient}; 
                                padding: 22px 20px; 
                                border-radius: 18px; 
                                border: 2px solid rgba(255, 255, 255, 0.3);
                                box-shadow: 0 8px 20px {shadow};
                                margin-bottom: 15px;
                                transition: all 0.3s ease;
                                position: relative;
                                overflow: hidden;
                                cursor: pointer;'
                         onmouseover="this.style.transform='translateY(-5px) scale(1.02)'; this.style.boxShadow='0 12px 32px {shadow}';";
                         onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 20px {shadow}';">
                        <div style='position: absolute; top: -20px; right: -20px; width: 80px; height: 80px;
                                   background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
                                   border-radius: 50%;'></div>
                        <div style='position: relative; z-index: 1;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;'>
                                <div style='background: rgba(255, 255, 255, 0.25); padding: 6px 14px; border-radius: 20px;
                                           backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3);'>
                                    <span style='font-size: 11px; font-weight: 700; color: white; 
                                               text-transform: uppercase; letter-spacing: 0.5px;'>
                                        {emoji} {badge}
                                    </span>
                                </div>
                                <div style='background: rgba(0, 0, 0, 0.15); padding: 4px 10px; border-radius: 12px;
                                           backdrop-filter: blur(5px);'>
                                    <span style='font-size: 10px; color: rgba(255, 255, 255, 0.9); font-weight: 600;'>
                                        Giai đoạn {idx + 1}
                                    </span>
                                </div>
                            </div>
                            <div style='text-align: center; margin: 18px 0;'>
                                <div style='font-size: 52px; font-weight: 900; color: white; 
                                           line-height: 1; text-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                    {conv['rate']:.1f}<span style='font-size: 28px; font-weight: 800;'>%</span>
                                </div>
                            </div>
                            <div style='background: rgba(255, 255, 255, 0.2); padding: 12px; border-radius: 12px; 
                                       backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.25);'>
                                <div style='font-size: 13px; color: white; font-weight: 700; margin-bottom: 8px;
                                           text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                    {conv['from']} → {conv['to']}
                                </div>
                                <div style='font-size: 12px; color: rgba(255, 255, 255, 0.9); font-weight: 600; margin-bottom: 10px;'>
                                    {conv['to_count']} / {conv['from_count']} chuyển tiếp thành công
                                </div>
                                <div style='background: rgba(0, 0, 0, 0.15); height: 8px; border-radius: 10px; 
                                           overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);'>
                                    <div style='background: rgba(255, 255, 255, 0.9); height: 100%; width: {conv['rate']:.1f}%; 
                                               border-radius: 10px;
                                               transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                                               box-shadow: 0 0 12px rgba(255, 255, 255, 0.6);
                                               position: relative;'>
                                        <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                                                   background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                                                   animation: shimmer 2s infinite;'></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add prominent success rate card spanning 2 columns with liquid style
            st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
            
            hired_count = status_dict.get('Hired', 0)
            rejected_count = status_dict.get('Rejected', 0)
            completed_applications = hired_count + rejected_count
            
            # Success rate based on completed applications only (Hired + Rejected)
            success_rate = (hired_count / completed_applications * 100) if completed_applications > 0 else 0
            
            if success_rate >= 50:
                emoji = '🎉'
                message = 'Xuất sắc!'
                base_color = '#10b981'
                glow_color = 'rgba(16, 185, 129, 0.3)'
            elif success_rate >= 30:
                emoji = '🌟'
                message = 'Rất tốt!'
                base_color = '#43e97b'
                glow_color = 'rgba(67, 233, 123, 0.3)'
            elif success_rate >= 15:
                emoji = '👍'
                message = 'Tiến triển tốt'
                base_color = '#4facfe'
                glow_color = 'rgba(79, 172, 254, 0.3)'
            else:
                emoji = '💪'
                message = 'Tiếp tục cố gắng!'
                base_color = '#667eea'
                glow_color = 'rgba(102, 126, 234, 0.3)'
            
            # Build HTML string properly to avoid rendering issues
            st.markdown(f"""
            <div style='background: white; padding: 45px 40px; border-radius: 24px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08); border: 3px solid {base_color}; position: relative; overflow: hidden; transition: all 0.3s ease;' onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 20px 60px {glow_color}';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 12px 40px rgba(0, 0, 0, 0.08)';">
                <div style='position: absolute; top: -30px; right: -30px; width: 120px; height: 120px; background: {base_color}; opacity: 0.08; border-radius: 50%; box-shadow: 0 0 60px {glow_color};'></div>
                <div style='position: absolute; bottom: -20px; left: -20px; width: 80px; height: 80px; background: {base_color}; opacity: 0.06; border-radius: 50%;'></div>
                <div style='position: absolute; top: 50%; right: 10%; width: 40px; height: 40px; background: {base_color}; opacity: 0.05; border-radius: 50%;'></div>
                <div style='position: relative; z-index: 1; text-align: center;'>
                    <div style='display: flex; align-items: center; justify-content: center; background: {base_color}; width: 100px; height: 100px; border-radius: 50%; box-shadow: 0 8px 24px {glow_color}, inset 0 -4px 12px rgba(0,0,0,0.1); position: relative; margin: 0 auto 25px auto; animation: float 3s ease-in-out infinite;'>
                        <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(180deg, rgba(255,255,255,0.4) 0%, transparent 60%); border-radius: 50%;'></div>
                        <span style='font-size: 48px; position: relative; z-index: 1; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));'>{emoji}</span>
                    </div>
                    <div style='font-size: 72px; font-weight: 900; color: {base_color}; line-height: 1; margin-bottom: 12px; text-shadow: 0 4px 12px {glow_color}; letter-spacing: -2px;'>
                        {success_rate:.1f}<span style='font-size: 42px;'>%</span>
                    </div>
                    <div style='font-size: 16px; color: #6b7280; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px;'>
                        Tỷ lệ thành công tổng thể
                    </div>
                    <div style='display: inline-block; background: {base_color}; padding: 12px 32px; border-radius: 30px; box-shadow: 0 6px 20px {glow_color}, inset 0 2px 0 rgba(255,255,255,0.3); margin-bottom: 25px; position: relative; overflow: hidden;'>
                        <div style='position: absolute; top: 0; left: 0; right: 0; height: 50%; background: linear-gradient(180deg, rgba(255,255,255,0.2) 0%, transparent 100%);'></div>
                        <span style='color: white; font-size: 16px; font-weight: 800; letter-spacing: 1px; position: relative; z-index: 1; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>{message}</span>
                    </div>
                    <div style='background: #f9fafb; padding: 20px; border-radius: 16px; border: 2px solid #f3f4f6;'>
                        <div style='font-size: 14px; color: #9ca3af; margin-bottom: 8px; font-weight: 600;'>Chi tiết kết quả</div>
                        <div style='font-size: 16px; color: #1f2937; font-weight: 700;'>
                            <span style='color: {base_color}; font-size: 24px;'>{hired_count}</span> nhận việc
                            <span style='color: #d1d5db; margin: 0 8px;'>/</span>
                            <span style='color: #6b7280; font-size: 20px;'>{completed_applications}</span> đơn hoàn thành
                        </div>
                    </div>
                </div>
                <style>
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-15px); }}
                }}
                </style>
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
            # Map English status to Vietnamese with liquid emoji
            status_vn_map = {
                'Applied': 'Đã nộp - Jobs đang chờ xử lý',
                'Screening': 'Sàng lọc - Hồ sơ đang được xem xét',
                'Interview': 'Phỏng vấn - Jobs đang trong vòng PV',
                'Offer': 'Nhận offer - Offers đang cân nhắc',
                'Hired': 'Đã nhận việc - Jobs đã chấp nhận',
                'Rejected': 'Bị từ chối - Jobs không phù hợp'
            }
            
            # Liquid-style emoji mapping
            liquid_emoji_map = {
                'Applied': '💧',
                'Screening': '🔍',
                'Interview': '💬',
                'Offer': '🎁',
                'Hired': '✨',
                'Rejected': '❌'
            }
            
            # Show all 6 statuses including Rejected with enhanced design
            for status in ['Applied', 'Screening', 'Interview', 'Offer', 'Hired', 'Rejected']:
                status_vn = status_vn_map.get(status, status)
                count = status_dict.get(status, 0)
                percentage = (count / total_applications * 100) if total_applications > 0 else 0
                liquid_icon = liquid_emoji_map.get(status, '⚪')
                
                # Enhanced gradient color coding
                if status == 'Hired':
                    gradient = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                    shadow_color = 'rgba(67, 233, 123, 0.3)'
                    bar_color = '#43e97b'
                elif status == 'Offer':
                    gradient = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
                    shadow_color = 'rgba(79, 172, 254, 0.3)'
                    bar_color = '#4facfe'
                elif status == 'Interview':
                    gradient = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
                    shadow_color = 'rgba(240, 147, 251, 0.3)'
                    bar_color = '#f093fb'
                elif status == 'Screening':
                    gradient = 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)'
                    shadow_color = 'rgba(118, 75, 162, 0.3)'
                    bar_color = '#764ba2'
                elif status == 'Rejected':
                    gradient = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
                    shadow_color = 'rgba(239, 68, 68, 0.3)'
                    bar_color = '#ef4444'
                else:  # Applied
                    gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                    shadow_color = 'rgba(102, 126, 234, 0.3)'
                    bar_color = '#667eea'
                
                st.markdown(f"""
                <div style='background: {gradient}; padding: 18px 20px; border-radius: 18px; 
                            margin-bottom: 14px; 
                            box-shadow: 0 6px 18px {shadow_color};
                            border: 2px solid rgba(255, 255, 255, 0.3);
                            transition: all 0.3s ease;
                            cursor: pointer;
                            position: relative;
                            overflow: hidden;'
                     onmouseover="this.style.transform='translateY(-4px) scale(1.02)'; this.style.boxShadow='0 12px 28px {shadow_color}';"
                     onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 6px 18px {shadow_color}';">
                    <div style='position: absolute; top: 0; right: 0; width: 100px; height: 100px;
                               background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
                               border-radius: 50%; transform: translate(30%, -30%);'></div>
                    <div style='position: relative; z-index: 1;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                            <div style='display: flex; align-items: center; gap: 10px;'>
                                <div style='background: rgba(255, 255, 255, 0.25); 
                                           width: 40px; height: 40px; border-radius: 50%;
                                           display: flex; align-items: center; justify-content: center;
                                           box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 -2px 6px rgba(0,0,0,0.1);
                                           backdrop-filter: blur(10px);
                                           border: 2px solid rgba(255, 255, 255, 0.3);
                                           position: relative;
                                           overflow: hidden;'>
                                    <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                                               background: linear-gradient(180deg, rgba(255,255,255,0.4) 0%, transparent 50%);
                                               border-radius: 50%;'></div>
                                    <span style='font-size: 20px; position: relative; z-index: 1;
                                               filter: drop-shadow(0 2px 3px rgba(0,0,0,0.2));'>{liquid_icon}</span>
                                </div>
                                <div>
                                    <div style='font-weight: 800; font-size: 14px; color: white; letter-spacing: -0.3px;
                                               text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                        {status_vn}
                                    </div>
                                    <div style='font-size: 11px; color: rgba(255, 255, 255, 0.85); font-weight: 600; margin-top: 2px;'>
                                        {percentage:.1f}% của tổng
                                    </div>
                                </div>
                            </div>
                            <div style='text-align: right;'>
                                <div style='font-size: 36px; font-weight: 900; 
                                           color: white;
                                           line-height: 1;
                                           text-shadow: 0 3px 8px rgba(0,0,0,0.25);'>
                                    {count}
                                </div>
                                <div style='font-size: 10px; color: rgba(255, 255, 255, 0.8); font-weight: 700; 
                                           margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;'>
                                    jobs
                                </div>
                            </div>
                        </div>
                        <div style='position: relative; background: rgba(255, 255, 255, 0.2); height: 8px; border-radius: 10px; 
                                   overflow: hidden; backdrop-filter: blur(10px);
                                   box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);'>
                            <div style='background: rgba(255, 255, 255, 0.8); height: 100%; width: {percentage}%; 
                                       border-radius: 10px;
                                       transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                                       box-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
                                       position: relative;'>
                                <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                                           background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
                                           animation: shimmer 2s infinite;'></div>
                            </div>
                        </div>
                    </div>
                </div>
                <style>
                @keyframes shimmer {{
                    0% {{ transform: translateX(-100%); }}
                    100% {{ transform: translateX(100%); }}
                }}
                </style>
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
