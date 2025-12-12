"""
Interview List Component - Display list of interviews
"""
import streamlit as st
import streamlit.components.v1 as components
from typing import List, Dict, Optional
from datetime import datetime


def get_result_style(result: Optional[str]) -> tuple:
    """Get color and icon for interview result"""
    if result == "Passed":
        return "#10b981", "#d1fae5", "✅"
    elif result == "Failed":
        return "#ef4444", "#fee2e2", "❌"
    else:  # Pending or None
        return "#f59e0b", "#fef3c7", "⏳"


def get_type_icon(interview_type: Optional[str]) -> str:
    """Get icon for interview type"""
    icons = {
        "Phone Screening": "📞",
        "Video Call": "💻",
        "Technical Test": "🧪",
        "Onsite Interview": "🏢",
        "Final Round": "🎯",
        "HR Interview": "👤"
    }
    return icons.get(interview_type, "📋")


def format_datetime(dt_str: str) -> tuple:
    """Format datetime string to readable format"""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        date_str = dt.strftime("%d/%m/%Y")
        time_str = dt.strftime("%H:%M")
        return date_str, time_str
    except:
        return "N/A", "N/A"


def is_upcoming(dt_str: str) -> bool:
    """Check if interview is upcoming"""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt > datetime.now(dt.tzinfo) if dt.tzinfo else dt > datetime.now()
    except:
        return False


def render_interview_card(interview: Dict, job_info: Optional[Dict] = None, show_job: bool = True):
    """Render a single interview card with liquid glassmorphism style"""
    date_str, time_str = format_datetime(interview.get("scheduled_date", ""))
    result_color, result_bg, result_icon = get_result_style(interview.get("result"))
    type_icon = get_type_icon(interview.get("interview_type"))
    upcoming = is_upcoming(interview.get("scheduled_date", ""))
    
    # Card gradient and glow based on status
    if upcoming:
        card_gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%)"
        border_color = "#10b981"
        glow_color = "rgba(16, 185, 129, 0.15)"
    elif interview.get("result") == "Passed":
        card_gradient = "linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%)"
        border_color = "#3b82f6"
        glow_color = "rgba(59, 130, 246, 0.15)"
    elif interview.get("result") == "Failed":
        card_gradient = "linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(220, 38, 38, 0.05) 100%)"
        border_color = "#ef4444"
        glow_color = "rgba(239, 68, 68, 0.15)"
    else:
        card_gradient = "linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%)"
        border_color = "#e5e7eb"
        glow_color = "rgba(0, 0, 0, 0.05)"
    
    # Build job info HTML
    job_html = ""
    if show_job and job_info:
        company = job_info.get('company_name', 'N/A')
        title = job_info.get('job_title', '')
        job_html = f"""
            <div style='
                font-size: 0.95rem; 
                color: #374151; 
                margin-bottom: 0.75rem;
                padding: 0.5rem;
                background: rgba(102, 126, 234, 0.05);
                border-radius: 10px;
                border-left: 3px solid #667eea;
            '>
                🏢 <strong style="color: #667eea;">{company}</strong> — {title}
            </div>
        """
    
    # Build details HTML
    details_parts = []
    if interview.get('location'):
        details_parts.append(f"<span style='display: inline-flex; align-items: center; gap: 4px;'>📍 {interview.get('location')}</span>")
    if interview.get('meeting_link'):
        details_parts.append(f"<span style='display: inline-flex; align-items: center; gap: 4px;'>🔗 <a href='{interview.get('meeting_link')}' target='_blank' style='color: #667eea; text-decoration: none; font-weight: 500; transition: all 0.2s;' onmouseover='this.style.color=\"#5568d3\"' onmouseout='this.style.color=\"#667eea\"'>Meeting Link</a></span>")
    if interview.get('interviewer_name'):
        details_parts.append(f"<span style='display: inline-flex; align-items: center; gap: 4px;'>👤 {interview.get('interviewer_name')}</span>")
    details_html = " • ".join(details_parts) if details_parts else "<span style='color: #9ca3af;'>Chưa có thông tin chi tiết</span>"
    
    result_text = interview.get('result') or 'Pending'
    
    card_html = f"""
        <div style="
            background: {card_gradient};
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 
                0 10px 30px {glow_color},
                0 4px 10px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.9),
                inset -3px 0 0 {border_color};
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-5px) scale(1.01)'; this.style.boxShadow='0 20px 40px {glow_color}, 0 8px 20px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 1), inset -3px 0 0 {border_color}';" onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 10px 30px {glow_color}, 0 4px 10px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.9), inset -3px 0 0 {border_color}';">
            
            <!-- Animated gradient overlay -->
            <div style="
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
                animation: float 8s ease-in-out infinite;
                pointer-events: none;
            "></div>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; position: relative;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 2rem; filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1)); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.2) rotate(10deg)';" onmouseout="this.style.transform='scale(1) rotate(0deg)';">{type_icon}</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1.1rem; color: #1f2937; letter-spacing: -0.01em;">
                            Round {interview.get('round_number', 1)}: {interview.get('interview_type', 'Interview')}
                        </div>
                        <div style="font-size: 0.9rem; color: #6b7280; margin-top: 0.25rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span style="display: inline-flex; align-items: center; gap: 4px;">📅 {date_str}</span>
                            <span style="color: #d1d5db;">•</span>
                            <span style="display: inline-flex; align-items: center; gap: 4px;">⏰ {time_str}</span>
                        </div>
                    </div>
                </div>
                <span style="
                    background: {result_bg};
                    color: {result_color};
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 700;
                    box-shadow: 0 4px 12px {glow_color};
                    border: 1px solid rgba(255, 255, 255, 0.5);
                    transition: all 0.3s ease;
                    letter-spacing: 0.02em;
                " onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                    {result_icon} {result_text}
                </span>
            </div>
            
            {job_html}
            
            <div style="
                display: flex; 
                gap: 1rem; 
                font-size: 0.875rem; 
                color: #6b7280; 
                flex-wrap: wrap;
                padding-top: 0.75rem;
                border-top: 1px solid rgba(0, 0, 0, 0.05);
                position: relative;
            ">
                {details_html}
            </div>
        </div>
        
        <style>
        @keyframes float {{
            0%, 100% {{ transform: translateY(0) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(5deg); }}
        }}
        </style>
    """
    
    # Use components.html for reliable rendering
    components.html(card_html, height=200 if show_job else 180, scrolling=False)


