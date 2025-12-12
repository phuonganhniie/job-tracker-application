"""
Interviews Page - Interview management with Hybrid view (List + Mini Calendar)
"""
import streamlit as st
from datetime import date
from frontend.config.settings import STATUS_COLORS
from frontend.services.interview_service import interview_service
from frontend.services.job_service import job_service
from frontend.components.interview_list import render_interview_list, render_upcoming_interviews
from frontend.components.interview_detail import render_interview_detail
from frontend.components.interview_form import render_interview_form, render_result_update_form
from frontend.components.mini_calendar import render_mini_calendar, render_interviews_on_date
from frontend.components.sidebar_navigation import apply_sidebar_navigation_css

st.set_page_config(page_title="Phỏng Vấn", page_icon="📅", layout="wide")

# Apply sidebar navigation CSS
apply_sidebar_navigation_css()

# Custom CSS - Liquid Style with Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Smooth animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Background with gradient */
    .main {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 50%, #f093fb15 100%);
        background-size: 200% 200%;
        animation: gradient-shift 15s ease infinite;
    }
    
    .main > div {
        padding-top: 2rem;
    }
    
    .block-container {
        max-width: 100%;
        padding-left: 3rem;
        padding-right: 3rem;
        animation: fade-in-up 0.6s ease-out;
    }
    
    /* Page header - Liquid glassmorphism */
    .page-header {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.9) 0%, 
            rgba(118, 75, 162, 0.9) 50%,
            rgba(240, 147, 251, 0.9) 100%);
        background-size: 200% 200%;
        animation: gradient-shift 8s ease infinite;
        color: white;
        padding: 2.5rem;
        border-radius: 32px;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 50px rgba(102, 126, 234, 0.3),
            0 10px 20px rgba(118, 75, 162, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .page-header:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 25px 60px rgba(102, 126, 234, 0.4),
            0 15px 30px rgba(118, 75, 162, 0.3);
    }
    
    .page-title {
        font-size: 2.25rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.02em;
        position: relative;
    }
    
    .page-subtitle {
        opacity: 0.95;
        font-size: 1.05rem;
        font-weight: 400;
        letter-spacing: 0.01em;
        position: relative;
    }
    
    /* Stats cards - Glassmorphism */
    .stat-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px) saturate(180%);
        padding: 1.75rem;
        border-radius: 24px;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.08),
            0 1px 3px rgba(0, 0, 0, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.6);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, currentColor, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.12),
            0 5px 10px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }
    
    .stat-card:hover::before {
        opacity: 0.6;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1f2937;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover .stat-value {
        transform: scale(1.1);
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    
    /* Tab styling - Glass morphism style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.7);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        color: #6b7280;
        background: transparent;
        letter-spacing: -0.01em;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(8px);
        color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        color: #667eea !important;
        font-weight: 600 !important;
        box-shadow: 
            0 4px 16px rgba(102, 126, 234, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 1) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Buttons - Liquid style */
    .stButton > button {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        padding: 0.65rem 1.25rem;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
        line-height: 1.5;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
        transform: none !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.35);
        filter: brightness(1.05);
    }
    
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.8);
        color: #374151;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.95);
        border-color: #667eea;
        color: #667eea;
    }
    
    /* Content sections */
    .content-section {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    /* Expander styling - Glass effect with Inter font */
    .streamlit-expanderHeader {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
        padding: 12px 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 1);
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .streamlit-expanderHeader p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        border-radius: 14px !important;
        border: 1.5px solid rgba(226, 232, 240, 0.8) !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(248, 250, 252, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5568d3, #6a3f8f);
    }
    
    /* Loading state */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent !important;
    }
    
    /* Responsive mobile-first */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .page-header {
            padding: 1.5rem;
            border-radius: 20px;
        }
        
        .page-title {
            font-size: 1.75rem;
        }
        
        .page-subtitle {
            font-size: 0.95rem;
        }
        
        .stat-card {
            padding: 1.25rem;
        }
        
        .stat-value {
            font-size: 2rem;
        }
        
        .stat-label {
            font-size: 0.8rem;
        }
        
        /* Stack columns on mobile */
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    @media (max-width: 480px) {
        .page-header {
            padding: 1.25rem;
        }
        
        .page-title {
            font-size: 1.5rem;
        }
        
        .stat-value {
            font-size: 1.75rem;
        }
        
        .stButton > button {
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "selected_interview_id" not in st.session_state:
    st.session_state.selected_interview_id = None
if "editing_interview_id" not in st.session_state:
    st.session_state.editing_interview_id = None
if "adding_interview" not in st.session_state:
    st.session_state.adding_interview = False
if "update_interview_id" not in st.session_state:
    st.session_state.update_interview_id = None


def load_data():
    """Load interviews and jobs data"""
    try:
        interviews_response = interview_service.get_interviews()
        interviews = interviews_response.get("items", [])
    except Exception as e:
        st.error(f"Lỗi tải danh sách phỏng vấn: {str(e)}")
        interviews = []
    
    try:
        upcoming_response = interview_service.get_upcoming_interviews(days=7)
        upcoming = upcoming_response.get("items", [])
    except:
        upcoming = []
    
    try:
        stats = interview_service.get_interview_stats()
    except Exception as e:
        st.warning(f"Không thể tải thống kê: {str(e)}")
        stats = {"total": 0, "passed": 0, "failed": 0, "pending": 0, "pass_rate": 0}
    
    try:
        jobs_response = job_service.get_jobs(page_size=100)
        jobs = jobs_response.get("items", [])
        jobs_map = {j["id"]: j for j in jobs}
    except:
        jobs_map = {}
    
    return interviews, upcoming, stats, jobs_map


# Check for detail/edit views first
if st.session_state.get("update_interview_id"):
    # Update result form
    try:
        interview = interview_service.get_interview_by_id(st.session_state.update_interview_id)
        render_result_update_form(interview)
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
        if st.button("← Quay lại"):
            del st.session_state.update_interview_id
            st.rerun()

elif st.session_state.get("editing_interview_id"):
    # Edit interview form
    try:
        interview = interview_service.get_interview_by_id(st.session_state.editing_interview_id)
        render_interview_form(interview=interview)
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
        if st.button("← Quay lại"):
            del st.session_state.editing_interview_id
            st.rerun()

elif st.session_state.get("selected_interview_id"):
    # Interview detail view
    render_interview_detail(st.session_state.selected_interview_id)

elif st.session_state.get("adding_interview"):
    # Add new interview form
    render_interview_form()

else:
    # Main page view
    
    # Load data
    interviews, upcoming, stats, jobs_map = load_data()
    
    # Page header
    st.markdown("""
        <div class="page-header">
            <div class="page-title">📅 Quản Lý Phỏng Vấn</div>
            <div class="page-subtitle">Theo dõi và quản lý các buổi phỏng vấn của bạn</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #667eea;">{stats.get('total', 0)}</div>
                <div class="stat-label">Tổng số</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #10b981;">{stats.get('passed', 0)}</div>
                <div class="stat-label">Đã qua</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #ef4444;">{stats.get('failed', 0)}</div>
                <div class="stat-label">Không qua</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color: #f59e0b;">{stats.get('pending', 0)}</div>
                <div class="stat-label">Chờ kết quả</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # Main content with sidebar calendar
    main_col, calendar_col = st.columns([2.5, 1], gap="large")
    
    with calendar_col:
        # Add button
        if st.button("➕ Thêm phỏng vấn", use_container_width=True, type="primary"):
            st.session_state.adding_interview = True
            st.rerun()
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Mini calendar
        render_mini_calendar(interviews)
        
        # Show interviews on selected date
        if st.session_state.get("selected_calendar_date"):
            st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
            render_interviews_on_date(interviews, st.session_state.selected_calendar_date)
    
    with main_col:
        # Tabs
        tab1, tab2, tab3 = st.tabs(["⏰ Sắp tới", "📋 Tất cả", "📊 Theo Job"])
        
        with tab1:
            st.markdown("""
                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 20px;
                    letter-spacing: -0.02em;
                    line-height: 1.4;
                ">
                    ⏰ Phỏng vấn sắp tới (7 ngày)
                </div>
            """, unsafe_allow_html=True)
            render_upcoming_interviews(upcoming, jobs_map)
        
        with tab2:
            st.markdown("""
                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 20px;
                    letter-spacing: -0.02em;
                    line-height: 1.4;
                ">
                    📋 Tất cả phỏng vấn
                </div>
            """, unsafe_allow_html=True)
            
            # Filters with enhanced UI
            with st.expander("🔍 Bộ lọc nâng cao", expanded=False):
                st.markdown("""
                    <div style="
                        font-family: 'Inter', sans-serif;
                        font-size: 0.85rem;
                        color: #6b7280;
                        margin-bottom: 12px;
                        font-weight: 500;
                    ">
                        Lọc phỏng vấn theo các tiêu chí bên dưới
                    </div>
                """, unsafe_allow_html=True)
                
                filter_col1, filter_col2, filter_col3 = st.columns(3, gap="medium")
                
                with filter_col1:
                    filter_type = st.selectbox(
                        "Loại phỏng vấn",
                        options=["Tất cả", "Phone Screening", "Video Call", "Technical Test", 
                                 "Onsite Interview", "Final Round", "HR Interview"],
                        help="Lọc theo loại phỏng vấn",
                        key="filter_type_select"
                    )
                
                with filter_col2:
                    filter_result = st.selectbox(
                        "Kết quả",
                        options=["Tất cả", "Pending", "Passed", "Failed"],
                        help="Lọc theo kết quả phỏng vấn",
                        key="filter_result_select"
                    )
                
                with filter_col3:
                    filter_job = st.selectbox(
                        "Công việc",
                        options=["Tất cả"] + [f"{j['company_name']} - {j['job_title']}" for j in jobs_map.values()],
                        help="Lọc theo công việc",
                        key="filter_job_select"
                    )
            
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            
            # Apply filters
            filtered_interviews = interviews
            
            if filter_type != "Tất cả":
                filtered_interviews = [i for i in filtered_interviews if i.get("interview_type") == filter_type]
            
            if filter_result != "Tất cả":
                if filter_result == "Pending":
                    filtered_interviews = [i for i in filtered_interviews if not i.get("result") or i.get("result") == "Pending"]
                else:
                    filtered_interviews = [i for i in filtered_interviews if i.get("result") == filter_result]
            
            if filter_job != "Tất cả":
                job_name = filter_job.split(" - ")[0]
                filtered_interviews = [i for i in filtered_interviews 
                                       if jobs_map.get(i.get("job_id"), {}).get("company_name") == job_name]
            
            # Pagination
            items_per_page = 5
            total_items = len(filtered_interviews)
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
            
            if "all_interviews_page" not in st.session_state:
                st.session_state.all_interviews_page = 1
            
            # Pagination info
            if total_items > 0:
                st.markdown(f"""
                    <div style="
                        font-family: 'Inter', sans-serif;
                        font-size: 0.875rem;
                        color: #6b7280;
                        margin-bottom: 16px;
                        font-weight: 500;
                    ">
                        Hiển thị {min((st.session_state.all_interviews_page - 1) * items_per_page + 1, total_items)}-{min(st.session_state.all_interviews_page * items_per_page, total_items)} trong tổng số {total_items} phỏng vấn
                    </div>
                """, unsafe_allow_html=True)
            
            # Display paginated items
            start_idx = (st.session_state.all_interviews_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            paginated_interviews = filtered_interviews[start_idx:end_idx]
            
            render_interview_list(paginated_interviews, jobs_map, key_prefix="all")
            
            # Pagination controls with custom styled buttons
            if total_pages > 1:
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                
                # Create columns for navigation
                pcol1, pcol2, pcol3, pcol4, pcol5 = st.columns([1, 1, 2, 1, 1])
                
                current_page = st.session_state.all_interviews_page
                
                with pcol1:
                    if st.button("⏮️", disabled=(current_page == 1), use_container_width=True, key="page_first", help="Trang đầu"):
                        st.session_state.all_interviews_page = 1
                        st.rerun()
                
                with pcol2:
                    if st.button("◀", disabled=(current_page == 1), use_container_width=True, key="page_prev", help="Trang trước"):
                        st.session_state.all_interviews_page -= 1
                        st.rerun()
                
                with pcol3:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.08));
                            backdrop-filter: blur(12px);
                            border-radius: 12px;
                            padding: 10px 16px;
                            text-align: center;
                            font-family: 'Inter', sans-serif;
                            font-weight: 600;
                            color: #667eea;
                            font-size: 0.9rem;
                            letter-spacing: -0.01em;
                            border: 1px solid rgba(102, 126, 234, 0.2);
                            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
                        ">
                            Trang {current_page} / {total_pages}
                        </div>
                    """, unsafe_allow_html=True)
                
                with pcol4:
                    if st.button("▶", disabled=(current_page == total_pages), use_container_width=True, key="page_next", help="Trang sau"):
                        st.session_state.all_interviews_page += 1
                        st.rerun()
                
                with pcol5:
                    if st.button("⏭️", disabled=(current_page == total_pages), use_container_width=True, key="page_last", help="Trang cuối"):
                        st.session_state.all_interviews_page = total_pages
                        st.rerun()
        
        with tab3:
            st.markdown("""
                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 20px;
                    letter-spacing: -0.02em;
                    line-height: 1.4;
                ">
                    📊 Phỏng vấn theo Job
                </div>
            """, unsafe_allow_html=True)
            
            # Group by job
            job_interviews = {}
            for interview in interviews:
                job_id = interview.get("job_id")
                if job_id not in job_interviews:
                    job_interviews[job_id] = []
                job_interviews[job_id].append(interview)
            
            for job_id, job_ints in job_interviews.items():
                job_info = jobs_map.get(job_id, {})
                job_name = f"{job_info.get('company_name', 'Unknown')} - {job_info.get('job_title', 'Unknown')}"
                
                with st.expander(f"🏢 {job_name} ({len(job_ints)} vòng)", expanded=False):
                    # Sort by round number
                    sorted_ints = sorted(job_ints, key=lambda x: x.get("round_number", 0))
                    render_interview_list(sorted_ints, jobs_map, show_job=False, key_prefix=f"job_{job_id}")
