"""
Job Form Component
Form for adding new jobs
"""
import streamlit as st
from datetime import date
from frontend.config.settings import STATUS_COLORS
from frontend.services.job_service import job_service


def render_job_form():
    """
    Render form for adding new job
    """
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
