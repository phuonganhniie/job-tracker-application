"""
Job Detail Component
Displays detailed information for a single job
"""
import streamlit as st
from datetime import date
from frontend.config.settings import STATUS_COLORS
from frontend.services.job_service import job_service

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
        
        # Action buttons
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        # Initialize edit mode state
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        if 'delete_confirm' not in st.session_state:
            st.session_state.delete_confirm = False
        
        with col1:
            if st.button("✏️ Sửa", use_container_width=True, type="primary"):
                st.session_state.edit_mode = True
                st.rerun()
        with col2:
            if st.button("🗑️ Xóa", use_container_width=True, type="secondary"):
                st.session_state.delete_confirm = True
                st.rerun()
        with col3:
            # Toggle favorite
            fav_label = "💔 Bỏ yêu thích" if job.get('is_favorite') else "⭐ Yêu thích"
            if st.button(fav_label, use_container_width=True, type="secondary"):
                try:
                    job_service.update_job(job_id, {"is_favorite": not job.get('is_favorite', False)})
                    st.success("✅ Đã cập nhật!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
        with col4:
            if st.button("📊 Analytics", use_container_width=True, type="secondary"):
                st.info("Chức năng đang phát triển")
        
        # Delete confirmation dialog
        if st.session_state.get('delete_confirm'):
            st.markdown("---")
            st.warning(f"⚠️ Bạn có chắc chắn muốn xóa job **{job['company_name']} - {job['job_title']}**? Hành động này không thể hoàn tác.")
            col_yes, col_no = st.columns(2)
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
                if st.button("❌ Hủy", use_container_width=True, type="secondary"):
                    st.session_state.delete_confirm = False
                    st.rerun()
        
        # Edit form
        if st.session_state.get('edit_mode'):
            st.markdown("---")
            st.markdown("### ✏️ Chỉnh sửa thông tin job")
            
            with st.form("edit_job_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    edit_company = st.text_input("Tên công ty *", value=job.get('company_name', ''))
                    edit_title = st.text_input("Vị trí *", value=job.get('job_title', ''))
                    edit_location = st.text_input("Địa điểm", value=job.get('location', '') or '')
                    edit_work_type = st.selectbox(
                        "Hình thức", 
                        ["Remote", "Hybrid", "Onsite"],
                        index=["Remote", "Hybrid", "Onsite"].index(job.get('work_type', 'Remote')) if job.get('work_type') in ["Remote", "Hybrid", "Onsite"] else 0
                    )
                    edit_source = st.text_input("Nguồn", value=job.get('source', '') or '')
                
                with col2:
                    status_options = ["Applied", "Screening", "Interview", "Offer", "Hired", "Rejected"]
                    edit_status = st.selectbox(
                        "Trạng thái",
                        status_options,
                        index=status_options.index(job.get('current_status', 'Applied')) if job.get('current_status') in status_options else 0
                    )
                    
                    # Parse applied_date
                    try:
                        applied_val = date.fromisoformat(str(job.get('applied_date', date.today()))[:10])
                    except:
                        applied_val = date.today()
                    edit_applied_date = st.date_input("Ngày nộp *", value=applied_val)
                    
                    # Parse deadline
                    deadline_val = None
                    if job.get('deadline'):
                        try:
                            deadline_val = date.fromisoformat(str(job['deadline'])[:10])
                        except:
                            pass
                    edit_deadline = st.date_input("Deadline", value=deadline_val)
                    
                    edit_favorite = st.checkbox("⭐ Yêu thích", value=job.get('is_favorite', False))
                
                edit_url = st.text_input("Link bài đăng", value=job.get('job_url', '') or '')
                edit_description = st.text_area("Mô tả công việc", value=job.get('job_description', '') or '', height=120)
                
                st.markdown("##### 💰 Mức lương")
                sal_col1, sal_col2, sal_col3 = st.columns(3)
                with sal_col1:
                    edit_salary_min = st.number_input("Lương tối thiểu", min_value=0, value=int(float(job.get('salary_min') or 0)), step=1000000)
                with sal_col2:
                    edit_salary_max = st.number_input("Lương tối đa", min_value=0, value=int(float(job.get('salary_max') or 0)), step=1000000)
                with sal_col3:
                    currency_options = ["VND", "USD"]
                    edit_currency = st.selectbox(
                        "Đơn vị",
                        currency_options,
                        index=currency_options.index(job.get('salary_currency', 'VND')) if job.get('salary_currency') in currency_options else 0
                    )
                
                st.markdown("##### 👤 Liên hệ")
                contact_col1, contact_col2, contact_col3 = st.columns(3)
                with contact_col1:
                    edit_contact_person = st.text_input("Người liên hệ", value=job.get('contact_person', '') or '')
                with contact_col2:
                    edit_contact_email = st.text_input("Email", value=job.get('contact_email', '') or '')
                with contact_col3:
                    edit_contact_phone = st.text_input("SĐT", value=job.get('contact_phone', '') or '')
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    submit_edit = st.form_submit_button("💾 Lưu thay đổi", use_container_width=True)
                with btn_col2:
                    cancel_edit = st.form_submit_button("❌ Hủy", use_container_width=True)
                
                if submit_edit:
                    if not edit_company or not edit_title:
                        st.error("⚠️ Vui lòng nhập đầy đủ thông tin bắt buộc (*)")
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
                            st.success("✅ Cập nhật thành công!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Lỗi khi cập nhật: {str(e)}")
                
                if cancel_edit:
                    st.session_state.edit_mode = False
                    st.rerun()
    
    except Exception as e:
        st.error(f"⚠️ Không thể tải chi tiết job: {str(e)}")
        if st.button("⬅️ Quay lại"):
            st.session_state.selected_job_id = None
            st.rerun()
