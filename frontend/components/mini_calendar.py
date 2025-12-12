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
    
    # Calendar CSS
    st.markdown("""
        <style>
        .mini-calendar {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid #f3f4f6;
        }
        
        .calendar-title {
            font-weight: 600;
            color: #1f2937;
            font-size: 1rem;
        }
        
        .calendar-nav {
            display: flex;
            gap: 0.5rem;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 2px;
            text-align: center;
        }
        
        .calendar-weekday {
            font-size: 0.7rem;
            font-weight: 600;
            color: #9ca3af;
            padding: 0.5rem 0;
            text-transform: uppercase;
        }
        
        .calendar-day {
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        
        .calendar-day:hover {
            background: #f3f4f6;
        }
        
        .calendar-day.empty {
            cursor: default;
        }
        
        .calendar-day.today {
            background: #dbeafe;
            color: #1e40af;
            font-weight: 600;
        }
        
        .calendar-day.has-interview {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-weight: 600;
        }
        
        .calendar-day.selected {
            outline: 2px solid #667eea;
            outline-offset: 2px;
        }
        
        .calendar-legend {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid #f3f4f6;
            font-size: 0.75rem;
            color: #6b7280;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="mini-calendar">', unsafe_allow_html=True)
    
    # Header with navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("◀", key="prev_month", use_container_width=True):
            if current_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year = current_year - 1
            else:
                st.session_state.calendar_month = current_month - 1
            st.rerun()
    
    with col2:
        st.markdown(f"""
            <div style="text-align: center; font-weight: 600; color: #1f2937;">
                {month_names[current_month]} {current_year}
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("▶", key="next_month", use_container_width=True):
            if current_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year = current_year + 1
            else:
                st.session_state.calendar_month = current_month + 1
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weekday headers
    weekdays = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    weekday_cols = st.columns(7)
    for i, day in enumerate(weekdays):
        with weekday_cols[i]:
            st.markdown(f"""
                <div style="text-align: center; font-size: 0.7rem; font-weight: 600; color: #9ca3af;">
                    {day}
                </div>
            """, unsafe_allow_html=True)
    
    # Calendar days
    month_weeks = get_month_calendar(current_year, current_month)
    
    for week in month_weeks:
        day_cols = st.columns(7)
        for i, day in enumerate(week):
            with day_cols[i]:
                if day == 0:
                    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
                else:
                    current_date = date(current_year, current_month, day)
                    is_today = current_date == today
                    has_interview = current_date in interview_dates
                    is_selected = selected_date and current_date == selected_date
                    
                    # Determine style
                    if has_interview:
                        bg = "linear-gradient(135deg, #667eea, #764ba2)"
                        color = "white"
                        weight = "600"
                    elif is_today:
                        bg = "#dbeafe"
                        color = "#1e40af"
                        weight = "600"
                    else:
                        bg = "transparent"
                        color = "#374151"
                        weight = "400"
                    
                    outline = "2px solid #667eea" if is_selected else "none"
                    
                    # Create button for clickable day
                    if st.button(
                        str(day),
                        key=f"day_{current_year}_{current_month}_{day}",
                        use_container_width=True,
                        help=f"{len([i for i in interviews if i.get('scheduled_date', '').startswith(current_date.isoformat())])} phỏng vấn" if has_interview else None
                    ):
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
                <div class="legend-dot" style="background: #dbeafe;"></div>
                <span>Hôm nay</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_interviews_on_date(interviews: List[Dict], target_date: date):
    """Show interviews on a specific date"""
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
        st.info(f"📭 Không có phỏng vấn nào vào ngày {target_date.strftime('%d/%m/%Y')}")
        return
    
    st.markdown(f"### 📅 Phỏng vấn ngày {target_date.strftime('%d/%m/%Y')}")
    
    for interview in sorted(filtered, key=lambda x: x.get("scheduled_date", "")):
        try:
            dt = datetime.fromisoformat(interview.get("scheduled_date", "").replace("Z", "+00:00"))
            time_str = dt.strftime("%H:%M")
        except:
            time_str = "N/A"
        
        st.markdown(f"""
            <div style="
                background: white;
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 0.75rem;
                border-left: 4px solid #667eea;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            ">
                <div style="font-weight: 600; color: #1f2937;">
                    ⏰ {time_str} - Round {interview.get('round_number', 1)}: {interview.get('interview_type', 'Interview')}
                </div>
                <div style="font-size: 0.9rem; color: #6b7280; margin-top: 0.25rem;">
                    {interview.get('location') or interview.get('meeting_link') or 'Chưa có địa điểm'}
                </div>
            </div>
        """, unsafe_allow_html=True)
