"""
Interview Detail Component - View/Edit single interview
"""
import streamlit as st
from typing import Dict, Optional
from datetime import datetime
from frontend.services.interview_service import interview_service
from frontend.services.job_service import job_service


def format_datetime_display(dt_str: str) -> str:
    """Format datetime for display"""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y lúc %H:%M")
    except:
        return "N/A"


def get_result_badge(result: Optional[str]) -> str:
    """Get HTML badge for result with premium styling"""
    if result == "Passed":
        return '<span style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 8px 20px; border-radius: 24px; font-weight: 700; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 6px;"><span style="font-size: 1.1rem;">✅</span>Passed</span>'
    elif result == "Failed":
        return '<span style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 8px 20px; border-radius: 24px; font-weight: 700; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 6px;"><span style="font-size: 1.1rem;">❌</span>Failed</span>'
    else:
        return '<span style="background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 8px 20px; border-radius: 24px; font-weight: 700; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 6px;"><span style="font-size: 1.1rem;">⏳</span>Pending</span>'


def render_interview_detail(interview_id: int):
    """
    Render interview detail view
    
    Args:
        interview_id: ID of the interview to display
    """
    # Apply CSS - Liquid glassmorphism style
    st.markdown("""
        <style>
        @keyframes fade-in-scale {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes shimmer {
            0%, 100% { background-position: -200% center; }
            50% { background-position: 200% center; }
        }
        
        .interview-detail-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
            backdrop-filter: blur(30px) saturate(180%);
            border-radius: 28px;
            padding: 2.5rem;
            box-shadow: 
                0 20px 50px rgba(0, 0, 0, 0.1),
                0 10px 20px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.8);
            animation: fade-in-scale 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .interview-detail-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, 
                transparent, 
                #667eea, 
                #764ba2, 
                #f093fb, 
                transparent);
            background-size: 200% 100%;
            animation: shimmer 3s ease-in-out infinite;
        }
        
        .detail-section {
            margin-bottom: 2rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .detail-section:hover {
            transform: translateX(5px);
        }
        
        .detail-section:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .section-title {
            font-size: 0.8rem;
            font-weight: 700;
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(102, 126, 234, 0.2);
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 16px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 2px;
        }
        
        .detail-value {
            font-size: 1.05rem;
            color: #1f2937;
            font-weight: 500;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.25rem;
        }
        
        .info-item {
            padding: 1.25rem;
            background: linear-gradient(135deg, rgba(249, 250, 251, 0.9), rgba(243, 244, 246, 0.8));
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .info-item:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
        }
        
        .info-label {
            font-size: 0.75rem;
            color: #9ca3af;
            margin-bottom: 0.5rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .info-value {
            font-weight: 600;
            color: #374151;
            font-size: 1rem;
        }
        
        .job-highlight {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.08));
            padding: 1.5rem;
            border-radius: 16px;
            border-left: 4px solid #667eea;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
            transition: all 0.3s ease;
        }
        
        .job-highlight:hover {
            transform: translateX(5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        }
        
        .notes-box {
            background: linear-gradient(135deg, rgba(255, 251, 235, 0.9), rgba(254, 249, 226, 0.8));
            padding: 1.5rem;
            border-radius: 16px;
            color: #92400e;
            white-space: pre-wrap;
            border: 1px solid rgba(245, 158, 11, 0.2);
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.08);
            line-height: 1.7;
            transition: all 0.3s ease;
        }
        
        .notes-box:hover {
            background: linear-gradient(135deg, rgba(255, 251, 235, 1), rgba(254, 249, 226, 0.95));
        }
        
        .feedback-box {
            background: linear-gradient(135deg, rgba(240, 253, 244, 0.9), rgba(236, 253, 245, 0.8));
            padding: 1.5rem;
            border-radius: 16px;
            color: #166534;
            white-space: pre-wrap;
            border: 1px solid rgba(16, 185, 129, 0.2);
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.08);
            line-height: 1.7;
            transition: all 0.3s ease;
        }
        
        .feedback-box:hover {
            background: linear-gradient(135deg, rgba(240, 253, 244, 1), rgba(236, 253, 245, 0.95));
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .interview-detail-card {
                padding: 1.5rem;
                border-radius: 20px;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Fetch interview data
    try:
        interview = interview_service.get_interview_by_id(interview_id)
    except Exception as e:
        st.error(f"❌ Không thể tải thông tin phỏng vấn: {str(e)}")
        return
    
    if not interview:
        st.warning("⚠️ Không tìm thấy phỏng vấn này.")
        return
    
    # Fetch job info
    job_info = None
    try:
        job_info = job_service.get_job_by_id(interview.get("job_id"))
    except:
        pass
    
    # Header with back button
    col1, col2 = st.columns([0.5, 5.5], gap="medium")
    with col1:
        if st.button("⬅️", key="back_btn", use_container_width=True, help="Quay lại danh sách"):
            if "selected_interview_id" in st.session_state:
                del st.session_state.selected_interview_id
            st.rerun()
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Main content
    st.markdown('<div class="interview-detail-card">', unsafe_allow_html=True)
    
    # Header
    result_badge = get_result_badge(interview.get("result"))
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px;">
                <h2 style="margin: 0 0 12px 0; color: #1f2937; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.3;">
                    Round {interview.get('round_number', 1)}: {interview.get('interview_type', 'Interview')}
                </h2>
                <p style="margin: 0; color: #6b7280; font-size: 1rem; display: flex; align-items: center; gap: 8px; line-height: 1.6;">
                    <span style="font-size: 1.1rem;">📅</span> {format_datetime_display(interview.get('scheduled_date', ''))}
                </p>
            </div>
            <div style="flex-shrink: 0;">{result_badge}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Job info section
    if job_info:
        st.markdown(f"""
            <div class="detail-section">
                <div class="section-title">🏢 Công việc</div>
                <div class="job-highlight">
                    <div style="font-weight: 700; font-size: 1.25rem; color: #667eea; margin-bottom: 0.5rem; letter-spacing: -0.01em;">
                        {job_info.get('job_title', 'N/A')}
                    </div>
                    <div style="color: #6b7280; font-size: 1rem;">
                        {job_info.get('company_name', 'N/A')}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Schedule & Location
    meeting_link = interview.get('meeting_link')
    meeting_link_html = f'<a href="{meeting_link}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600; transition: all 0.2s;" onmouseover="this.style.color=\'#5568d3\'; this.style.textDecoration=\'underline\';" onmouseout="this.style.color=\'#667eea\'; this.style.textDecoration=\'none\';">{meeting_link}</a>' if meeting_link else '<span style="color: #9ca3af;">Chưa có</span>'
    
    st.markdown(f"""
        <div class="detail-section">
            <div class="section-title">📍 Địa điểm & Thời gian</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">📅 Ngày giờ</div>
                    <div class="info-value">{format_datetime_display(interview.get('scheduled_date', ''))}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📍 Địa điểm</div>
                    <div class="info-value">{interview.get('location') or '<span style="color: #9ca3af;">Chưa có</span>'}</div>
                </div>
                <div class="info-item" style="grid-column: span 2;">
                    <div class="info-label">🔗 Link meeting</div>
                    <div class="info-value">
                        {meeting_link_html}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Interviewer
    st.markdown(f"""
        <div class="detail-section">
            <div class="section-title">👤 Người phỏng vấn</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Tên</div>
                    <div class="info-value">{interview.get('interviewer_name') or '<span style="color: #9ca3af;">Chưa có</span>'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Chức vụ</div>
                    <div class="info-value">{interview.get('interviewer_title') or '<span style="color: #9ca3af;">Chưa có</span>'}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Preparation notes
    st.markdown(f"""
        <div class="detail-section">
            <div class="section-title">📝 Ghi chú chuẩn bị</div>
            <div class="notes-box">
                {interview.get('preparation_notes') or '<span style="color: #d97706; font-style: italic;">Chưa có ghi chú</span>'}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feedback (if any)
    if interview.get("feedback"):
        st.markdown(f"""
            <div class="detail-section">
                <div class="section-title">💬 Feedback</div>
                <div class="feedback-box">
                    {interview.get('feedback')}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2], gap="medium")
    
    with col1:
        if st.button("✏️ Chỉnh sửa", key="edit_interview", use_container_width=True, help="Chỉnh sửa thông tin phỏng vấn"):
            st.session_state.editing_interview_id = interview_id
            st.rerun()
    
    with col2:
        if st.button("📊 Kết quả", key="update_result", use_container_width=True, type="primary", help="Cập nhật kết quả phỏng vấn"):
            st.session_state.update_interview_id = interview_id
            st.rerun()
    
    with col3:
        if st.button("🗑️ Xóa", key="delete_interview", use_container_width=True, type="secondary", help="Xóa phỏng vấn này"):
            st.session_state.confirm_delete_interview = interview_id
            st.rerun()
    
    # Delete confirmation
    if st.session_state.get("confirm_delete_interview") == interview_id:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.08));
                padding: 20px;
                border-radius: 16px;
                border-left: 4px solid #ef4444;
                margin-bottom: 16px;
            ">
                <div style="font-weight: 700; color: #991b1b; font-size: 1.05rem; margin-bottom: 8px;">
                    ⚠️ Xác nhận xóa
                </div>
                <div style="color: #dc2626; font-size: 0.95rem; line-height: 1.6;">
                    Bạn có chắc chắn muốn xóa phỏng vấn này không? Hành động này không thể hoàn tác.
                </div>
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 3], gap="medium")
        with col1:
            if st.button("✅ Xác nhận", type="primary", use_container_width=True, help="Xác nhận xóa phỏng vấn"):
                try:
                    interview_service.delete_interview(interview_id)
                    st.success("✅ Đã xóa phỏng vấn!")
                    del st.session_state.confirm_delete_interview
                    if "selected_interview_id" in st.session_state:
                        del st.session_state.selected_interview_id
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        with col2:
            if st.button("❌ Hủy", use_container_width=True, help="Hủy thao tác"):
                del st.session_state.confirm_delete_interview
                st.rerun()
