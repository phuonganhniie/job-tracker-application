"""
Jobs Page - Job management
"""
import streamlit as st
from frontend.config.settings import STATUS_COLORS
from frontend.components.job_list import render_job_list
from frontend.components.job_detail import render_job_detail
from frontend.components.job_form import render_job_form
from frontend.components.sidebar_navigation import apply_sidebar_navigation_css
from frontend.components.job_filters import render_job_filters

st.set_page_config(page_title="Jobs", page_icon="💼", layout="wide")

# Apply sidebar navigation CSS
apply_sidebar_navigation_css()

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
        padding-left: 3rem;
        padding-right: 3rem;
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
    
    /* Tab styling - Liquid gradient design with blue-cyan gradient */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        background: transparent;
        padding: 1.5rem 0 2rem 0;
        margin-bottom: 1rem;
        border-bottom: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 70px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 20px;
        border: none;
        color: #64748b;
        font-weight: 700;
        font-size: 17px;
        letter-spacing: -0.02em;
        padding: 0 2.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    
    .stTabs [data-baseweb="tab"] p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        letter-spacing: -0.02em !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
        color: #0284c7;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #06b6d4 !important;
        border: none !important;
        box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.1), 
                    0 12px 32px rgba(6, 182, 212, 0.2) !important;
        transform: translateY(-3px) scale(1.02);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2.5rem;
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
        
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            font-size: 15px;
            padding: 0 1.5rem;
        }
        
        .stTabs [data-baseweb="tab"] p {
            font-size: 15px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Job Tracker Application")
st.markdown("---")
st.markdown("""
<p style='font-size: 16px; color: #6b7280; margin-bottom: 2rem;'>
    Theo dõi và quản lý các công việc đã/đang ứng tuyển
</p>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    filter_values = render_job_filters()

# Extract filter values
search_keyword = filter_values["search_keyword"]
status_filter = filter_values["status_filter"]
source_filter = filter_values["source_filter"]
work_type_filter = filter_values["work_type_filter"]
is_favorite = filter_values["is_favorite"]

# Check if viewing job details
if "selected_job_id" in st.session_state and st.session_state.selected_job_id:
    # Show job details without tabs
    render_job_detail(st.session_state.selected_job_id)
else:
    # Show success message if job was just created
    if st.session_state.get("job_created_success", False):
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%); 
                    padding: 1.25rem 1.75rem; 
                    border-radius: 12px; 
                    margin-bottom: 1.5rem;
                    border-left: 5px solid #10b981;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);'>
            <div style='color: #059669; font-weight: 700; font-size: 16px; margin-bottom: 4px;'>
                Thêm job thành công
            </div>
            <div style='color: #6b7280; font-size: 14px; font-weight: 500;'>
                {} - {}
            </div>
        </div>
        <script>
            // Auto-click first tab after job creation
            setTimeout(function() {{
                const firstTab = parent.document.querySelector('[data-baseweb="tab"][aria-selected="false"]');
                if (firstTab) {{
                    firstTab.click();
                }}
            }}, 100);
        </script>
        """.format(
            st.session_state.get("new_job_company", ""), 
            st.session_state.get("new_job_title", "")
        ), unsafe_allow_html=True)
        
        st.session_state.job_created_success = False
        st.session_state.pop("new_job_company", None)
        st.session_state.pop("new_job_title", None)

    # Initialize active tab in session state
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0

    # Main content tabs
    tab1, tab2 = st.tabs(["📋 Danh sách Jobs", "✨ Thêm Job mới"])    # Tab 1: Job list
    with tab1:
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
