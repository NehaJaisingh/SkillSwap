import streamlit as st
from db import get_connection

st.set_page_config(
    page_title="SkillSwap",
    page_icon="🤝",
    layout="wide"
)


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


# ---------------- SIDEBAR ----------------

st.sidebar.title("🤝 SkillSwap")
st.sidebar.caption("Exchange Skills. Learn Together.")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👤 My Profile",
        "🧠 Skills",
        "🤝 Find Matches",
        "📩 Swap Requests",
        "📊 Dashboard"
    ]
)


# ---------------- HOME ----------------

if page == "🏠 Home":

    st.title("🤝 SkillSwap")
    st.subheader("Exchange Skills. Learn Together.")

    st.write(
        "A peer-to-peer platform where people can exchange knowledge, "
        "discover new skills, and connect with people who can teach them."
    )

    st.divider()

    users = fetch_data(
        "SELECT COUNT(*) AS total FROM users"
    )[0]["total"]

    skills = fetch_data(
        "SELECT COUNT(*) AS total FROM skills"
    )[0]["total"]

    requests = fetch_data(
        "SELECT COUNT(*) AS total FROM swap_requests"
    )[0]["total"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Members", users)

    with col2:
        st.metric("🧠 Skills", skills)

    with col3:
        st.metric("🤝 Swap Requests", requests)

    st.divider()

    st.subheader("🌟 Community Skill Pool")

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
        with st.container(border=True):
            st.write(f"### 👤 {person['name']}")
            st.write(f"**Can teach:** {person['skill_name']}")
            st.write(f"**Level:** {person['skill_level']}")
            st.write(person["bio"])


# ---------------- MY PROFILE ----------------

elif page == "👤 My Profile":

    st.title("👤 My Profile")

    users = fetch_data(
        "SELECT user_id, name, email, bio FROM users ORDER BY name"
    )

    selected_user = st.selectbox(
        "Select a user",
        users,
        format_func=lambda x: x["name"]
    )

    st.divider()

    st.subheader(selected_user["name"])

    st.write(f"📧 **Email:** {selected_user['email']}")
    st.write(f"📝 **Bio:** {selected_user['bio']}")

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
        st.subheader("🎓 Skills I Teach")

        if teach:
            for skill in teach:
                st.write(
                    f"• {skill['skill_name']} — {skill['skill_level']}"
                )
        else:
            st.info("No teaching skills added yet.")

    with col2:
        st.subheader("📚 Skills I Want to Learn")

        if learn:
            for skill in learn:
                st.write(
                    f"• {skill['skill_name']} — {skill['skill_level']}"
                )
        else:
            st.info("No learning goals added yet.")


# ---------------- SKILLS ----------------

elif page == "🧠 Skills":

    st.title("🧠 Skill Management")

    st.write(
        "Add a skill you can teach or a skill you want to learn."
    )

    users = fetch_data(
        "SELECT user_id, name FROM users ORDER BY name"
    )

    skills = fetch_data(
        "SELECT skill_id, skill_name FROM skills ORDER BY skill_name"
    )

    selected_user = st.selectbox(
        "Select user",
        users,
        format_func=lambda x: x["name"]
    )

    selected_skill = st.selectbox(
        "Select skill",
        skills,
        format_func=lambda x: x["skill_name"]
    )

    skill_type = st.radio(
        "Skill type",
        ["TEACH", "LEARN"],
        horizontal=True
    )

    skill_level = st.selectbox(
        "Skill level",
        ["BEGINNER", "INTERMEDIATE", "ADVANCED"]
    )

    if st.button("➕ Add Skill", use_container_width=True):

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

    st.divider()

    st.subheader("📋 Current Skill Records")

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


# ---------------- FIND MATCHES ----------------

elif page == "🤝 Find Matches":

    st.title("🤝 Find Your Skill Match")

    st.write(
        "Find people who can teach you a skill you want to learn."
    )

    skills = fetch_data(
        "SELECT skill_id, skill_name FROM skills ORDER BY skill_name"
    )

    selected_skill = st.selectbox(
        "What skill do you want to learn?",
        skills,
        format_func=lambda x: x["skill_name"]
    )

    if st.button("🔍 Find Matches"):

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

                with st.container(border=True):

                    st.write(f"### 👤 {match['name']}")

                    st.write(
                        f"**Teaches:** {match['skill_name']}"
                    )

                    st.write(
                        f"**Skill Level:** {match['skill_level']}"
                    )

                    st.write(match["bio"])

                    if st.button(
                        "📩 Send Swap Request",
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


# ---------------- SWAP REQUESTS ----------------

elif page == "📩 Swap Requests":

    st.title("📩 Swap Requests")

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

            with st.container(border=True):

                st.write(
                    f"### 🤝 {request['sender']} → {request['receiver']}"
                )

                st.write(
                    f"**Offering:** {request['offered_skill']}"
                )

                st.write(
                    f"**Wants:** {request['requested_skill']}"
                )

                st.write(
                    f"**Status:** `{request['status']}`"
                )

                st.write(
                    f"🕒 {request['request_time']}"
                )

                st.write(request["message"])

    else:

        st.info("No swap requests yet.")


# ---------------- DASHBOARD ----------------

elif page == "📊 Dashboard":

    st.title("📊 SkillSwap Dashboard")

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("✅ Completed", completed)

    with col2:
        st.metric("🤝 Accepted", accepted)

    with col3:
        st.metric("⏳ Pending", pending)

    with col4:
        st.metric("📅 Sessions", total_sessions)

    st.divider()

    st.subheader("📈 Swap Activity")

    chart_data = {
        "Status": ["Pending", "Accepted", "Completed"],
        "Requests": [pending, accepted, completed]
    }

    st.bar_chart(
        chart_data,
        x="Status",
        y="Requests"
    )

    st.divider()

    st.subheader("🏆 Top Skills")

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