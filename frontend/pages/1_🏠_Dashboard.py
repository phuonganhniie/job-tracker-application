"""
Dashboard Page - Overview and quick stats
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from frontend.services.analytics_service import analytics_service
from frontend.config.settings import STATUS_COLORS

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

st.title("🏠 Dashboard")
st.markdown("Tổng quan về quá trình ứng tuyển của bạn")
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
            st.bar_chart(df_status.set_index('status')['count'])
            
            # Show table
            with st.expander("Xem chi tiết"):
                st.dataframe(df_status, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu")
    
    with col2:
        st.subheader("🌐 Thống kê theo nguồn")
        if by_source:
            df_source = pd.DataFrame(by_source)
            st.bar_chart(df_source.set_index('source')['total_applications'])
            
            # Show table
            with st.expander("Xem chi tiết"):
                st.dataframe(df_source, use_container_width=True)
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

except Exception as e:
    st.error(f"⚠️ Lỗi khi tải dữ liệu: {str(e)}")
    st.info("Vui lòng đảm bảo backend đang chạy!")
