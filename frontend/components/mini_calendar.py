"""
Mini Calendar Component - Display a small calendar widget
"""
import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
import calendar


def get_month_calendar(year: int, month: int) -> List[List[int]]:
    """Get calendar matrix for a month"""
    cal = calendar.Calendar(firstweekday=0)  # Monday as first day
    return cal.monthdayscalendar(year, month)


def render_mini_calendar(
    interviews: List[Dict],
    selected_date: Optional[date] = None,
    on_date_select: Optional[callable] = None
):
    """
    Render a mini calendar showing interview dates
    
    Args:
        interviews: List of interviews with scheduled_date
        selected_date: Currently selected date
        on_date_select: Callback when date is selected
    """
    # Parse interview dates
    interview_dates = set()
    for interview in interviews:
        try:
            dt_str = interview.get("scheduled_date", "")
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            interview_dates.add(dt.date())
        except:
            pass
    
    # Current view month
    if "calendar_month" not in st.session_state:
        st.session_state.calendar_month = date.today().month
    if "calendar_year" not in st.session_state:
        st.session_state.calendar_year = date.today().year
    
    current_month = st.session_state.calendar_month
    current_year = st.session_state.calendar_year
    today = date.today()
    
    # Month names in Vietnamese
    month_names = [
        "", "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
    ]
    
    # Calendar CSS - Premium responsive design without white box
    st.markdown("""
        <style>
        .mini-calendar {
            padding: 0;
        }
        
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .calendar-title {
            font-weight: 700;
            color: #1f2937;
            font-size: 1.1rem;
            letter-spacing: -0.01em;
            flex: 1;
            text-align: center;
        }
        
        .calendar-nav {
            display: flex;
            gap: 8px;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            text-align: center;
        }
        
        .calendar-weekday {
            font-size: 0.75rem;
            font-weight: 700;
            color: #667eea;
            padding: 8px 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .calendar-day {
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.875rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 500;
            min-height: 36px;
            position: relative;
        }
        
        .calendar-day:hover {
            background: rgba(102, 126, 234, 0.1);
            transform: scale(1.1);
        }
        
        .calendar-day.empty {
            cursor: default;
            opacity: 0;
        }
        
        .calendar-day.today {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.1));
            color: #1e40af;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
        }
        
        .calendar-day.has-interview {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .calendar-day.has-interview:hover {
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
            transform: scale(1.12);
        }
        
        .calendar-day.selected {
            outline: 3px solid #667eea;
            outline-offset: 2px;
            z-index: 10;
        }
        
        .calendar-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid rgba(0, 0, 0, 0.06);
            font-size: 0.8rem;
            color: #6b7280;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 500;
        }
        
        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Calendar navigation buttons */
        .stButton button {
            padding: 0.5rem 0.75rem !important;
            font-size: 0.9rem !important;
            border-radius: 10px !important;
            min-height: 38px !important;
            white-space: nowrap !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Compact day buttons - Force uniform sizing */
        .mini-calendar div[data-testid="column"] > div > div > button {
            padding: 8px 2px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            height: 40px !important;
            font-size: 0.9rem !important;
            line-height: 1 !important;
            font-weight: 600 !important;
            width: 100% !important;
            box-sizing: border-box !important;
            border-radius: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Override primary button specific styles */
        .mini-calendar div[data-testid="column"] > div > div > button[kind="primary"],
        .mini-calendar div[data-testid="column"] > div > div > button[data-testid="baseButton-primary"] {
            min-width: 100% !important;
            padding: 8px 2px !important;
            height: 40px !important;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .mini-calendar {
                padding: 1rem;
                border-radius: 16px;
            }
            
            .calendar-weekday {
                font-size: 0.7rem;
                padding: 6px 0;
            }
            
            .calendar-day {
                font-size: 0.8rem;
                min-height: 32px;
                border-radius: 10px;
            }
            
            .calendar-legend {
                font-size: 0.75rem;
                gap: 8px;
            }
        }
        
        @media (max-width: 480px) {
            .calendar-day {
                min-height: 28px;
                font-size: 0.75rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Build calendar with Streamlit components
    month_weeks = get_month_calendar(current_year, current_month)
    weekdays = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    
    st.markdown('<div class="mini-calendar">', unsafe_allow_html=True)
    
    # Navigation header with buttons and centered month title
    nav_cols = st.columns([1, 3, 1])
    
    with nav_cols[0]:
        if st.button("◄", key="prev_month_btn", use_container_width=True):
            if current_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year = current_year - 1
            else:
                st.session_state.calendar_month = current_month - 1
            st.rerun()
    
    with nav_cols[1]:
        st.markdown(f"""
            <div style="text-align: center; font-weight: 700; color: #1f2937; font-size: 1.1rem; padding-top: 6px;">
                {month_names[current_month]} {current_year}
            </div>
        """, unsafe_allow_html=True)
    
    with nav_cols[2]:
        if st.button("►", key="next_month_btn", use_container_width=True):
            if current_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year = current_year + 1
            else:
                st.session_state.calendar_month = current_month + 1
            st.rerun()
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Weekday headers
    weekday_cols = st.columns(7)
    for i, day in enumerate(weekdays):
        with weekday_cols[i]:
            st.markdown(f"""
                <div style="text-align: center; font-size: 0.7rem; font-weight: 700; color: #667eea; letter-spacing: 0.03em; padding: 6px 0;">
                    {day}
                </div>
            """, unsafe_allow_html=True)
    
    # Calendar days
    for week in month_weeks:
        day_cols = st.columns(7)
        for i, day in enumerate(week):
            with day_cols[i]:
                if day == 0:
                    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)
                else:
                    current_date = date(current_year, current_month, day)
                    is_today = current_date == today
                    has_interview = current_date in interview_dates
                    
                    interview_count = len([iv for iv in interviews if iv.get('scheduled_date', '').startswith(current_date.isoformat())])
                    
                    button_kwargs = {
                        "label": str(day),
                        "key": f"day_{current_year}_{current_month}_{day}",
                        "use_container_width": True
                    }
                    
                    if has_interview:
                        button_kwargs["type"] = "primary"
                        button_kwargs["help"] = f"📅 {interview_count} phỏng vấn"
                    
                    if st.button(**button_kwargs):
                        st.session_state.selected_calendar_date = current_date
                        if on_date_select:
                            on_date_select(current_date)
                        st.rerun()
    
    # Legend
    st.markdown("""
        <div class="calendar-legend">
            <div class="legend-item">
                <div class="legend-dot" style="background: linear-gradient(135deg, #667eea, #764ba2);"></div>
                <span>Có phỏng vấn</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.4), rgba(37, 99, 235, 0.3));"></div>
                <span>Hôm nay</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_interviews_on_date(interviews: List[Dict], target_date: date):
    """Show interviews on a specific date with premium styling"""
    filtered = []
    for interview in interviews:
        try:
            dt_str = interview.get("scheduled_date", "")
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            if dt.date() == target_date:
                filtered.append(interview)
        except:
            pass
    
    if not filtered:
        st.markdown(f"""
            <div style="
                text-align: center;
                padding: 24px 16px;
                background: linear-gradient(135deg, rgba(243, 244, 246, 0.95), rgba(249, 250, 251, 0.9));
                backdrop-filter: blur(10px);
                border-radius: 16px;
                border: 1px dashed rgba(156, 163, 175, 0.4);
                margin: 16px 0;
            ">
                <div style="font-size: 2.5rem; margin-bottom: 8px; opacity: 0.6;">📭</div>
                <div style="color: #6b7280; font-weight: 500; font-size: 0.95rem;">
                    Không có phỏng vấn vào ngày {target_date.strftime('%d/%m/%Y')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"""
        <div style="
            font-size: 1.1rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(102, 126, 234, 0.2);
            letter-spacing: -0.01em;
        ">
            📅 Phỏng vấn ngày {target_date.strftime('%d/%m/%Y')}
        </div>
    """, unsafe_allow_html=True)
    
    for interview in sorted(filtered, key=lambda x: x.get("scheduled_date", "")):
        try:
            dt = datetime.fromisoformat(interview.get("scheduled_date", "").replace("Z", "+00:00"))
            time_str = dt.strftime("%H:%M")
        except:
            time_str = "N/A"
        
        location = interview.get('location') or interview.get('meeting_link') or '<span style="color: #9ca3af; font-style: italic;">Chưa có địa điểm</span>'
        
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
                backdrop-filter: blur(10px);
                padding: 16px;
                border-radius: 14px;
                margin-bottom: 12px;
                border-left: 4px solid #667eea;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            " onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='0 6px 16px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 4px 12px rgba(0, 0, 0, 0.06)';">
                <div style="font-weight: 700; color: #1f2937; font-size: 0.95rem; margin-bottom: 6px; letter-spacing: -0.01em;">
                    ⏰ {time_str} — Round {interview.get('round_number', 1)}: {interview.get('interview_type', 'Interview')}
                </div>
                <div style="font-size: 0.875rem; color: #6b7280; line-height: 1.5;">
                    {location}
                </div>
            </div>
        """, unsafe_allow_html=True)
