"""
Jobs Page - Job management
"""
import streamlit as st
from frontend.config.settings import STATUS_COLORS
from frontend.components.job_list import render_job_list
from frontend.components.job_detail import render_job_detail
from frontend.components.job_form import render_job_form

st.set_page_config(page_title="Jobs", page_icon="💼", layout="wide")

# Custom CSS with Inter font and modern styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'San Francisco', sans-serif;
    }
    
    .main > div {
        padding-top: 2rem;
    }
    .stApp {
        max-width: 100%;
    }
    
    .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    body {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.02em;
    }
    
    /* Job card styling */
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-applied { background: #dbeafe; color: #1e40af; }
    .status-screening { background: #e0e7ff; color: #4338ca; }
    .status-interview { background: #fce7f3; color: #be185d; }
    .status-offer { background: #dbeafe; color: #0284c7; }
    .status-hired { background: #d1fae5; color: #065f46; }
    .status-rejected { background: #fee2e2; color: #991b1b; }
    
    /* Detail page header */
    .detail-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }
    
    .detail-title {
        font-size: 36px;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .detail-subtitle {
        font-size: 20px;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Info card */
    .info-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    
    .info-card h3 {
        color: #1f2937;
        font-size: 18px;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    .info-item {
        margin-bottom: 0.75rem;
        color: #4b5563;
        line-height: 1.6;
    }
    
    .info-label {
        font-weight: 600;
        color: #1f2937;
    }
    
    /* Form styling */
    .stForm {
        background: #f9fafb;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    
    /* Button enhancements */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #1f2937;
        font-size: 20px;
        font-weight: 800;
        padding: 1rem 0 0.5rem 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 1.5rem;
    }
    
    /* Filter section header */
    .filter-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Input styling in sidebar */
    [data-testid="stSidebar"] .stTextInput > div > div {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        transition: all 0.2s;
        background: white;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div:focus-within {
        border-color: #e5e7eb;
        box-shadow: none;
        transform: none;
    }
    
    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #9ca3af;
        font-style: italic;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        background: white;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #e5e7eb;
    }
    
    /* Radio button styling */
    [data-testid="stSidebar"] .stRadio {
        background: transparent;
        padding: 0.75rem 0;
        border-radius: 8px;
        border: none;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 600;
        color: #374151;
        font-size: 13px;
    }
    
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        gap: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        background: transparent;
        border-radius: 6px;
        padding: 0.4rem 0.75rem;
        transition: all 0.2s;
        border: none;
    }
    
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"]:hover {
        background: transparent;
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + div {
        background: transparent;
        color: #374151;
        font-weight: 600;
        border: none;
    }
    
    /* Checkbox styling */
    [data-testid="stSidebar"] .stCheckbox {
        background: transparent;
        padding: 0.75rem 0;
        border-radius: 8px;
        border: none;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stCheckbox:hover {
        border: none;
        background: transparent;
    }
    
    [data-testid="stSidebar"] .stCheckbox input:checked ~ div {
        background: inherit;
    }
    
    /* Section labels */
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #1f2937;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    /* Action buttons styling */
    [data-testid="stSidebar"] .stButton > button {
        font-weight: 600;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 12px;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: white;
        color: #374151;
        border: 1px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: white;
        border-color: #e5e7eb;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a4190 100%);
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .detail-title {
            font-size: 24px;
        }
        
        .detail-subtitle {
            font-size: 16px;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='font-size: 40px; font-weight: 900; color: #111827; 
           margin-bottom: 10px; letter-spacing: -1.5px;'>
    💼 Quản lý Jobs
</h1>
<p style='font-size: 16px; color: #6b7280; margin-bottom: 2rem;'>
    Theo dõi và quản lý các công việc đã/đang ứng tuyển
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# Clear filter callback function
def clear_filters():
    """Clear all filter keys from session state"""
    filter_keys = ["search_keyword_input", "status_filter_select", 
                  "source_filter_input", "work_type_filter_select", "is_favorite_checkbox"]
    for key in filter_keys:
        if key in st.session_state:
            del st.session_state[key]

# Sidebar filters
with st.sidebar:
    # Search keyword with icon
    st.markdown("**🔍 Tìm kiếm công ty**")
    search_keyword = st.text_input(
        "Tìm kiếm",
        value="",
        placeholder="Nhập tên công ty...",
        label_visibility="collapsed",
        help="Tìm kiếm không phân biệt hoa thường",
        key="search_keyword_input"
    )
    
    st.markdown("")  # Spacing
    
    # Status filter with icon and Vietnamese mapping
    st.markdown("**📊 Trạng thái**")
    status_vn_map = {
        "Applied": "Đã nộp",
        "Screening": "Sàng lọc",
        "Interview": "Phỏng vấn",
        "Offer": "Nhận offer",
        "Hired": "Đã nhận việc",
        "Rejected": "Bị từ chối"
    }
    status_options_vn = ["Tất cả"] + [status_vn_map.get(s, s) for s in STATUS_COLORS.keys()]
    status_filter_vn = st.selectbox(
        "Trạng thái",
        status_options_vn,
        index=0,
        label_visibility="collapsed",
        help="Lọc theo trạng thái ứng tuyển",
        key="status_filter_select"
    )
    # Convert back to English for API
    status_en_map = {v: k for k, v in status_vn_map.items()}
    status_filter = status_en_map.get(status_filter_vn, status_filter_vn) if status_filter_vn != "Tất cả" else "Tất cả"
    
    st.markdown("")  # Spacing
    
    # Source filter with improved placeholder
    st.markdown("**🌐 Nguồn tuyển dụng**")
    source_filter = st.text_input(
        "Nguồn",
        value="",
        placeholder="VD: LinkedIn, Indeed, TopCV...",
        label_visibility="collapsed",
        help="Tìm kiếm không phân biệt hoa thường (partial match)",
        key="source_filter_input"
    )
    
    st.markdown("")  # Spacing
    
    # Work type filter
    st.markdown("**💼 Hình thức làm việc**")
    work_type_filter = st.selectbox(
        "Hình thức",
        ["Tất cả", "Remote", "Hybrid", "Onsite"],
        index=0,
        label_visibility="collapsed",
        help="Lọc theo hình thức làm việc",
        key="work_type_filter_select"
    )
    
    st.markdown("")  # Spacing
    
    # Favorite filter with enhanced checkbox
    st.markdown("**⭐ Yêu thích**")
    is_favorite = st.checkbox(
        "Chỉ hiển thị jobs yêu thích",
        value=False,
        help="Hiển thị các công việc đã đánh dấu yêu thích",
        key="is_favorite_checkbox"
    )
    
    st.markdown("---")
    
    # Action buttons without icons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Làm mới", use_container_width=True, type="secondary"):
            st.rerun()
    with col2:
        st.button("Xóa lọc", use_container_width=True, type="primary", on_click=clear_filters)
    
    # Filter summary
    st.markdown("---")
    active_filters = []
    if search_keyword:
        active_filters.append(f"🔎 Công ty: {search_keyword}")
    if status_filter != "Tất cả":
        active_filters.append(f"📊 {status_filter}")
    if source_filter:
        active_filters.append(f"🌐 {source_filter}")
    if work_type_filter != "Tất cả":
        active_filters.append(f"💼 {work_type_filter}")
    if is_favorite:
        active_filters.append("⭐ Yêu thích")
    
    if active_filters:
        st.markdown("**Đang lọc:**")
        for f in active_filters:
            st.caption(f"• {f}")
    else:
        st.info("💡 Chưa có bộ lọc nào")

# Main content tabs
tab1, tab2 = st.tabs(["📋 Danh sách Jobs", "➕ Thêm Job mới"])

# Tab 1: Job list
with tab1:
    # Check if viewing job details
    if "selected_job_id" in st.session_state and st.session_state.selected_job_id:
        render_job_detail(st.session_state.selected_job_id)
    else:
        # Display job list
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
            # Search by company name only (partial match)
            filters["company_name"] = search_keyword
        
        # Display job list using component
        render_job_list(filters)

# Tab 2: Add new job
with tab2:
    render_job_form()
