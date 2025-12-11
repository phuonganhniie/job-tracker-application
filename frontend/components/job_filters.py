"""
Job Filters Component
Sidebar filters for job search and filtering
"""
import streamlit as st
from frontend.config.settings import STATUS_COLORS


def render_job_filters():
    """
    Render job filters in sidebar and return filter values
    
    Returns:
        dict: Filter values including search_keyword, status_filter, source_filter, 
              work_type_filter, is_favorite
    """
    
    # CSS for filter section
    st.markdown("""
        <style>
        /* Filter section styling - Light theme */
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stTextInput,
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stCheckbox,
        [data-testid="stSidebar"] .stButton {
            margin-bottom: 0.5rem;
        }
        
        /* Section labels */
        [data-testid="stSidebar"] .stMarkdown strong {
            display: block;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #475569;
            margin-bottom: 0.75rem;
            margin-top: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e2e8f0;
        }
        
        /* Input styling - liquid style with cyan-blue */
        [data-testid="stSidebar"] .stTextInput > div > div {
            border-radius: 12px;
            border: 2px solid #e0f2fe;
            background: white;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] .stTextInput > div > div:focus-within {
            border: 2px solid #06b6d4;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.25);
            transform: translateY(-2px);
        }
        
        [data-testid="stSidebar"] .stTextInput input {
            border-radius: 10px;
            font-weight: 500;
            color: #1e293b;
        }
        
        [data-testid="stSidebar"] .stTextInput input::placeholder {
            color: #94a3b8;
            font-style: italic;
            font-weight: 400;
        }
        
        /* Selectbox styling */
        [data-testid="stSidebar"] .stSelectbox > div > div {
            border-radius: 12px;
            border: 2px solid #e0f2fe;
            background: white;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] .stSelectbox > div > div:hover {
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.2);
            transform: translateY(-1px);
            border-color: #06b6d4;
        }
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
            color: #1e293b;
        }
        
        /* Checkbox styling */
        [data-testid="stSidebar"] .stCheckbox {
            background: transparent;
            padding: 0.5rem;
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        [data-testid="stSidebar"] .stCheckbox:hover {
            background: rgba(6, 182, 212, 0.1);
        }
        
        [data-testid="stSidebar"] .stCheckbox label {
            color: #475569 !important;
        }
        
        /* Action buttons */
        [data-testid="stSidebar"] .stButton > button {
            font-weight: 600;
            padding: 0.6rem 1rem;
            border-radius: 10px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 13px;
            letter-spacing: 0.3px;
        }
        
        [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
            background: white;
            color: #475569;
            border: 2px solid #e2e8f0;
        }
        
        [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
            border-color: #cbd5e1;
            background: #f8fafc;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
            color: white;
            border: none;
            box-shadow: 0 2px 8px rgba(6, 182, 212, 0.25);
        }
        
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
            background: linear-gradient(135deg, #0891b2 0%, #2563eb 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Clear filter callback
    def clear_filters():
        """Clear all filter keys from session state"""
        filter_keys = ["search_keyword_input", "status_filter_select", 
                      "source_filter_input", "work_type_filter_select", "is_favorite_checkbox"]
        for key in filter_keys:
            if key in st.session_state:
                del st.session_state[key]
    
    # Modern title
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0 2rem 0;'>
            <h2 style='font-size: 20px; font-weight: 800; 
                       background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       margin: 0; letter-spacing: -0.5px;'>
                Bộ lọc tìm kiếm
            </h2>
            <div style='width: 60px; height: 3px; 
                        background: linear-gradient(90deg, #06b6d4, #3b82f6);
                        margin: 0.75rem auto; border-radius: 2px;'></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Search keyword
    st.markdown("**Tìm kiếm công ty**")
    search_keyword = st.text_input(
        "Tìm kiếm",
        value="",
        placeholder="Nhập tên công ty...",
        label_visibility="collapsed",
        help="Tìm kiếm không phân biệt hoa thường",
        key="search_keyword_input"
    )
    
    # Status filter
    st.markdown("**Trạng thái ứng tuyển**")
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
    
    # Source filter
    st.markdown("**Nguồn tuyển dụng**")
    source_filter = st.text_input(
        "Nguồn",
        value="",
        placeholder="LinkedIn, Indeed, TopCV...",
        label_visibility="collapsed",
        help="Tìm kiếm không phân biệt hoa thường",
        key="source_filter_input"
    )
    
    # Work type filter
    st.markdown("**Hình thức làm việc**")
    work_type_filter = st.selectbox(
        "Hình thức",
        ["Tất cả", "Remote", "Hybrid", "Onsite"],
        index=0,
        label_visibility="collapsed",
        help="Lọc theo hình thức làm việc",
        key="work_type_filter_select"
    )
    
    # Favorite filter
    st.markdown("**Yêu thích**")
    is_favorite = st.checkbox(
        "Chỉ hiển thị jobs yêu thích",
        value=False,
        help="Hiển thị các công việc đã đánh dấu yêu thích",
        key="is_favorite_checkbox"
    )
    
    st.markdown("---")
    
    # Action buttons
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
        active_filters.append(f"Công ty: {search_keyword}")
    if status_filter != "Tất cả":
        active_filters.append(f"Trạng thái: {status_filter_vn}")
    if source_filter:
        active_filters.append(f"Nguồn: {source_filter}")
    if work_type_filter != "Tất cả":
        active_filters.append(f"Hình thức: {work_type_filter}")
    if is_favorite:
        active_filters.append("Yêu thích")
    
    if active_filters:
        st.markdown("**Đang lọc:**")
        for f in active_filters:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
                            padding: 0.5rem 0.75rem; border-radius: 8px; 
                            margin-bottom: 0.5rem; font-size: 13px;
                            border-left: 3px solid #06b6d4; color: #0c4a6e;'>
                    {f}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                        padding: 1rem; border-radius: 10px; 
                        text-align: center; color: #166534; font-size: 13px;
                        border: 2px solid #86efac;'>
                Chưa có bộ lọc nào
            </div>
        """, unsafe_allow_html=True)
    
    # Return filter values
    return {
        "search_keyword": search_keyword,
        "status_filter": status_filter,
        "status_filter_vn": status_filter_vn,
        "source_filter": source_filter,
        "work_type_filter": work_type_filter,
        "is_favorite": is_favorite
    }
