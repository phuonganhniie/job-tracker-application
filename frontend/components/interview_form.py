"""
Interview Form Component - Add/Edit interview form
"""
import streamlit as st
from typing import Dict, Optional
from datetime import datetime, date, time
from frontend.services.interview_service import interview_service
from frontend.services.job_service import job_service


# Interview types
INTERVIEW_TYPES = [
    "Phone Screening",
    "Video Call", 
    "Technical Test",
    "Onsite Interview",
    "Final Round",
    "HR Interview"
]

# Result options
RESULT_OPTIONS = ["Pending", "Passed", "Failed"]


def render_interview_form(
    job_id: Optional[int] = None,
    interview: Optional[Dict] = None,
    on_success: Optional[callable] = None
):
    """
    Render interview add/edit form
    
    Args:
        job_id: Pre-selected job ID (for adding from job detail)
        interview: Existing interview data (for editing)
        on_success: Callback after successful save
    """
    is_edit = interview is not None
    
    # Back button
    col1, col2 = st.columns([0.5, 5.5], gap="medium")
    with col1:
        if st.button("⬅️", key="form_back_btn", use_container_width=True, help="Quay lại"):
            if "editing_interview_id" in st.session_state:
                del st.session_state.editing_interview_id
            if "adding_interview" in st.session_state:
                del st.session_state.adding_interview
            st.rerun()
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Apply form CSS - Liquid glassmorphism style
    st.markdown("""
        <style>
        @keyframes form-fade-in {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes gradient-rotate {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .interview-form-container {
            background: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.95) 0%, 
                rgba(248, 250, 252, 0.9) 50%,
                rgba(243, 244, 246, 0.85) 100%);
            backdrop-filter: blur(30px) saturate(180%);
            border-radius: 28px;
            padding: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 
                0 20px 50px rgba(0, 0, 0, 0.08),
                0 10px 20px rgba(0, 0, 0, 0.04),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            animation: form-fade-in 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .interview-form-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, 
                #667eea, 
                #764ba2, 
                #f093fb, 
                #667eea);
            background-size: 200% 100%;
            animation: gradient-rotate 4s linear infinite;
        }
        
        .form-section-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin: 2rem 0 1.25rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid rgba(102, 126, 234, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            position: relative;
        }
        
        .form-section-title:first-of-type {
            margin-top: 0;
        }
        
        .form-section-title::before {
            content: '';
            width: 5px;
            height: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 3px;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        /* Enhanced input styling */
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input,
        .stNumberInput > div > div > input {
            border-radius: 14px !important;
            border: 1.5px solid rgba(226, 232, 240, 0.8) !important;
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
        }
        
        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stDateInput > div > div > input:focus,
        .stTimeInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 1) !important;
        }
        
        .stTextArea > div > div > textarea {
            min-height: 120px !important;
            line-height: 1.6 !important;
            resize: vertical !important;
        }
        
        /* Placeholder styling */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #9ca3af !important;
            opacity: 1 !important;
        }
        
        /* Label styling */
        .stSelectbox > label,
        .stTextInput > label,
        .stTextArea > label,
        .stDateInput > label,
        .stTimeInput > label,
        .stNumberInput > label {
            font-weight: 600 !important;
            color: #374151 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Form buttons */
        .stForm button {
            border-radius: 16px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        }
        
        .stForm button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12) !important;
        }
        
        .stForm button[kind="primary"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3) !important;
        }
        
        .stForm button[kind="primary"]:hover {
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4) !important;
            filter: brightness(1.1);
        }
        
        /* Disabled inputs */
        input:disabled,
        textarea:disabled,
        select:disabled {
            background: rgba(243, 244, 246, 0.8) !important;
            cursor: not-allowed !important;
            opacity: 0.7 !important;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .interview-form-container {
                padding: 1.5rem;
                border-radius: 20px;
            }
            
            .form-section-title {
                font-size: 0.8rem;
                margin: 1.5rem 0 1rem 0;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
            backdrop-filter: blur(20px);
            padding: 1.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        ">
            <h3 style="
                margin: 0;
                color: white;
                font-size: 1.5rem;
                font-weight: 800;
                display: flex;
                align-items: center;
                gap: 0.75rem;
                letter-spacing: -0.02em;
            ">
                <span style="font-size: 1.75rem;">{'✏️' if is_edit else '➕'}</span>
                {'Chỉnh sửa phỏng vấn' if is_edit else 'Thêm phỏng vấn mới'}
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="interview_form", clear_on_submit=not is_edit):
        # Section 1: Job Selection
        st.markdown('<div class="form-section-title">🏢 Công việc</div>', unsafe_allow_html=True)
        
        # Get jobs for dropdown
        try:
            jobs_response = job_service.get_jobs(page_size=100)
            jobs = jobs_response.get("items", [])
            job_options = {f"{j['company_name']} - {j['job_title']}": j['id'] for j in jobs}
        except:
            jobs = []
            job_options = {}
        
        if is_edit:
            # Show job info (read-only for edit)
            selected_job_id = interview.get("job_id")
            job_display = next(
                (k for k, v in job_options.items() if v == selected_job_id), 
                "Unknown Job"
            )
            st.text_input("Công việc", value=job_display, disabled=True)
        else:
            # Job selection dropdown
            if job_id and job_id in job_options.values():
                default_job = next((k for k, v in job_options.items() if v == job_id), None)
                default_idx = list(job_options.keys()).index(default_job) if default_job else 0
            else:
                default_idx = 0
            
            selected_job_name = st.selectbox(
                "Chọn công việc *",
                options=list(job_options.keys()),
                index=default_idx if job_options else 0,
                placeholder="Chọn công việc..."
            )
            selected_job_id = job_options.get(selected_job_name) if selected_job_name else None
        
        # Section 2: Interview Details
        st.markdown('<div class="form-section-title">📋 Thông tin phỏng vấn</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            round_number = st.number_input(
                "Vòng phỏng vấn *",
                min_value=1,
                max_value=10,
                value=interview.get("round_number", 1) if is_edit else 1,
                step=1,
                help="Nhập số vòng phỏng vấn (1-10)"
            )
        
        with col2:
            interview_type = st.selectbox(
                "Loại phỏng vấn *",
                options=INTERVIEW_TYPES,
                index=INTERVIEW_TYPES.index(interview.get("interview_type")) 
                    if is_edit and interview.get("interview_type") in INTERVIEW_TYPES 
                    else 0,
                help="Chọn loại hình phỏng vấn"
            )
        
        # Section 3: Schedule
        st.markdown('<div class="form-section-title">📅 Lịch hẹn</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            # Parse existing date
            if is_edit and interview.get("scheduled_date"):
                try:
                    existing_dt = datetime.fromisoformat(
                        interview["scheduled_date"].replace("Z", "+00:00")
                    )
                    default_date = existing_dt.date()
                    default_time = existing_dt.time()
                except:
                    default_date = date.today()
                    default_time = time(9, 0)
            else:
                default_date = date.today()
                default_time = time(9, 0)
            
            scheduled_date = st.date_input(
                "Ngày phỏng vấn *",
                value=default_date,
                help="Chọn ngày diễn ra phỏng vấn"
            )
        
        with col2:
            scheduled_time = st.time_input(
                "Giờ phỏng vấn *",
                value=default_time,
                help="Chọn giờ bắt đầu phỏng vấn"
            )
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            location = st.text_input(
                "Location địa điểm",
                value=interview.get("location", "") if is_edit else "",
                placeholder="VD: Tầng 5, Tòa nhà ABC...",
                help="Nhập địa điểm phỏng vấn"
            )
        
        with col2:
            meeting_link = st.text_input(
                "Link meeting",
                value=interview.get("meeting_link", "") if is_edit else "",
                placeholder="https://meet.google.com/...",
                help="Nhập link cuộc họp online"
            )
        
        # Section 4: Interviewer
        st.markdown('<div class="form-section-title">👤 Người phỏng vấn</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            interviewer_name = st.text_input(
                "Tên người phỏng vấn",
                value=interview.get("interviewer_name", "") if is_edit else "",
                placeholder="VD: Nguyễn Văn A",
                help="Nhập tên người phỏng vấn"
            )
        
        with col2:
            interviewer_title = st.text_input(
                "Chức vụ",
                value=interview.get("interviewer_title", "") if is_edit else "",
                placeholder="VD: Senior Engineer, HR Manager...",
                help="Nhập chức vụ của người phỏng vấn"
            )
        
        # Section 5: Notes & Result (for edit mode)
        st.markdown('<div class="form-section-title">📝 Ghi chú & Kết quả</div>', unsafe_allow_html=True)
        
        preparation_notes = st.text_area(
            "Ghi chú chuẩn bị",
            value=interview.get("preparation_notes", "") if is_edit else "",
            placeholder="Những điều cần chuẩn bị, câu hỏi dự kiến...",
            height=100,
            help="Ghi chú các nội dung cần chuẩn bị cho phỏng vấn"
        )
        
        if is_edit:
            col1, col2 = st.columns([1, 1.5], gap="medium")
            
            with col1:
                result = st.selectbox(
                    "Kết quả",
                    options=RESULT_OPTIONS,
                    index=RESULT_OPTIONS.index(interview.get("result")) 
                        if interview.get("result") in RESULT_OPTIONS 
                        else 0,
                    help="Chọn kết quả phỏng vấn"
                )
            
            with col2:
                feedback = st.text_area(
                    "Feedback",
                    value=interview.get("feedback", "") if is_edit else "",
                    placeholder="Nhận xét sau phỏng vấn...",
                    height=100,
                    help="Ghi chú nhận xét sau phỏng vấn"
                )
        
        # Submit buttons
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1.5, 1.5, 3], gap="medium")
        
        with col1:
            submitted = st.form_submit_button(
                "💾 Lưu" if is_edit else "➕ Thêm mới",
                use_container_width=True,
                type="primary",
                help="Lưu thông tin phỏng vấn"
            )
        
        with col2:
            if st.form_submit_button("❌ Hủy", use_container_width=True, help="Hủy và quay lại"):
                if "editing_interview_id" in st.session_state:
                    del st.session_state.editing_interview_id
                if "adding_interview" in st.session_state:
                    del st.session_state.adding_interview
                st.rerun()
        
        if submitted:
            # Validate required fields
            if not selected_job_id:
                st.error("❌ Vui lòng chọn công việc!")
                return
            
            # Combine date and time
            scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)
            
            # Prepare data
            interview_data = {
                "job_id": selected_job_id,
                "round_number": round_number,
                "interview_type": interview_type,
                "scheduled_date": scheduled_datetime.isoformat(),
                "location": location if location else None,
                "meeting_link": meeting_link if meeting_link else None,
                "interviewer_name": interviewer_name if interviewer_name else None,
                "interviewer_title": interviewer_title if interviewer_title else None,
                "preparation_notes": preparation_notes if preparation_notes else None,
            }
            
            if is_edit:
                interview_data["result"] = result
                interview_data["feedback"] = feedback if feedback else None
            
            try:
                if is_edit:
                    response = interview_service.update_interview(interview["id"], interview_data)
                    st.success("✅ Cập nhật phỏng vấn thành công!")
                else:
                    response = interview_service.create_interview(interview_data)
                    st.success("✅ Thêm phỏng vấn mới thành công!")
                
                # Clear states
                if "editing_interview_id" in st.session_state:
                    del st.session_state.editing_interview_id
                if "adding_interview" in st.session_state:
                    del st.session_state.adding_interview
                
                if on_success:
                    on_success()
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")


def render_result_update_form(interview: Dict, on_success: Optional[callable] = None):
    """Quick form to update interview result with enhanced styling"""
    
    # Back button
    col1, col2 = st.columns([0.5, 5.5], gap="medium")
    with col1:
        if st.button("⬅️", key="result_back_btn", use_container_width=True, help="Quay lại"):
            if "update_interview_id" in st.session_state:
                del st.session_state.update_interview_id
            st.rerun()
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(37, 99, 235, 0.95));
            backdrop-filter: blur(20px);
            padding: 1.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        ">
            <h3 style="
                margin: 0;
                color: white;
                font-size: 1.5rem;
                font-weight: 800;
                display: flex;
                align-items: center;
                gap: 0.75rem;
                letter-spacing: -0.02em;
            ">
                <span style="font-size: 1.75rem;">📊</span>
                Cập nhật kết quả phỏng vấn
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(249, 250, 251, 0.95), rgba(243, 244, 246, 0.9));
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(226, 232, 240, 0.5);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        ">
            <div style="font-weight: 700; color: #1f2937; font-size: 1.1rem; margin-bottom: 0.5rem;">
                Round {interview.get('round_number')} — {interview.get('interview_type', 'Interview')}
            </div>
            <div style="color: #6b7280; display: flex; align-items: center; gap: 0.5rem;">
                <span>📅</span>
                <span>{interview.get('scheduled_date', 'N/A')[:10]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="result_form"):
        result = st.selectbox(
            "Kết quả *",
            options=RESULT_OPTIONS,
            index=RESULT_OPTIONS.index(interview.get("result")) 
                if interview.get("result") in RESULT_OPTIONS 
                else 0,
            help="Chọn kết quả phỏng vấn"
        )
        
        feedback = st.text_area(
            "Feedback / Nhận xét",
            value=interview.get("feedback", ""),
            placeholder="Những điểm tốt, điểm cần cải thiện...",
            height=150,
            help="Ghi chú nhận xét và phản hồi sau phỏng vấn"
        )
        
        col1, col2, col3 = st.columns([1.5, 1.5, 3], gap="medium")
        
        with col1:
            if st.form_submit_button("💾 Cập nhật", use_container_width=True, type="primary", help="Cập nhật kết quả phỏng vấn"):
                try:
                    interview_service.update_interview_result(
                        interview["id"], 
                        result, 
                        feedback if feedback else None
                    )
                    st.success("✅ Đã cập nhật kết quả!")
                    
                    if "update_interview_id" in st.session_state:
                        del st.session_state.update_interview_id
                    
                    if on_success:
                        on_success()
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        
        with col2:
            if st.form_submit_button("❌ Hủy", use_container_width=True, help="Hủy và quay lại"):
                if "update_interview_id" in st.session_state:
                    del st.session_state.update_interview_id
                st.rerun()
