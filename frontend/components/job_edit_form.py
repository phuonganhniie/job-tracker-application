"""
Job Edit Form Component
Modern liquid-style form for editing job details
"""
import streamlit as st
from datetime import date
from typing import Dict, Any
from frontend.services.job_service import job_service
from frontend.config.settings import STATUS_COLORS


def render_job_edit_form(job: Dict[str, Any], job_id: int):
    """
    Render modern edit form for job details with liquid styling
    
    Args:
        job: Current job data dictionary
        job_id: ID of the job being edited
    """
    # Comprehensive CSS for modern liquid-style form
    st.markdown("""
    <style>
    /* ===== GLOBAL FORM STYLING ===== */
    [data-testid="stForm"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%) !important;
        border-radius: 24px !important;
        padding: 2rem !important;
        border: 1px solid rgba(6, 182, 212, 0.15) !important;
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.05),
            0 10px 15px -3px rgba(0, 0, 0, 0.08),
            0 20px 25px -5px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* ===== ALL INPUT FIELDS - UNIFIED HEIGHT ===== */
    [data-testid="stForm"] .stTextInput > div > div,
    [data-testid="stForm"] .stSelectbox > div > div,
    [data-testid="stForm"] .stNumberInput > div > div,
    [data-testid="stForm"] .stDateInput > div > div {
        min-height: 48px !important;
    }
    
    /* ===== TEXT INPUT STYLING ===== */
    [data-testid="stForm"] .stTextInput input {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        height: 52px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stForm"] .stTextInput input:hover {
        border-color: #94a3b8 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    
    [data-testid="stForm"] .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.12),
            0 4px 12px rgba(102, 126, 234, 0.15) !important;
        outline: none !important;
    }
    
    /* ===== SELECT/DROPDOWN STYLING ===== */
    [data-testid="stForm"] .stSelectbox [data-baseweb="select"] > div {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        min-height: 52px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stForm"] .stSelectbox [data-baseweb="select"] > div:hover {
        border-color: #94a3b8 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    
    [data-testid="stForm"] .stSelectbox [data-baseweb="select"] > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.12),
            0 4px 12px rgba(102, 126, 234, 0.15) !important;
    }
    
    [data-testid="stForm"] .stSelectbox [data-baseweb="select"] [role="button"] {
        padding: 12px 16px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
    }
    
    /* ===== NUMBER INPUT STYLING ===== */
    [data-testid="stForm"] .stNumberInput input {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        height: 52px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stForm"] .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.12),
            0 4px 12px rgba(102, 126, 234, 0.15) !important;
    }
    
    [data-testid="stForm"] .stNumberInput [data-baseweb="input"] {
        border-radius: 14px !important;
    }
    
    /* ===== DATE INPUT STYLING ===== */
    [data-testid="stForm"] .stDateInput > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        min-height: 52px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stForm"] .stDateInput > div > div:hover {
        border-color: #94a3b8 !important;
    }
    
    [data-testid="stForm"] .stDateInput > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.12),
            0 4px 12px rgba(102, 126, 234, 0.15) !important;
    }
    
    [data-testid="stForm"] .stDateInput input {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        padding: 14px 16px !important;
    }
    
    /* ===== TEXTAREA STYLING ===== */
    [data-testid="stForm"] .stTextArea textarea {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 16px 18px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        line-height: 1.6 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        resize: vertical !important;
    }
    
    [data-testid="stForm"] .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.12),
            0 4px 12px rgba(102, 126, 234, 0.15) !important;
    }
    
    /* ===== LABELS STYLING ===== */
    [data-testid="stForm"] .stTextInput label,
    [data-testid="stForm"] .stSelectbox label,
    [data-testid="stForm"] .stNumberInput label,
    [data-testid="stForm"] .stDateInput label,
    [data-testid="stForm"] .stTextArea label {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.01em !important;
    }
    
    /* ===== CHECKBOX STYLING ===== */
    [data-testid="stForm"] .stCheckbox {
        background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%) !important;
        border: 2px solid #fde047 !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-top: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stForm"] .stCheckbox:hover {
        border-color: #facc15 !important;
        box-shadow: 0 4px 12px rgba(250, 204, 21, 0.2) !important;
    }
    
    [data-testid="stForm"] .stCheckbox label {
        font-weight: 600 !important;
        color: #854d0e !important;
    }
    
    /* ===== FORM SUBMIT BUTTONS ===== */
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
        border-radius: 14px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 14px 28px !important;
        height: 52px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.02em !important;
    }
    
    /* Primary button (Save) */
    [data-testid="stForm"] [data-testid="stFormSubmitButton"]:first-of-type button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
    }
    
    [data-testid="stForm"] [data-testid="stFormSubmitButton"]:first-of-type button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.45) !important;
    }
    
    /* Secondary button (Cancel) */
    [data-testid="stForm"] [data-testid="stFormSubmitButton"]:last-of-type button {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        color: #64748b !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stForm"] [data-testid="stFormSubmitButton"]:last-of-type button:hover {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        border-color: #cbd5e1 !important;
        transform: translateY(-1px) !important;
    }
    
    /* ===== COLUMN ALIGNMENT FIX ===== */
    [data-testid="stForm"] [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }
    
    [data-testid="stForm"] [data-testid="column"] > div {
        flex: 1 !important;
    }
    
    /* ===== SECTION CARDS ===== */
    .form-section-header {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #0ea5e9;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .form-section-header h3 {
        margin: 0;
        color: #0369a1;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .form-section-header .icon {
        font-size: 20px;
    }
    
    /* ===== RESPONSIVE GRID ===== */
    @media (max-width: 768px) {
        [data-testid="stForm"] [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Form header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px; padding: 1.75rem 2rem; margin-bottom: 1.5rem;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.35);'>
        <h2 style='color: white; font-size: 26px; font-weight: 800; margin: 0; letter-spacing: -0.5px;'>
            ✏️ Chỉnh sửa thông tin Job
        </h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 0.5rem 0 0 0;'>
            Cập nhật thông tin công việc bên dưới
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("edit_job_form", clear_on_submit=False):
        
        # ===== SECTION 1: BASIC INFO =====
        st.markdown("""
        <div class='form-section-header'>
            <span class='icon'>📋</span>
            <h3>Thông tin cơ bản</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            edit_company = st.text_input(
                "🏢 Tên công ty *", 
                value=job.get('company_name', ''),
                placeholder="VD: FPT Software"
            )
            edit_location = st.text_input(
                "📍 Địa điểm", 
                value=job.get('location', '') or '',
                placeholder="VD: Hà Nội, Việt Nam"
            )
            edit_source = st.text_input(
                "🔗 Nguồn tuyển dụng", 
                value=job.get('source', '') or '',
                placeholder="VD: LinkedIn, TopCV..."
            )
        
        with col2:
            edit_title = st.text_input(
                "💼 Vị trí ứng tuyển *", 
                value=job.get('job_title', ''),
                placeholder="VD: Python Developer"
            )
            work_type_options = ["Remote", "Hybrid", "Onsite"]
            edit_work_type = st.selectbox(
                "🏠 Hình thức làm việc", 
                work_type_options,
                index=work_type_options.index(job.get('work_type', 'Remote')) if job.get('work_type') in work_type_options else 0
            )
            status_options = ["Applied", "Screening", "Interview", "Offer", "Hired", "Rejected"]
            edit_status = st.selectbox(
                "📊 Trạng thái hiện tại",
                status_options,
                index=status_options.index(job.get('current_status', 'Applied')) if job.get('current_status') in status_options else 0
            )
        
        edit_url = st.text_input(
            "🌐 Link bài đăng tuyển dụng", 
            value=job.get('job_url', '') or '',
            placeholder="https://..."
        )
        
        # ===== SECTION 2: TIME & PRIORITY =====
        st.markdown("""
        <div class='form-section-header'>
            <span class='icon'>📅</span>
            <h3>Thời gian & Ưu tiên</h3>
        </div>
        """, unsafe_allow_html=True)
        
        time_col1, time_col2, time_col3 = st.columns(3, gap="medium")
        
        with time_col1:
            try:
                applied_val = date.fromisoformat(str(job.get('applied_date', date.today()))[:10])
            except:
                applied_val = date.today()
            edit_applied_date = st.date_input("📆 Ngày nộp hồ sơ *", value=applied_val)
        
        with time_col2:
            deadline_val = None
            if job.get('deadline'):
                try:
                    deadline_val = date.fromisoformat(str(job['deadline'])[:10])
                except:
                    pass
            edit_deadline = st.date_input("⏰ Deadline", value=deadline_val)
        
        with time_col3:
            edit_favorite = st.checkbox("⭐ Đánh dấu yêu thích", value=job.get('is_favorite', False))
        
        # ===== SECTION 3: SALARY =====
        st.markdown("""
        <div class='form-section-header'>
            <span class='icon'>💰</span>
            <h3>Mức lương</h3>
        </div>
        """, unsafe_allow_html=True)
        
        sal_col1, sal_col2, sal_col3 = st.columns(3, gap="medium")
        
        with sal_col1:
            edit_salary_min = st.number_input(
                "💵 Lương tối thiểu", 
                min_value=0, 
                value=int(float(job.get('salary_min') or 0)), 
                step=1000000,
                format="%d"
            )
        
        with sal_col2:
            edit_salary_max = st.number_input(
                "💵 Lương tối đa", 
                min_value=0, 
                value=int(float(job.get('salary_max') or 0)), 
                step=1000000,
                format="%d"
            )
        
        with sal_col3:
            currency_options = ["VND", "USD"]
            edit_currency = st.selectbox(
                "💱 Đơn vị tiền tệ",
                currency_options,
                index=currency_options.index(job.get('salary_currency', 'VND')) if job.get('salary_currency') in currency_options else 0
            )
        
        # ===== SECTION 4: CONTACT =====
        st.markdown("""
        <div class='form-section-header'>
            <span class='icon'>👤</span>
            <h3>Thông tin liên hệ</h3>
        </div>
        """, unsafe_allow_html=True)
        
        contact_col1, contact_col2, contact_col3 = st.columns(3, gap="medium")
        
        with contact_col1:
            edit_contact_person = st.text_input(
                "👤 Người liên hệ", 
                value=job.get('contact_person', '') or '',
                placeholder="Tên HR/Recruiter"
            )
        
        with contact_col2:
            edit_contact_email = st.text_input(
                "📧 Email liên hệ", 
                value=job.get('contact_email', '') or '',
                placeholder="hr@company.com"
            )
        
        with contact_col3:
            edit_contact_phone = st.text_input(
                "📱 Số điện thoại", 
                value=job.get('contact_phone', '') or '',
                placeholder="0123 456 789"
            )
        
        # ===== SECTION 5: DESCRIPTION =====
        st.markdown("""
        <div class='form-section-header'>
            <span class='icon'>📝</span>
            <h3>Mô tả công việc</h3>
        </div>
        """, unsafe_allow_html=True)
        
        edit_description = st.text_area(
            "Nhập mô tả chi tiết về công việc...", 
            value=job.get('job_description', '') or '', 
            height=180,
            placeholder="Mô tả chi tiết về yêu cầu, trách nhiệm, quyền lợi..."
        )
        
        # ===== ACTION BUTTONS =====
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_spacer = st.columns([1.2, 1, 2])
        
        with btn_col1:
            submit_edit = st.form_submit_button(
                "💾 Lưu thay đổi", 
                use_container_width=True,
                type="primary"
            )
        
        with btn_col2:
            cancel_edit = st.form_submit_button(
                "❌ Hủy bỏ", 
                use_container_width=True
            )
        
        # Handle form submission
        if submit_edit:
            if not edit_company or not edit_title:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                            border: 2px solid #fecaca; border-radius: 14px; padding: 1rem 1.25rem;
                            margin-top: 1rem; display: flex; align-items: center; gap: 0.75rem;'>
                    <span style='font-size: 20px;'>⚠️</span>
                    <span style='color: #991b1b; font-weight: 600;'>
                        Vui lòng nhập đầy đủ thông tin bắt buộc (*)
                    </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                try:
                    update_data = {
                        "company_name": edit_company,
                        "job_title": edit_title,
                        "job_url": edit_url or None,
                        "job_description": edit_description or None,
                        "location": edit_location or None,
                        "work_type": edit_work_type,
                        "salary_min": edit_salary_min if edit_salary_min > 0 else None,
                        "salary_max": edit_salary_max if edit_salary_max > 0 else None,
                        "salary_currency": edit_currency,
                        "source": edit_source or None,
                        "contact_person": edit_contact_person or None,
                        "contact_email": edit_contact_email or None,
                        "contact_phone": edit_contact_phone or None,
                        "current_status": edit_status,
                        "applied_date": str(edit_applied_date),
                        "deadline": str(edit_deadline) if edit_deadline else None,
                        "is_favorite": edit_favorite
                    }
                    job_service.update_job(job_id, update_data)
                    st.session_state.edit_mode = False
                    
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                                border: 2px solid #6ee7b7; border-radius: 14px; padding: 1rem 1.25rem;
                                margin-top: 1rem; display: flex; align-items: center; gap: 0.75rem;'>
                        <span style='font-size: 20px;'>✅</span>
                        <span style='color: #065f46; font-weight: 600;'>
                            Cập nhật thành công! Đang tải lại...
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
                    
                except Exception as e:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                                border: 2px solid #fecaca; border-radius: 14px; padding: 1rem 1.25rem;
                                margin-top: 1rem;'>
                        <div style='display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;'>
                            <span style='font-size: 20px;'>❌</span>
                            <span style='color: #991b1b; font-weight: 700;'>Lỗi khi cập nhật</span>
                        </div>
                        <p style='color: #7f1d1d; margin: 0; font-size: 14px;'>{str(e)}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        if cancel_edit:
            st.session_state.edit_mode = False
            st.rerun()