def render_interview_list(
    interviews: List[Dict], 
    jobs_map: Optional[Dict[int, Dict]] = None,
    show_job: bool = True,
    on_select: Optional[callable] = None,
    key_prefix: str = ""
):
    """
    Render list of interview cards
    
    Args:
        interviews: List of interview data
        jobs_map: Optional dict mapping job_id to job info
        show_job: Whether to show job info on cards
        on_select: Optional callback when interview is selected
        key_prefix: Prefix for widget keys to avoid duplicates
    """
    if not interviews:
        st.info("📭 Không có phỏng vấn nào.")
        return
    
    # Generate unique prefix if not provided
    if not key_prefix:
        import random
        key_prefix = f"list_{random.randint(1000, 9999)}"
    
    for interview in interviews:
        job_info = None
        if jobs_map and interview.get("job_id"):
            job_info = jobs_map.get(interview["job_id"])
        
        render_interview_card(interview, job_info, show_job)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("📝 Chi tiết", key=f"{key_prefix}_detail_{interview['id']}", use_container_width=True):
                if on_select:
                    on_select(interview["id"])
                else:
                    st.session_state.selected_interview_id = interview["id"]
                    st.rerun()
        with col2:
            if st.button("📊 Cập nhật", key=f"{key_prefix}_update_{interview['id']}", use_container_width=True):
                st.session_state.update_interview_id = interview["id"]
                st.rerun()
        
        st.markdown("<hr style='border: none; border-top: 1px solid #f3f4f6; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)


def render_upcoming_interviews(interviews: List[Dict], jobs_map: Optional[Dict[int, Dict]] = None):
    """Render upcoming interviews section with enhanced styling"""
    if not interviews:
        st.markdown("""
            <div style="
                text-align: center;
                padding: 3rem 2rem;
                background: linear-gradient(135deg, rgba(240, 253, 244, 0.9), rgba(236, 253, 245, 0.8));
                backdrop-filter: blur(20px);
                border-radius: 24px;
                border: 1px solid rgba(134, 239, 172, 0.3);
                box-shadow: 0 10px 30px rgba(16, 185, 129, 0.1);
                animation: fade-in 0.6s ease-out;
            ">
                <div style="font-size: 3.5rem; margin-bottom: 1rem; animation: bounce 2s ease-in-out infinite;">🎉</div>
                <div style="color: #166534; font-weight: 600; font-size: 1.2rem; margin-bottom: 0.5rem;">Không có phỏng vấn nào trong 7 ngày tới</div>
                <div style="color: #22c55e; font-size: 1rem;">Hãy tiếp tục ứng tuyển nhé!</div>
            </div>
            
            <style>
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }
            @keyframes fade-in {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            </style>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(254, 243, 199, 0.95), rgba(253, 230, 138, 0.9));
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 20px;
            padding: 1.5rem 1.75rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            border: 1px solid rgba(245, 158, 11, 0.2);
            box-shadow: 
                0 10px 30px rgba(245, 158, 11, 0.15),
                0 4px 10px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slide-in 0.5s ease-out;
        " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 15px 40px rgba(245, 158, 11, 0.2), 0 8px 15px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(245, 158, 11, 0.15), 0 4px 10px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.8)';">
            <span style="font-size: 2.5rem; filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1)); animation: pulse 2s ease-in-out infinite;">⏰</span>
            <div style="flex: 1;">
                <div style="font-weight: 700; color: #92400e; font-size: 1.2rem; letter-spacing: -0.01em;">Sắp tới: {len(interviews)} phỏng vấn</div>
                <div style="font-size: 0.95rem; color: #a16207; margin-top: 0.25rem;">Trong 7 ngày tới</div>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.5);
                padding: 0.5rem 1rem;
                border-radius: 12px;
                font-weight: 700;
                font-size: 1.5rem;
                color: #92400e;
            ">{len(interviews)}</div>
        </div>
        
        <style>
        @keyframes slide-in {{
            from {{ opacity: 0; transform: translateX(-30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        </style>
    """, unsafe_allow_html=True)
    
    render_interview_list(interviews, jobs_map, show_job=True, key_prefix="upcoming")
