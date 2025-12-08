"""
Dashboard Page - Overview and quick stats
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from frontend.services.analytics_service import analytics_service
from frontend.config.settings import STATUS_COLORS

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

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

st.title("💼 Job Tracker Application")
st.markdown("---")

try:
    # Get analytics data
    analytics = analytics_service.get_analytics()
    summary = analytics.get("summary", {})
    by_status = analytics.get("by_status", [])
    by_source = analytics.get("by_source", [])
    timeline = analytics.get("timeline", [])
    
    # Summary metrics
    st.subheader("📊 Tổng quan")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Tổng đơn ứng tuyển",
            value=summary.get("total_applications", 0),
            delta=None
        )
    
    with col2:
        st.metric(
            label="Đang xử lý",
            value=summary.get("active_applications", 0)
        )
    
    with col3:
        st.metric(
            label="Phỏng vấn",
            value=f"{summary.get('total_interviews', 0)} total",
            delta=f"{summary.get('upcoming_interviews', 0)} sắp tới"
        )
    
    with col4:
        st.metric(
            label="Offers",
            value=summary.get("offers_received", 0)
        )
    
    with col5:
        st.metric(
            label="Tỷ lệ thành công",
            value=f"{summary.get('success_rate', 0):.1f}%"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Thống kê theo trạng thái")
        if by_status:
            df_status = pd.DataFrame(by_status)
            # Filter out None/null status and ensure valid data
            df_status = df_status[df_status['status'].notna()]
            if not df_status.empty:
                df_status['count'] = pd.to_numeric(df_status['count'], errors='coerce').fillna(0).astype(int)
                st.bar_chart(df_status.set_index('status')['count'])
                
                # Show table
                with st.expander("Xem chi tiết"):
                    st.dataframe(df_status, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu hợp lệ")
        else:
            st.info("Chưa có dữ liệu")
    
    with col2:
        st.subheader("🌐 Thống kê theo nguồn")
        if by_source:
            df_source = pd.DataFrame(by_source)
            # Filter out None/null source and ensure valid data
            df_source = df_source[df_source['source'].notna()]
            if not df_source.empty:
                df_source['total_applications'] = pd.to_numeric(df_source['total_applications'], errors='coerce').fillna(0).astype(int)
                st.bar_chart(df_source.set_index('source')['total_applications'])
                
                # Show table
                with st.expander("Xem chi tiết"):
                    st.dataframe(df_source, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu hợp lệ")
        else:
            st.info("Chưa có dữ liệu")
    
    st.markdown("---")
    
    # Timeline
    st.subheader("📅 Timeline (6 tháng gần đây)")
    if timeline:
        df_timeline = pd.DataFrame(timeline)
        df_timeline = df_timeline.set_index('period')
        st.line_chart(df_timeline)
        
        with st.expander("Xem chi tiết"):
            st.dataframe(df_timeline, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu timeline")
    
    # Recent activity (placeholder)
    st.markdown("---")
    st.subheader("🕐 Hoạt động gần đây")
    st.info("Tính năng đang phát triển - sẽ hiển thị các cập nhật gần đây")
    
    # Status legend
    st.markdown("---")
    st.subheader("📌 Trạng thái Pipeline")
    
    # Show status with counts if we have data
    if by_status:
        status_dict = {item['status']: item['count'] for item in by_status}
        cols = st.columns(len(STATUS_COLORS))
        for idx, (status, icon) in enumerate(STATUS_COLORS.items()):
            with cols[idx]:
                count = status_dict.get(status, 0)
                st.markdown(f"{icon} **{status}**")
                st.metric("Số lượng", count)
    else:
        cols = st.columns(len(STATUS_COLORS))
        for idx, (status, icon) in enumerate(STATUS_COLORS.items()):
            with cols[idx]:
                st.markdown(f"{icon} **{status}**")

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
