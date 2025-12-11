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
    Render modern form for adding new job with gradient design
    """
    # Initialize form counter to reset form after submission
    if "form_counter" not in st.session_state:
        st.session_state.form_counter = 0
    
    # Custom CSS for form
    st.markdown("""
    <style>
    /* Force CSS reload */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    .form-header {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(6, 182, 212, 0.15);
        border-radius: 20px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.75rem;
        box-shadow: 0 8px 32px rgba(6, 182, 212, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .form-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #06b6d4 100%);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .form-section {
        background: rgba(248, 250, 252, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        border: 2px solid rgba(6, 182, 212, 0.1);
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.06);
        transition: all 0.3s ease;
    }
    
    .form-section:hover {
        border-color: rgba(6, 182, 212, 0.25);
        box-shadow: 0 4px 16px rgba(6, 182, 212, 0.12);
        transform: translateY(-1px);
    }
    
    .form-section h3 {
        color: #0284c7;
        font-size: 15px;
        font-weight: 800;
        margin: 0 0 1.25rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Form container */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(6, 182, 212, 0.1) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 16px rgba(6, 182, 212, 0.08) !important;
    }
    
    /* All inputs styling */
    [data-testid="stForm"] input,
    [data-testid="stForm"] textarea {
        border-radius: 16px !important;
        border: 2px solid #e0f2fe !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.08) !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
        height: 48px !important;
    }
    
    /* Selectbox specific styling */
    [data-testid="stForm"] [data-baseweb="select"] > div {
        border-radius: 16px !important;
        border: 2px solid #e0f2fe !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.08) !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 48px !important;
        height: 48px !important;
    }
    
    /* Selectbox alignment fix */
    [data-testid="stForm"] .stSelectbox > div > div {
        display: flex !important;
        align-items: stretch !important;
    }
    
    [data-testid="stForm"] [data-baseweb="select"] {
        width: 100% !important;
    }
    
    /* Ensure selectbox value text is vertically centered */
    [data-testid="stForm"] [data-baseweb="select"] [role="button"] {
        display: flex !important;
        align-items: center !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-testid="stForm"] textarea {
        height: auto !important;
        min-height: 120px !important;
    }
    
    /* Force consistent height for all form fields */
    [data-testid="stForm"] .stTextInput,
    [data-testid="stForm"] .stSelectbox,
    [data-testid="stForm"] .stNumberInput,
    [data-testid="stForm"] .stDateInput {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
    
    /* Ensure inner divs align properly */
    [data-testid="stForm"] .stTextInput > div,
    [data-testid="stForm"] .stSelectbox > div,
    [data-testid="stForm"] .stNumberInput > div,
    [data-testid="stForm"] .stDateInput > div {
        width: 100% !important;
    }
    
    [data-testid="stForm"] .stTextInput > div > div,
    [data-testid="stForm"] .stSelectbox > div > div,
    [data-testid="stForm"] .stNumberInput > div > div,
    [data-testid="stForm"] .stDateInput > div > div {
        display: flex !important;
        align-items: center !important;
    }
    
    [data-testid="stForm"] .stTextArea {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
    
    /* Consistent labels */
    [data-testid="stForm"] label {
        font-weight: 600 !important;
        color: #475569 !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    [data-testid="stForm"] input:focus,
    [data-testid="stForm"] textarea:focus,
    [data-testid="stForm"] select:focus {
        border: 2px solid #06b6d4 !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.25) !important;
        outline: none !important;
    }
    
    /* Checkbox */
    [data-testid="stForm"] [data-testid="stCheckbox"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stForm"] [data-testid="stCheckbox"]:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%) !important;
    }
    
    /* Submit button - Orange/Red Gradient */
    [data-testid="stForm"] button[kind="primary"],
    [data-testid="stForm"] .stButton > button[type="submit"] {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 0.5px !important;
        padding: 1rem 2rem !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        height: auto !important;
    }
    
    [data-testid="stForm"] button[kind="primary"]:hover,
    [data-testid="stForm"] .stButton > button[type="submit"]:hover {
        background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 40px rgba(234, 88, 12, 0.5) !important;
    }
    
    [data-testid="stForm"] button[kind="primary"]:active,
    [data-testid="stForm"] .stButton > button[type="submit"]:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class='form-header'>
        <div style='position: relative; z-index: 1;'>
            <h1 style='font-size: 26px; font-weight: 800; margin: 0; letter-spacing: -0.5px; line-height: 1.2; color: #0891b2;'>Thêm Job Mới</h1>
            <p style='font-size: 14px; margin: 0.5rem 0 0 0; line-height: 1.4; color: #64748b; font-weight: 500;'>Điền thông tin công việc bạn muốn theo dõi</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use dynamic form key to reset form after submission
    form_key = f"add_job_form_{st.session_state.form_counter}"
    
    with st.form(form_key):
        # Basic Information Section
        st.markdown("<div class='form-section'><h3>📋 Thông tin cơ bản</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            company_name = st.text_input("Tên công ty *", placeholder="VD: FPT Software", key="company")
            job_title = st.text_input("Vị trí ứng tuyển *", placeholder="VD: Python Developer", key="jobtitle")
            location = st.text_input("Địa điểm", placeholder="VD: Hà Nội, Việt Nam", key="location")
        
        with col2:
            work_type = st.selectbox("Hình thức làm việc", ["Remote", "Hybrid", "Onsite"], key="worktype")
            source = st.text_input("Nguồn tuyển dụng", placeholder="VD: LinkedIn, TopCV...", key="source")
            current_status = st.selectbox("Trạng thái hiện tại", list(STATUS_COLORS.keys()), key="status")
        
        job_url = st.text_input("🔗 Link bài đăng", placeholder="https://...")
        job_description = st.text_area("📝 Mô tả công việc", height=120, placeholder="Nhập mô tả công việc...")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Date & Status Section
        st.markdown("<div class='form-section'><h3>📅 Thời gian</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            applied_date = st.date_input("Ngày nộp hồ sơ *", value=date.today())
        with col2:
            deadline = st.date_input("Deadline (tùy chọn)", value=None)
        with col3:
            is_favorite = st.checkbox("⭐ Đánh dấu yêu thích", value=False)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Salary Section
        st.markdown("<div class='form-section'><h3>💰 Mức lương</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            salary_min = st.number_input("Lương tối thiểu", min_value=0, value=0, step=1000000)
        with col2:
            salary_max = st.number_input("Lương tối đa", min_value=0, value=0, step=1000000)
        with col3:
            salary_currency = st.selectbox("Đơn vị tiền tệ", ["VND", "USD"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Contact Section
        st.markdown("<div class='form-section'><h3>👤 Thông tin liên hệ</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            contact_person = st.text_input("Người liên hệ", placeholder="Tên HR/Recruiter")
        with col2:
            contact_email = st.text_input("Email liên hệ", placeholder="hr@company.com")
        with col3:
            contact_phone = st.text_input("Số điện thoại", placeholder="0123456789")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Submit button with custom HTML styling
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stFormSubmitButton"] > button {
            background: rgba(6, 182, 212, 0.08) !important;
            backdrop-filter: blur(10px) !important;
            color: #0891b2 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            letter-spacing: 0.02em !important;
            padding: 0.875rem 2rem !important;
            border-radius: 16px !important;
            border: 2px solid rgba(6, 182, 212, 0.2) !important;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.1) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            height: 52px !important;
            width: 100% !important;
        }
        
        div[data-testid="stFormSubmitButton"] > button:hover {
            background: rgba(6, 182, 212, 0.15) !important;
            border-color: rgba(6, 182, 212, 0.4) !important;
            color: #0e7490 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(6, 182, 212, 0.2) !important;
        }
        
        div[data-testid="stFormSubmitButton"] > button:active {
            transform: translateY(0px) scale(0.98) !important;
            box-shadow: 0 2px 8px rgba(6, 182, 212, 0.15) !important;
        }
        
        div[data-testid="stFormSubmitButton"] > button p {
            font-size: 16px !important;
            font-weight: 700 !important;
            margin: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Thêm job mới", use_container_width=True)
        
        if submitted:
            if not company_name or not job_title:
                st.error("⚠️ Vui lòng nhập đầy đủ thông tin bắt buộc (*)")
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
                    
                    # Increment form counter to reset the form
                    st.session_state.form_counter += 1
                    
                    st.session_state.job_created_success = True
                    st.session_state.new_job_company = result['company_name']
                    st.session_state.new_job_title = result['job_title']
                    st.rerun()
                    
                except Exception as e:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                                color: white; padding: 1.5rem; border-radius: 16px; 
                                text-align: center; margin-top: 1rem;
                                box-shadow: 0 8px 24px rgba(239, 68, 68, 0.3);'>
                        <h3 style='margin: 0; font-size: 18px; font-weight: 700;'>
                            ⚠️ Đã xảy ra lỗi
                        </h3>
                        <p style='margin: 0.5rem 0 0 0; font-size: 14px; opacity: 0.95;'>
                            {str(e)}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

