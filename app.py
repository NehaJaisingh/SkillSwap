import streamlit as st
from db import get_connection

st.set_page_config(
    page_title="SkillSwap",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================================================================
#  Database Helpers  (UNCHANGED)
# ================================================================

def fetch_data(query, params=()):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def execute_query(query, params=()):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
    finally:
        cursor.close()
        connection.close()


# ================================================================
#  Design System  —  Centralised CSS
# ================================================================

ACCENT = "#4f46e5"           # indigo-600
ACCENT_HOVER = "#4338ca"     # indigo-700
ACCENT_LIGHT = "#eef2ff"     # indigo-50
BORDER = "#e5e7eb"           # gray-200
TEXT_PRIMARY = "#111827"      # gray-900
TEXT_SECONDARY = "#6b7280"   # gray-500
TEXT_MUTED = "#9ca3af"       # gray-400
SURFACE = "#ffffff"
BG = "#f9fafb"               # gray-50

st.markdown(f"""
<style>
/* ── Reset & Global ─────────────────────────────────────── */
.stApp {{
    background-color: {BG};
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, Helvetica, Arial, sans-serif;
}}
#MainMenu, footer, header {{visibility: hidden;}}

/* ── Sidebar ────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {SURFACE};
    border-right: 1px solid {BORDER};
    padding-top: 1.5rem;
}}
section[data-testid="stSidebar"] .stRadio > label {{
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
}}
section[data-testid="stSidebar"] .stRadio > div {{
    gap: 2px;
}}
section[data-testid="stSidebar"] .stRadio > div label {{
    padding: 0.55rem 0.85rem;
    border-radius: 8px;
    font-size: 0.88rem;
    color: {TEXT_SECONDARY};
    font-weight: 500;
    transition: all 0.12s ease;
    cursor: pointer;
}}
section[data-testid="stSidebar"] .stRadio > div label:hover {{
    background: {BG};
    color: {TEXT_PRIMARY};
}}
section[data-testid="stSidebar"] .stRadio > div label[data-checked="true"] {{
    background: {ACCENT_LIGHT};
    color: {ACCENT};
    font-weight: 600;
}}

/* ── Typography ─────────────────────────────────────────── */
h1 {{
    font-weight: 700 !important;
    color: {TEXT_PRIMARY} !important;
    font-size: 1.65rem !important;
    letter-spacing: -0.03em;
    margin-bottom: 0.15rem !important;
}}
h2 {{
    font-weight: 600 !important;
    color: {TEXT_PRIMARY} !important;
    font-size: 1.2rem !important;
    letter-spacing: -0.015em;
}}
h3 {{
    font-weight: 600 !important;
    color: {TEXT_PRIMARY} !important;
    font-size: 1.05rem !important;
}}

/* ── Buttons ────────────────────────────────────────────── */
.stButton > button {{
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 1.15rem;
    border: 1px solid {BORDER};
    background: {SURFACE};
    color: {TEXT_PRIMARY};
    transition: all 0.12s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}}
.stButton > button:hover {{
    border-color: {ACCENT};
    color: {ACCENT};
    background: {ACCENT_LIGHT};
    box-shadow: 0 1px 3px rgba(79,70,229,0.08);
}}
.stButton > button:active {{
    transform: scale(0.98);
}}

/* ── Inputs ─────────────────────────────────────────────── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea textarea {{
    border-radius: 8px !important;
    border-color: {BORDER} !important;
    font-size: 0.88rem;
}}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div:focus-within {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 2px {ACCENT_LIGHT} !important;
}}
.stRadio > div label {{
    font-size: 0.88rem;
}}

/* ── Dataframe ──────────────────────────────────────────── */
.stDataFrame {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    overflow: hidden;
}}

/* ── Divider ────────────────────────────────────────────── */
hr {{
    border: none;
    border-top: 1px solid {BORDER};
    margin: 1.25rem 0;
}}

/* ── Hide default st.metric (we use custom cards) ───────── */
[data-testid="stMetric"] {{
    display: none;
}}

/* ──────────────────────────────────────────────────────────
   Custom Component Classes
   ────────────────────────────────────────────────────────── */

/* Metric / KPI Card */
.kpi-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.35rem 1.4rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {TEXT_MUTED};
    margin-bottom: 0.3rem;
}}
.kpi-value {{
    font-size: 1.85rem;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    line-height: 1.15;
}}

/* Content Card */
.card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 0.65rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.15s ease;
}}
.card:hover {{
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.card-name {{
    font-size: 0.95rem;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin: 0 0 0.45rem 0;
}}
.card-row {{
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.2rem;
    font-size: 0.84rem;
    line-height: 1.5;
}}
.card-label {{
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-size: 0.68rem;
    color: {TEXT_MUTED};
    min-width: 62px;
}}
.card-value {{
    color: {TEXT_PRIMARY};
    font-weight: 500;
}}
.card-bio {{
    margin-top: 0.55rem;
    font-size: 0.84rem;
    color: {TEXT_SECONDARY};
    line-height: 1.55;
}}

/* Section Header */
.section-hdr {{
    font-size: 1rem;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin: 2rem 0 0.85rem 0;
    padding-bottom: 0.55rem;
    border-bottom: 1px solid {BORDER};
    letter-spacing: -0.01em;
}}

/* Page Subtitle */
.page-sub {{
    font-size: 0.92rem;
    color: {TEXT_SECONDARY};
    margin-bottom: 1.75rem;
    line-height: 1.55;
}}

/* Badges / Pills */
.badge {{
    display: inline-block;
    padding: 0.18rem 0.58rem;
    border-radius: 9999px;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    line-height: 1.5;
    vertical-align: middle;
}}
.badge-beginner    {{ background: #ecfdf5; color: #059669; }}
.badge-intermediate {{ background: #eff6ff; color: #2563eb; }}
.badge-advanced    {{ background: #fef3c7; color: #d97706; }}
.badge-pending     {{ background: #fef3c7; color: #d97706; }}
.badge-accepted    {{ background: #ecfdf5; color: #059669; }}
.badge-completed   {{ background: #eff6ff; color: #2563eb; }}

/* Profile skills section */
.profile-box {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    min-height: 160px;
}}
.profile-box-title {{
    font-size: 0.88rem;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin-bottom: 0.75rem;
}}
.skill-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.35rem 0;
    font-size: 0.84rem;
    color: {TEXT_PRIMARY};
}}
.skill-row + .skill-row {{
    border-top: 1px solid #f3f4f6;
}}

/* Swap request card header */
.swap-header {{
    display: flex;
    align-items: center;
    gap: 0.45rem;
    flex-wrap: wrap;
    margin-bottom: 0.65rem;
}}
.swap-arrow {{
    color: {TEXT_MUTED};
    font-size: 0.9rem;
}}

/* Spacer utility */
.spacer-sm {{ height: 0.5rem; }}
.spacer-md {{ height: 1rem; }}
.spacer-lg {{ height: 1.75rem; }}
</style>
""", unsafe_allow_html=True)


# ================================================================
#  UI Helper Functions
# ================================================================

def render_kpi(label, value):
    """Render a clean KPI metric card."""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section(title):
    """Render a section header with a subtle bottom border."""
    st.markdown(f'<div class="section-hdr">{title}</div>',
                unsafe_allow_html=True)


def skill_badge(level):
    """Return HTML for a skill-level pill badge."""
    return (f'<span class="badge badge-{level.lower()}">'
            f'{level}</span>')


def status_badge(status):
    """Return HTML for a status pill badge."""
    return (f'<span class="badge badge-{status.lower()}">'
            f'{status}</span>')


def spacer(size="md"):
    st.markdown(f'<div class="spacer-{size}"></div>',
                unsafe_allow_html=True)


# ================================================================
#  Sidebar Navigation
# ================================================================

with st.sidebar:
    st.markdown(
        f'<div style="padding:0 0.25rem;">'
        f'<p style="margin:0; font-size:1.15rem; font-weight:700; '
        f'color:{TEXT_PRIMARY}; letter-spacing:-0.02em;">SkillSwap</p>'
        f'<p style="margin:0.2rem 0 1.6rem 0; font-size:0.78rem; '
        f'color:{TEXT_MUTED};">Exchange Skills. Learn Together.</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigate",
        [
            "Home",
            "My Profile",
            "Skills",
            "Find Matches",
            "Swap Requests",
            "Dashboard"
        ],
        label_visibility="collapsed"
    )


# ================================================================
#  HOME
# ================================================================

if page == "Home":

    st.markdown("# SkillSwap")
    st.markdown(
        '<p class="page-sub">'
        'A peer-to-peer platform where people can exchange knowledge, '
        'discover new skills, and connect with people who can teach them.'
        '</p>',
        unsafe_allow_html=True
    )

    # ---- KPI row ----

    users = fetch_data(
        "SELECT COUNT(*) AS total FROM users"
    )[0]["total"]

    skills = fetch_data(
        "SELECT COUNT(*) AS total FROM skills"
    )[0]["total"]

    requests = fetch_data(
        "SELECT COUNT(*) AS total FROM swap_requests"
    )[0]["total"]

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi("Members", users)
    with c2:
        render_kpi("Skills", skills)
    with c3:
        render_kpi("Swap Requests", requests)

    # ---- Community Skill Pool ----

    render_section("Community Skill Pool")

    teachers = fetch_data(
        """
        SELECT
            u.name,
            s.skill_name,
            us.skill_level,
            u.bio
        FROM user_skills us
        JOIN users u ON us.user_id = u.user_id
        JOIN skills s ON us.skill_id = s.skill_id
        WHERE us.skill_type = 'TEACH'
        ORDER BY u.name
        """
    )

    for person in teachers:
        lvl = skill_badge(person["skill_level"])
        bio = person["bio"] or ""
        st.markdown(f"""
        <div class="card">
            <div class="card-name">{person['name']}</div>
            <div class="card-row">
                <span class="card-label">Teaches</span>
                <span class="card-value">{person['skill_name']}</span>
                {lvl}
            </div>
            <div class="card-bio">{bio}</div>
        </div>
        """, unsafe_allow_html=True)


# ================================================================
#  MY PROFILE
# ================================================================

elif page == "My Profile":

    st.markdown("# My Profile")

    users = fetch_data(
        "SELECT user_id, name, email, bio FROM users ORDER BY name"
    )

    selected_user = st.selectbox(
        "Select a user",
        users,
        format_func=lambda x: x["name"]
    )

    spacer("sm")

    # Profile info card
    bio_text = selected_user["bio"] or ""
    st.markdown(f"""
    <div class="card">
        <div class="card-name" style="font-size:1.05rem;
             margin-bottom:0.55rem;">{selected_user['name']}</div>
        <div class="card-row">
            <span class="card-label">Email</span>
            <span class="card-value">{selected_user['email']}</span>
        </div>
        <div class="card-bio">{bio_text}</div>
    </div>
    """, unsafe_allow_html=True)

    spacer("sm")

    teach = fetch_data(
        """
        SELECT s.skill_name, us.skill_level
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.skill_id
        WHERE us.user_id = %s
        AND us.skill_type = 'TEACH'
        """,
        (selected_user["user_id"],)
    )

    learn = fetch_data(
        """
        SELECT s.skill_name, us.skill_level
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.skill_id
        WHERE us.user_id = %s
        AND us.skill_type = 'LEARN'
        """,
        (selected_user["user_id"],)
    )

    col1, col2 = st.columns(2)

    with col1:
        teach_rows = ""
        if teach:
            for s in teach:
                teach_rows += (
                    f'<div class="skill-row">'
                    f'<span>{s["skill_name"]}</span>'
                    f'{skill_badge(s["skill_level"])}'
                    f'</div>'
                )
        else:
            teach_rows = (
                '<p style="font-size:0.84rem; color:#9ca3af; '
                'margin:0.5rem 0 0 0;">No teaching skills added yet.</p>'
            )

        st.markdown(f"""
        <div class="profile-box">
            <div class="profile-box-title">Skills I Teach</div>
            {teach_rows}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        learn_rows = ""
        if learn:
            for s in learn:
                learn_rows += (
                    f'<div class="skill-row">'
                    f'<span>{s["skill_name"]}</span>'
                    f'{skill_badge(s["skill_level"])}'
                    f'</div>'
                )
        else:
            learn_rows = (
                '<p style="font-size:0.84rem; color:#9ca3af; '
                'margin:0.5rem 0 0 0;">No learning goals added yet.</p>'
            )

        st.markdown(f"""
        <div class="profile-box">
            <div class="profile-box-title">Skills I Want to Learn</div>
            {learn_rows}
        </div>
        """, unsafe_allow_html=True)


# ================================================================
#  SKILLS
# ================================================================

elif page == "Skills":

    st.markdown("# Skills")
    st.markdown(
        '<p class="page-sub">'
        'Add a skill you can teach or a skill you want to learn.'
        '</p>',
        unsafe_allow_html=True
    )

    # ---- Add Skill form ----

    render_section("Add Skill")

    users = fetch_data(
        "SELECT user_id, name FROM users ORDER BY name"
    )

    skills = fetch_data(
        "SELECT skill_id, skill_name FROM skills ORDER BY skill_name"
    )

    left, right = st.columns(2)

    with left:
        selected_user = st.selectbox(
            "User",
            users,
            format_func=lambda x: x["name"]
        )
        skill_type = st.radio(
            "Skill type",
            ["TEACH", "LEARN"],
            horizontal=True
        )

    with right:
        selected_skill = st.selectbox(
            "Skill",
            skills,
            format_func=lambda x: x["skill_name"]
        )
        skill_level = st.selectbox(
            "Skill level",
            ["BEGINNER", "INTERMEDIATE", "ADVANCED"]
        )

    spacer("sm")

    if st.button("Add Skill", use_container_width=True):

        existing = fetch_data(
            """
            SELECT user_skill_id
            FROM user_skills
            WHERE user_id = %s
            AND skill_id = %s
            AND skill_type = %s
            """,
            (
                selected_user["user_id"],
                selected_skill["skill_id"],
                skill_type
            )
        )

        if existing:
            st.warning("This skill is already added.")

        else:
            execute_query(
                """
                INSERT INTO user_skills
                (user_id, skill_id, skill_type, skill_level)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    selected_user["user_id"],
                    selected_skill["skill_id"],
                    skill_type,
                    skill_level
                )
            )

            st.success(
                f"{selected_skill['skill_name']} added for "
                f"{selected_user['name']}!"
            )

    # ---- Current records ----

    render_section("Current Skill Records")

    records = fetch_data(
        """
        SELECT
            u.name AS user_name,
            s.skill_name,
            us.skill_type,
            us.skill_level
        FROM user_skills us
        JOIN users u ON us.user_id = u.user_id
        JOIN skills s ON us.skill_id = s.skill_id
        ORDER BY u.name, s.skill_name
        """
    )

    if records:
        st.dataframe(
            records,
            use_container_width=True
        )


