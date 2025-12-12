"""
Job Detail Component
Displays detailed information for a single job
"""
import streamlit as st
from datetime import date
from frontend.config.settings import STATUS_COLORS
from frontend.services.job_service import job_service
from frontend.components.job_edit_form import render_job_edit_form

# Status Vietnamese mapping
STATUS_VN_MAP = {
    "Applied": "Đã ứng tuyển",
    "Screening": "Đã phỏng vấn", 
    "Interview": "Đã phỏng vấn",
    "Offer": "Đã nhận offer",
    "Hired": "Đã từ chối",
    "Rejected": "Đã bị từ chối"
}

def render_job_detail(job_id: int):
    """
    Render detailed view of a job with modern gradient design
    
    Args:
        job_id: ID of the job to display
    """
    try:
        job = job_service.get_job(job_id)
        
        # Custom CSS for job detail
        st.markdown("""
        <style>
        .detail-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border-left: 6px solid #06b6d4;
        }
        
        .detail-header {
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
            border-radius: 20px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 8px 24px rgba(6, 182, 212, 0.3);
        }
        
        .detail-title {
            font-size: 36px;
            font-weight: 900;
            margin: 0 0 0.5rem 0;
            letter-spacing: -1px;
        }
        
        .detail-subtitle {
            font-size: 22px;
            margin: 0;
            opacity: 0.95;
            font-weight: 600;
        }
        
        .info-section {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 16px;
            padding: 1.5rem;
            border-left: 4px solid #06b6d4;
            margin-bottom: 1rem;
        }
        
        .info-section h3 {
            color: #0284c7;
            font-size: 18px;
            font-weight: 800;
            margin: 0 0 1rem 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .info-item {
            margin-bottom: 0.75rem;
            line-height: 1.6;
        }
        
        .info-label {
            font-weight: 700;
            color: #475569;
            font-size: 14px;
        }
        
        .info-value {
            color: #1e293b;
            font-weight: 600;
            font-size: 15px;
        }
        
        .status-badge-detail {
            display: inline-block;
            padding: 0.5rem 1.25rem;
            border-radius: 25px;
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
            color: white;
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
        }
        
        .description-box {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            border: 2px solid #e0f2fe;
            margin-top: 1.5rem;
        }
        
        .description-box h3 {
            color: #0284c7;
            font-size: 20px;
            font-weight: 800;
            margin: 0 0 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Back button
        if st.button("← Quay lại danh sách", type="secondary"):
            st.session_state.selected_job_id = None
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Header section with gradient
        favorite_icon = "⭐" if job.get("is_favorite") else ""
        status_vn = STATUS_VN_MAP.get(job["current_status"], job["current_status"])
        
        header_html = f"""
        <div class='detail-header'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <div style='flex: 1;'>
                    <div class='detail-title'>{favorite_icon} {job['company_name']}</div>
                    <div class='detail-subtitle'>{job['job_title']}</div>
                </div>
                <div class='status-badge-detail'>{status_vn}</div>
            </div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        
        # Basic info in 3 columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            info_html = """
            <div class='info-section'>
                <h3>📋 Thông tin cơ bản</h3>
            """
            if job.get("location"):
                info_html += f"<div class='info-item'><span class='info-label'>Địa điểm:</span><br><span class='info-value'>{job['location']}</span></div>"
            if job.get("work_type"):
                info_html += f"<div class='info-item'><span class='info-label'>Hình thức:</span><br><span class='info-value'>{job['work_type']}</span></div>"
            if job.get("source"):
                info_html += f"<div class='info-item'><span class='info-label'>Nguồn:</span><br><span class='info-value'>{job['source']}</span></div>"
            if job.get("job_url"):
                info_html += f"<div class='info-item'><span class='info-label'>Link:</span><br><a href='{job['job_url']}' target='_blank' style='color: #06b6d4; font-weight: 600;'>Xem bài đăng →</a></div>"
            info_html += "</div>"
            st.markdown(info_html, unsafe_allow_html=True)
        
        with col2:
            info_html = """
            <div class='info-section'>
                <h3>📅 Thời gian</h3>
            """
            info_html += f"<div class='info-item'><span class='info-label'>Ngày nộp:</span><br><span class='info-value'>{job['applied_date']}</span></div>"
            if job.get("deadline"):
                info_html += f"<div class='info-item'><span class='info-label'>Deadline:</span><br><span class='info-value'>{job['deadline']}</span></div>"
            info_html += f"<div class='info-item'><span class='info-label'>Tạo lúc:</span><br><span class='info-value'>{job.get('created_at', 'N/A')}</span></div>"
            if job.get("updated_at"):
                info_html += f"<div class='info-item'><span class='info-label'>Cập nhật:</span><br><span class='info-value'>{job['updated_at']}</span></div>"
            info_html += "</div>"
            st.markdown(info_html, unsafe_allow_html=True)
        
        with col3:
            info_html = """
            <div class='info-section'>
                <h3>💰 Lương & Liên hệ</h3>
            """
            if job.get("salary_min") and job.get("salary_max"):
                salary_min = int(float(job['salary_min']))
                salary_max = int(float(job['salary_max']))
                info_html += f"<div class='info-item'><span class='info-label'>Lương:</span><br><span class='info-value'>{salary_min:,} - {salary_max:,} {job.get('salary_currency', 'VND')}</span></div>"
            if job.get("contact_person"):
                info_html += f"<div class='info-item'><span class='info-label'>Người liên hệ:</span><br><span class='info-value'>{job['contact_person']}</span></div>"
            if job.get("contact_email"):
                info_html += f"<div class='info-item'><span class='info-label'>Email:</span><br><span class='info-value'>{job['contact_email']}</span></div>"
            if job.get("contact_phone"):
                info_html += f"<div class='info-item'><span class='info-label'>SĐT:</span><br><span class='info-value'>{job['contact_phone']}</span></div>"
            info_html += "</div>"
            st.markdown(info_html, unsafe_allow_html=True)
        
        # Job description
        if job.get("job_description"):
            desc_html = f"""
            <div class='description-box'>
                <h3>📝 Mô tả công việc</h3>
                <div style='color: #475569; line-height: 1.8; font-size: 15px;'>
                    {job["job_description"]}
                </div>
            </div>
            """
            st.markdown(desc_html, unsafe_allow_html=True)
        
        # Custom CSS for action buttons
        st.markdown("""
        <style>
        /* Action buttons container */
        .action-buttons-container {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }
        
        /* Modern button styles */
        div[data-testid="column"] .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Edit button - Blue gradient */
        div[data-testid="column"]:nth-child(1) .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        div[data-testid="column"]:nth-child(1) .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        }
        
        /* Delete button - Red gradient */
        div[data-testid="column"]:nth-child(2) .stButton > button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            color: white !important;
        }
        div[data-testid="column"]:nth-child(2) .stButton > button:hover {
            background: linear-gradient(135deg, #e879f9 0%, #ef4444 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4) !important;
        }
        
        /* Favorite button - Yellow/Orange gradient */
        div[data-testid="column"]:nth-child(3) .stButton > button {
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%) !important;
            color: #1a1a2e !important;
        }
        div[data-testid="column"]:nth-child(3) .stButton > button:hover {
            background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(251, 146, 60, 0.4) !important;
        }
        
        /* Analytics button - Cyan gradient */
        div[data-testid="column"]:nth-child(4) .stButton > button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
            color: #1a1a2e !important;
        }
        div[data-testid="column"]:nth-child(4) .stButton > button:hover {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4) !important;
        }
        
        /* Confirm delete buttons */
        .confirm-delete-yes .stButton > button {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
            color: white !important;
        }
        .confirm-delete-no .stButton > button {
            background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%) !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Action buttons section header
        st.markdown("""<br>
        <div style='background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                    border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1rem;
                    border-left: 4px solid #06b6d4;'>
            <h3 style='margin: 0; color: #0284c7; font-size: 16px; font-weight: 700;'>
                🛠️ Thao tác nhanh
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        # Initialize edit mode state
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        if 'delete_confirm' not in st.session_state:
            st.session_state.delete_confirm = False
        
        with col1:
            if st.button("✏️ Chỉnh sửa", use_container_width=True, type="primary"):
                st.session_state.edit_mode = True
                st.rerun()
        with col2:
            if st.button("🗑️ Xóa job", use_container_width=True, type="secondary"):
                st.session_state.delete_confirm = True
                st.rerun()
        with col3:
            # Toggle favorite
            fav_label = "💔 Bỏ thích" if job.get('is_favorite') else "⭐ Yêu thích"
            if st.button(fav_label, use_container_width=True, type="secondary"):
                try:
                    job_service.update_job(job_id, {"is_favorite": not job.get('is_favorite', False)})
                    st.success("✅ Đã cập nhật!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
        
        # Delete confirmation dialog - Modern styled
        if st.session_state.get('delete_confirm'):
            st.markdown("""<br>
            <div style='background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); 
                        border-radius: 16px; padding: 1.5rem; margin: 1rem 0;
                        border: 2px solid #fecaca; box-shadow: 0 4px 14px rgba(239, 68, 68, 0.15);'>
                <div style='display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;'>
                    <span style='font-size: 24px;'>⚠️</span>
                    <h3 style='margin: 0; color: #dc2626; font-size: 18px; font-weight: 700;'>Xác nhận xóa</h3>
                </div>
                <p style='color: #7f1d1d; margin: 0; font-size: 15px; line-height: 1.6;'>
                    Bạn có chắc chắn muốn xóa job <strong>""" + job['company_name'] + " - " + job['job_title'] + """</strong>?<br>
                    <span style='opacity: 0.8;'>Hành động này không thể hoàn tác.</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col_yes, col_no, col_empty = st.columns([1, 1, 2])
            with col_yes:
                if st.button("✅ Xác nhận xóa", use_container_width=True, type="primary"):
                    try:
                        job_service.delete_job(job_id)
                        st.session_state.delete_confirm = False
                        st.session_state.selected_job_id = None
                        st.success("✅ Đã xóa job thành công!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi khi xóa: {str(e)}")
            with col_no:
                if st.button("❌ Hủy bỏ", use_container_width=True, type="secondary"):
                    st.session_state.delete_confirm = False
                    st.rerun()
        
        # Edit form - Using separate component
        if st.session_state.get('edit_mode'):
            st.markdown("---")
            render_job_edit_form(job, job_id)
    
    except Exception as e:
        st.error(f"⚠️ Không thể tải chi tiết job: {str(e)}")
        if st.button("⬅️ Quay lại"):
            st.session_state.selected_job_id = None
            st.rerun()
