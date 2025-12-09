"""
Job Detail Component
Displays detailed information for a single job
"""
import streamlit as st
from frontend.config.settings import STATUS_COLORS
from frontend.services.job_service import job_service


def render_job_detail(job_id: int):
    """
    Render detailed view of a job
    
    Args:
        job_id: ID of the job to display
    """
    try:
        job = job_service.get_job(job_id)
        
        # Header with back button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("⬅️ Quay lại"):
                st.session_state.selected_job_id = None
                st.rerun()
        with col2:
            favorite = "⭐" if job.get("is_favorite") else ""
            st.title(f"{favorite} {job['company_name']}")
        
        st.subheader(job['job_title'])
        
        # Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📋 Thông tin cơ bản")
            status_icon = STATUS_COLORS.get(job["current_status"], "⚪")
            st.markdown(f"**Trạng thái:** {status_icon} {job['current_status']}")
            if job.get("location"):
                st.markdown(f"**Địa điểm:** {job['location']}")
            if job.get("work_type"):
                st.markdown(f"**Hình thức:** {job['work_type']}")
            if job.get("source"):
                st.markdown(f"**Nguồn:** {job['source']}")
            if job.get("job_url"):
                st.markdown(f"**Link:** [Xem bài đăng]({job['job_url']})")
        
        with col2:
            st.markdown("### 📅 Thời gian")
            st.markdown(f"**Ngày nộp:** {job['applied_date']}")
            if job.get("deadline"):
                st.markdown(f"**Deadline:** {job['deadline']}")
            st.markdown(f"**Tạo lúc:** {job.get('created_at', 'N/A')}")
            if job.get("updated_at"):
                st.markdown(f"**Cập nhật:** {job['updated_at']}")
        
        with col3:
            st.markdown("### 💰 Lương & Liên hệ")
            if job.get("salary_min") and job.get("salary_max"):
                salary_min = int(float(job['salary_min']))
                salary_max = int(float(job['salary_max']))
                st.markdown(f"**Lương:** {salary_min:,} - {salary_max:,} {job.get('salary_currency', 'VND')}")
            if job.get("contact_person"):
                st.markdown(f"**Người liên hệ:** {job['contact_person']}")
            if job.get("contact_email"):
                st.markdown(f"**Email:** {job['contact_email']}")
            if job.get("contact_phone"):
                st.markdown(f"**SĐT:** {job['contact_phone']}")
        
        # Job description
        if job.get("job_description"):
            st.markdown("---")
            st.markdown("### 📝 Mô tả công việc")
            st.markdown(job["job_description"])
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ Sửa", use_container_width=True):
                st.info("Chức năng đang phát triển")
        with col2:
            if st.button("🗑️ Xóa", use_container_width=True):
                st.warning("Chức năng đang phát triển")
        with col3:
            if st.button("📊 Xem Analytics", use_container_width=True):
                st.info("Chức năng đang phát triển")
    
    except Exception as e:
        st.error(f"⚠️ Không thể tải chi tiết job: {str(e)}")
        if st.button("⬅️ Quay lại"):
            st.session_state.selected_job_id = None
            st.rerun()
