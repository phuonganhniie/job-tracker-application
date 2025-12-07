"""
Jobs Page - Job management
"""
import streamlit as st
import pandas as pd
from datetime import date
from frontend.services.job_service import job_service
from frontend.config.settings import STATUS_COLORS

st.set_page_config(page_title="Jobs", page_icon="💼", layout="wide")

st.title("💼 Quản lý Jobs")
st.markdown("Theo dõi các công việc đã/đang ứng tuyển")
st.markdown("---")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Bộ lọc")
    
    search_keyword = st.text_input("Tìm kiếm (công ty/vị trí)")
    
    status_filter = st.selectbox(
        "Trạng thái",
        ["Tất cả"] + list(STATUS_COLORS.keys())
    )
    
    source_filter = st.text_input("Nguồn (LinkedIn, Indeed...)")
    
    work_type_filter = st.selectbox(
        "Hình thức làm việc",
        ["Tất cả", "Remote", "Hybrid", "Onsite"]
    )
    
    is_favorite = st.checkbox("Chỉ yêu thích ⭐")
    
    st.markdown("---")
    
    if st.button("🔄 Làm mới", use_container_width=True):
        st.rerun()

# Main content tabs
tab1, tab2 = st.tabs(["📋 Danh sách Jobs", "➕ Thêm Job mới"])

# Tab 1: Job list
with tab1:
    try:
        # Build filters
        filters = {}
        if status_filter != "Tất cả":
            filters["status"] = status_filter
        if source_filter:
            filters["source"] = source_filter
        if work_type_filter != "Tất cả":
            filters["work_type"] = work_type_filter
        if is_favorite:
            filters["is_favorite"] = True
        if search_keyword:
            filters["company_name"] = search_keyword
        
        # Get jobs
        response = job_service.get_jobs(page=1, page_size=50, filters=filters)
        jobs = response.get("items", [])
        total = response.get("total", 0)
        
        st.info(f"Tìm thấy **{total}** jobs")
        
        if jobs:
            # Display as cards
            for job in jobs:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        status_icon = STATUS_COLORS.get(job["current_status"], "⚪")
                        favorite = "⭐" if job.get("is_favorite") else ""
                        st.markdown(f"### {favorite} {job['company_name']}")
                        st.markdown(f"**{job['job_title']}**")
                        if job.get("location"):
                            st.caption(f"📍 {job['location']}")
                    
                    with col2:
                        st.markdown(f"{status_icon} **{job['current_status']}**")
                        if job.get("source"):
                            st.caption(f"Nguồn: {job['source']}")
                    
                    with col3:
                        st.caption(f"Nộp: {job['applied_date']}")
                        if job.get("salary_min") and job.get("salary_max"):
                            st.caption(f"💰 {job['salary_min']}-{job['salary_max']} {job.get('salary_currency', 'VND')}")
                    
                    with col4:
                        if st.button("👁️", key=f"view_{job['id']}"):
                            st.session_state.selected_job_id = job['id']
                            st.switch_page("pages/2_💼_Jobs.py")
                    
                    st.markdown("---")
        else:
            st.info("Chưa có job nào. Hãy thêm job mới!")
    
    except Exception as e:
        st.error(f"⚠️ Lỗi: {str(e)}")

# Tab 2: Add new job
with tab2:
    st.subheader("Thêm Job mới")
    
    with st.form("add_job_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Tên công ty *", placeholder="VD: FPT Software")
            job_title = st.text_input("Vị trí ứng tuyển *", placeholder="VD: Python Developer")
            location = st.text_input("Địa điểm", placeholder="VD: Hà Nội")
            work_type = st.selectbox("Hình thức", ["Remote", "Hybrid", "Onsite"])
            source = st.text_input("Nguồn", placeholder="VD: LinkedIn")
        
        with col2:
            applied_date = st.date_input("Ngày nộp hồ sơ *", value=date.today())
            deadline = st.date_input("Deadline (nếu có)", value=None)
            current_status = st.selectbox("Trạng thái", list(STATUS_COLORS.keys()))
            is_favorite = st.checkbox("Đánh dấu yêu thích ⭐")
        
        job_url = st.text_input("Link bài đăng", placeholder="https://...")
        job_description = st.text_area("Mô tả công việc", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            salary_min = st.number_input("Lương tối thiểu", min_value=0, value=0)
        with col2:
            salary_max = st.number_input("Lương tối đa", min_value=0, value=0)
        
        salary_currency = st.selectbox("Đơn vị", ["VND", "USD", "EUR"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            contact_person = st.text_input("Người liên hệ")
        with col2:
            contact_email = st.text_input("Email liên hệ")
        with col3:
            contact_phone = st.text_input("SĐT liên hệ")
        
        submitted = st.form_submit_button("✅ Thêm Job", use_container_width=True)
        
        if submitted:
            if not company_name or not job_title:
                st.error("Vui lòng nhập đầy đủ thông tin bắt buộc (*)")
            else:
                try:
                    job_data = {
                        "company_name": company_name,
                        "job_title": job_title,
                        "job_url": job_url or None,
                        "job_description": job_description or None,
                        "location": location or None,
                        "work_type": work_type,
                        "salary_min": salary_min if salary_min > 0 else None,
                        "salary_max": salary_max if salary_max > 0 else None,
                        "salary_currency": salary_currency,
                        "source": source or None,
                        "contact_person": contact_person or None,
                        "contact_email": contact_email or None,
                        "contact_phone": contact_phone or None,
                        "current_status": current_status,
                        "applied_date": str(applied_date),
                        "deadline": str(deadline) if deadline else None,
                        "is_favorite": is_favorite
                    }
                    
                    result = job_service.create_job(job_data)
                    st.success(f"✅ Đã thêm job: {result['company_name']} - {result['job_title']}")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"⚠️ Lỗi: {str(e)}")
