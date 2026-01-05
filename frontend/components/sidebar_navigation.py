"""
Sidebar Navigation Component
Provides CSS styling for sidebar navigation used across all pages
"""
import streamlit as st


def apply_sidebar_navigation_css():
    """Apply modern sidebar navigation CSS styling"""
    st.markdown("""
        <style>
        /* ============================================
           SIDEBAR NAVIGATION - MODERN LIGHT THEME
           ============================================ */
        
        /* Sidebar container */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 50%, #f8fafc 100%);
            border-right: 1px solid #cbd5e1;
        }
        
        /* Sidebar content padding */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem !important;
        }
        
        /* App logo/title area */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            background: transparent;
            padding-top: 1rem;
        }
        
        /* Navigation list container */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] > ul {
            padding: 0 1rem;
        }
        
        /* Navigation links */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] li {
            margin-bottom: 0.5rem;
        }
        
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
            display: flex;
            align-items: center;
            padding: 0.875rem 1.25rem;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            color: #475569;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: transparent;
            border: 2px solid transparent;
            letter-spacing: 0.2px;
        }
        
        /* Navigation link hover */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
            background: rgba(6, 182, 212, 0.1);
            color: #06b6d4;
            border-color: rgba(6, 182, 212, 0.3);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.15);
        }
        
        /* Active/selected page */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
            color: white;
            font-weight: 700;
            border-color: transparent;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.4);
            transform: scale(1.02);
        }
        
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"]:hover {
            transform: scale(1.02) translateX(2px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
        }
        
        /* Emoji spacing */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] a span {
            margin-right: 0.75rem;
            font-size: 18px;
        }
        
        /* Sidebar divider */
        [data-testid="stSidebar"] hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(203, 213, 225, 0.5), transparent);
            margin: 1.5rem 0;
        }
        
        /* Collapse button */
        [data-testid="stSidebar"] button[kind="header"] {
            background: rgba(6, 182, 212, 0.1);
            color: #06b6d4;
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        [data-testid="stSidebar"] button[kind="header"]:hover {
            background: rgba(6, 182, 212, 0.2);
            transform: scale(1.05);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
                padding: 0.75rem 1rem;
                font-size: 14px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