# ================================================================
#  FIND MATCHES
# ================================================================

elif page == "Find Matches":

    st.markdown("# Find Matches")
    st.markdown(
        '<p class="page-sub">'
        'Find people who can teach you a skill you want to learn.'
        '</p>',
        unsafe_allow_html=True
    )

    skills = fetch_data(
        "SELECT skill_id, skill_name FROM skills ORDER BY skill_name"
    )

    selected_skill = st.selectbox(
        "What skill do you want to learn?",
        skills,
        format_func=lambda x: x["skill_name"]
    )

    if st.button("Find Matches"):

        matches = fetch_data(
            """
            SELECT DISTINCT
                u.user_id,
                u.name,
                u.email,
                u.bio,
                s.skill_id,
                s.skill_name,
                us.skill_level
            FROM user_skills us
            JOIN users u ON us.user_id = u.user_id
            JOIN skills s ON us.skill_id = s.skill_id
            WHERE us.skill_type = 'TEACH'
            AND us.skill_id = %s
            """,
            (selected_skill["skill_id"],)
        )

        if matches:

            st.success(
                f"Found {len(matches)} potential match(es)!"
            )

            for match in matches:

                lvl = skill_badge(match["skill_level"])
                bio = match["bio"] or ""

                st.markdown(f"""
                <div class="card">
                    <div class="card-name">{match['name']}</div>
                    <div class="card-row">
                        <span class="card-label">Email</span>
                        <span class="card-value">{match['email']}</span>
                    </div>
                    <div class="card-row">
                        <span class="card-label">Teaches</span>
                        <span class="card-value">{match['skill_name']}</span>
                        {lvl}
                    </div>
                    <div class="card-bio">{bio}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "Send Swap Request",
                    key=f"send_{match['user_id']}_{match['skill_id']}"
                ):

                    offered_skills = fetch_data(
                        """
                        SELECT skill_id
                        FROM user_skills
                        WHERE user_id = 1
                        AND skill_type = 'TEACH'
                        LIMIT 1
                        """
                    )

                    if not offered_skills:

                        st.error(
                            "You need to teach at least one skill "
                            "before sending a request."
                        )

                    else:

                        execute_query(
                            """
                            INSERT INTO swap_requests
                            (
                                sender_id,
                                receiver_id,
                                skill_offered_id,
                                skill_requested_id,
                                message,
                                status
                            )
                            VALUES (%s, %s, %s, %s, %s, 'PENDING')
                            """,
                            (
                                1,
                                match["user_id"],
                                offered_skills[0]["skill_id"],
                                selected_skill["skill_id"],
                                "I would like to exchange skills with you!"
                            )
                        )

                        st.success(
                            f"Swap request sent to {match['name']}!"
                        )

        else:

            st.info(
                "No matches found for this skill yet."
            )


# ================================================================
#  SWAP REQUESTS
# ================================================================

elif page == "Swap Requests":

    st.markdown("# Swap Requests")

    requests = fetch_data(
        """
        SELECT
            sr.request_id,
            sender.name AS sender,
            receiver.name AS receiver,
            offered.skill_name AS offered_skill,
            requested.skill_name AS requested_skill,
            sr.status,
            sr.message,
            DATE_FORMAT(sr.requested_at, '%d %b %Y %H:%i') AS request_time
        FROM swap_requests sr
        JOIN users sender
            ON sr.sender_id = sender.user_id
        JOIN users receiver
            ON sr.receiver_id = receiver.user_id
        JOIN skills offered
            ON sr.skill_offered_id = offered.skill_id
        JOIN skills requested
            ON sr.skill_requested_id = requested.skill_id
        ORDER BY sr.requested_at DESC
        """
    )

    if requests:

        for request in requests:

            s_badge = status_badge(request["status"])
            msg = request["message"] or ""

            st.markdown(f"""
            <div class="card">
                <div class="swap-header">
                    <span class="card-name" style="margin:0;">
                        {request['sender']}</span>
                    <span class="swap-arrow">&rarr;</span>
                    <span class="card-name" style="margin:0;">
                        {request['receiver']}</span>
                    <span style="margin-left:auto;">{s_badge}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">Offering</span>
                    <span class="card-value">
                        {request['offered_skill']}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">Wants</span>
                    <span class="card-value">
                        {request['requested_skill']}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">Requested</span>
                    <span class="card-value">
                        {request['request_time']}</span>
                </div>
                <div class="card-bio" style="font-style:italic;">
                    {msg}</div>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info("No swap requests yet.")


# ================================================================
#  DASHBOARD
# ================================================================

elif page == "Dashboard":

    st.markdown("# Dashboard")

    completed = fetch_data(
        """
        SELECT COUNT(*) AS total
        FROM swap_requests
        WHERE status = 'COMPLETED'
        """
    )[0]["total"]

    accepted = fetch_data(
        """
        SELECT COUNT(*) AS total
        FROM swap_requests
        WHERE status = 'ACCEPTED'
        """
    )[0]["total"]

    pending = fetch_data(
        """
        SELECT COUNT(*) AS total
        FROM swap_requests
        WHERE status = 'PENDING'
        """
    )[0]["total"]

    total_sessions = fetch_data(
        """
        SELECT COUNT(*) AS total
        FROM swap_sessions
        """
    )[0]["total"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("Completed", completed)
    with c2:
        render_kpi("Accepted", accepted)
    with c3:
        render_kpi("Pending", pending)
    with c4:
        render_kpi("Sessions", total_sessions)

    render_section("Swap Activity")

    chart_data = {
        "Status": ["Pending", "Accepted", "Completed"],
        "Requests": [pending, accepted, completed]
    }

    st.bar_chart(
        chart_data,
        x="Status",
        y="Requests"
    )

    render_section("Top Skills")

    top_skills = fetch_data(
        """
        SELECT
            s.skill_name,
            COUNT(*) AS total_users
        FROM user_skills us
        JOIN skills s
            ON us.skill_id = s.skill_id
        GROUP BY s.skill_id, s.skill_name
        ORDER BY total_users DESC
        LIMIT 5
        """
    )

    if top_skills:
        st.dataframe(
            top_skills,
            use_container_width=True
        )