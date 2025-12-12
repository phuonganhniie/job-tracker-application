"""
Job List Component
Displays filtered job list with card view
"""
import streamlit as st
from frontend.config.settings import STATUS_COLORS
from frontend.services.job_service import job_service


# Vietnamese status mapping
STATUS_VN_MAP = {
    "Applied": "Đã nộp",
    "Screening": "Sàng lọc",
    "Interview": "Phỏng vấn",
    "Offer": "Nhận offer",
    "Hired": "Đã nhận việc",
    "Rejected": "Bị từ chối"
}


def render_job_list(filters: dict):
    """
    Render job list with filters
    
    Args:
        filters: Dictionary containing filter criteria
    """
    try:
        # Initialize pagination state
        if 'jobs_page' not in st.session_state:
            st.session_state.jobs_page = 1
        if 'jobs_page_size' not in st.session_state:
            st.session_state.jobs_page_size = 10
        
        # Get jobs with pagination
        response = job_service.get_jobs(
            page=st.session_state.jobs_page, 
            page_size=st.session_state.jobs_page_size, 
            filters=filters
        )
        jobs = response.get("items", [])
        total = response.get("total", 0)
        total_pages = (total + st.session_state.jobs_page_size - 1) // st.session_state.jobs_page_size
        
        # Custom CSS for buttons
        st.markdown("""
        <style>
        div[data-testid="column"] button[kind="primary"] {
            background: white !important;
            border: 2px solid #e5e7eb !important;
            color: #667eea !important;
            font-weight: 700 !important;
            padding: 0.65rem 1.5rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
            font-size: 15px !important;
        }
        div[data-testid="column"] button[kind="primary"]:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-color: transparent !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        }
        div[data-testid="column"] button[kind="secondary"] {
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%) !important;
            border: none !important;
            color: #4b5563 !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="column"] button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        }
        div[data-testid="column"] button[kind="secondary"]:disabled {
            background: #f9fafb !important;
            color: #d1d5db !important;
            cursor: not-allowed !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Result summary with pagination info
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 2rem;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
            <p style='color: white; font-size: 18px; font-weight: 600; margin: 0;'>
                Tìm thấy <span style='font-weight: 800; font-size: 24px;'>{total}</span> công việc
                <span style='opacity: 0.9; font-size: 16px; margin-left: 1rem;'>
                    (Trang {st.session_state.jobs_page}/{total_pages if total_pages > 0 else 1})
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if jobs:
            # Display as modern cards with gradient design in 2 columns (responsive)
            for i in range(0, len(jobs), 2):
                cols = st.columns([1, 1], gap="large")
                for col_idx, col in enumerate(cols):
                    if i + col_idx < len(jobs):
                        job = jobs[i + col_idx]
                        with col:
                            # Status gradient mapping
                            status_gradients = {
                                "Applied": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                "Screening": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                                "Interview": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                                "Offer": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
                                "Hired": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
                                "Rejected": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)"
                            }
                            status_gradient = status_gradients.get(job["current_status"], "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
                            status_vn = STATUS_VN_MAP.get(job["current_status"], job["current_status"])
                            
                            # Card with gradient accent
                            card_html = "<div style='background: white; border-radius: 16px; margin-bottom: 2rem; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.12); transition: transform 0.3s ease, box-shadow 0.3s ease;'>"
                
                            
                            # Gradient header bar
                            card_html += f"<div style='height: 6px; background: {status_gradient};'></div>"
                            
                            # Card content
                            card_html += "<div style='padding: 1.75rem;'>"
                            
                            # Top section with company and status
                            card_html += "<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.25rem;'>"
                            card_html += "<div style='flex: 1;'>"
                            card_html += f"<h2 style='margin: 0 0 0.5rem 0; color: #111827; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;'>{job['company_name']}</h2>"
                            card_html += f"<p style='margin: 0 0 0.5rem 0; color: #4b5563; font-size: 18px; font-weight: 600;'>{job['job_title']}</p>"
                            
                            if job.get('location'):
                                card_html += f"<p style='margin: 0; color: #9ca3af; font-size: 15px; font-weight: 500;'>{job['location']}</p>"
                            
                            card_html += "</div>"
                            
                            # Status badge with gradient
                            card_html += "<div style='text-align: right;'>"
                            card_html += f"<div style='background: {status_gradient}; padding: 0.5rem 1.25rem; border-radius: 25px; display: inline-block; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);'>"
                            card_html += f"<span style='color: white; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>{status_vn}</span>"
                            card_html += "</div>"
                            
                            if job.get('is_favorite'):
                                card_html += "<div style='margin-top: 0.75rem; background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800; font-size: 15px; letter-spacing: 0.5px;'>⭐ YÊU THÍCH</div>"
                            
                            card_html += "</div>"
                            card_html += "</div>"
                            
                            # Info grid with gradient accents
                            card_html += "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 2px solid #f3f4f6;'>"
                            
                            # Applied date
                            card_html += "<div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1rem; border-radius: 12px; border-left: 4px solid #667eea;'>"
                            card_html += "<p style='margin: 0 0 0.5rem 0; color: #6b7280; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>Ngày nộp</p>"
                            card_html += f"<p style='margin: 0; color: #111827; font-size: 16px; font-weight: 700;'>{job['applied_date']}</p>"
                            card_html += "</div>"
                            
                            # Salary
                            if job.get('salary_min') and job.get('salary_max'):
                                salary_min = int(float(job['salary_min']))
                                salary_max = int(float(job['salary_max']))
                                card_html += "<div style='background: linear-gradient(135deg, #43e97b15 0%, #38f9d715 100%); padding: 1rem; border-radius: 12px; border-left: 4px solid #43e97b;'>"
                                card_html += "<p style='margin: 0 0 0.5rem 0; color: #6b7280; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>Mức lương</p>"
                                card_html += f"<p style='margin: 0; color: #111827; font-size: 16px; font-weight: 700;'>{salary_min:,} - {salary_max:,}</p>"
                                card_html += f"<p style='margin: 0.25rem 0 0 0; color: #6b7280; font-size: 13px; font-weight: 600;'>{job.get('salary_currency', 'VND')}</p>"
                                card_html += "</div>"
                            
                            # Source
                            if job.get('source'):
                                card_html += "<div style='background: linear-gradient(135deg, #4facfe15 0%, #00f2fe15 100%); padding: 1rem; border-radius: 12px; border-left: 4px solid #4facfe;'>"
                                card_html += "<p style='margin: 0 0 0.5rem 0; color: #6b7280; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>Nguồn</p>"
                                card_html += f"<p style='margin: 0; color: #111827; font-size: 16px; font-weight: 700;'>{job['source']}</p>"
                                card_html += "</div>"
                            
                            card_html += "</div>"
                            
                            card_html += "</div>"
                            
                            card_html += "</div>"
                            card_html += "</div>"
                            
                            st.markdown(card_html, unsafe_allow_html=True)
                            
                            # Button in columns to position at bottom left
                            col_left, col_mid, col_right = st.columns([2, 4, 4])
                            with col_left:
                                if st.button("Xem chi tiết", key=f"view_{job['id']}", use_container_width=True):
                                    st.session_state.selected_job_id = job['id']
                                    st.rerun()
                            with col_right:
                                # Delete button with confirm
                                delete_key = f"delete_{job['id']}"
                                confirm_key = f"confirm_delete_{job['id']}"
                                
                                if st.session_state.get(confirm_key):
                                    # Show confirm buttons
                                    confirm_col1, confirm_col2 = st.columns(2)
                                    with confirm_col1:
                                        if st.button("✅ Xóa", key=f"yes_{job['id']}", use_container_width=True, type="primary"):
                                            try:
                                                job_service.delete_job(job['id'])
                                                st.session_state[confirm_key] = False
                                                st.success(f"✅ Đã xóa job!")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Lỗi: {str(e)}")
                                    with confirm_col2:
                                        if st.button("❌ Hủy", key=f"no_{job['id']}", use_container_width=True):
                                            st.session_state[confirm_key] = False
                                            st.rerun()
                                else:
                                    if st.button("🗑️ Xóa", key=delete_key, use_container_width=True, type="secondary"):
                                        st.session_state[confirm_key] = True
                                        st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Pagination controls
            if total > st.session_state.jobs_page_size:
                st.markdown("---")
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                
                with col1:
                    if st.button("Đầu", type="secondary", disabled=(st.session_state.jobs_page == 1), use_container_width=True):
                        st.session_state.jobs_page = 1
                        st.rerun()
                
                with col2:
                    if st.button("Trước", type="secondary", disabled=(st.session_state.jobs_page == 1), use_container_width=True):
                        st.session_state.jobs_page -= 1
                        st.rerun()
                
                with col3:
                    st.markdown(f"<p style='text-align: center; font-weight: 700; color: #667eea; margin-top: 0.5rem; font-size: 16px;'>Trang {st.session_state.jobs_page} / {total_pages}</p>", unsafe_allow_html=True)
                
                with col4:
                    if st.button("Tiếp", type="secondary", disabled=(st.session_state.jobs_page >= total_pages), use_container_width=True):
                        st.session_state.jobs_page += 1
                        st.rerun()
                
                with col5:
                    if st.button("Cuối", type="secondary", disabled=(st.session_state.jobs_page >= total_pages), use_container_width=True):
                        st.session_state.jobs_page = total_pages
                        st.rerun()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 3rem 2rem; background: #f9fafb; 
                        border-radius: 12px; border: 2px dashed #d1d5db;'>
                <p style='font-size: 18px; color: #6b7280; margin: 0;'>
                    Chưa có công việc nào. Hãy thêm công việc mới!
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
