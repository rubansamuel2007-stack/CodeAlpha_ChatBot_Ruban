
import streamlit as st
from chatbot import FAQChatbot


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CodeAlpha Chatbot | Smart FAQ Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# PROFESSIONAL UI STYLING
# ==================================================

st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f4f7fc 0%,
            #eef3fb 100%
        );
        color: #172b4d;
    }

    /* Main content spacing */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Global readable text */
    html, body, [class*="st-"] {
        font-family: "Segoe UI", Arial, sans-serif;
    }

    /* Main heading */
    .hero-title {
        color: #12346b !important;
        font-size: 43px;
        font-weight: 800;
        letter-spacing: -1.2px;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #526783 !important;
        font-size: 16px;
        line-height: 1.7;
        margin-bottom: 18px;
    }

    /* Section headings */
    h1, h2, h3 {
        color: #173765 !important;
    }

    /* Normal markdown text */
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown label {
        color: #253858;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #102b50;
        border-right: 1px solid #d8e2f0;
    }

    section[data-testid="stSidebar"] * {
        color: #f4f7ff !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        background: #ffffff;
        color: #173765 !important;
        border: 1px solid #d5e1f2;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton button p {
        color: #173765 !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #dceaff;
        border-color: #9bbcf0;
        transform: translateY(-1px);
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 18px;
        border: 1px solid #dce6f3;
        border-radius: 15px;
        box-shadow: 0 4px 14px rgba(20, 48, 90, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #526783 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #12346b !important;
        font-weight: 800;
    }

    /* Chat message containers */
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        border: 1px solid #dce5f1;
        padding: 14px 16px;
        margin-bottom: 14px;
        box-shadow: 0 3px 12px rgba(25, 50, 85, 0.04);
    }

    /* User chat bubble */
    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-user"]
    ) {
        background: #e2edff;
        border-color: #c4d8fa;
    }

    /* Assistant chat bubble */
    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #ffffff;
        border-color: #d9e5f3;
    }

    /* FIX: Force readable text inside ALL chat bubbles */
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] strong,
    div[data-testid="stChatMessage"] em {
        color: #172b4d !important;
        line-height: 1.75;
    }

    div[data-testid="stChatMessage"] a {
        color: #0759bd !important;
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        background: #ffffff;
        border-radius: 15px;
    }

    div[data-testid="stChatInput"] textarea {
        color: #172b4d !important;
        background: #ffffff !important;
        -webkit-text-fill-color: #172b4d !important;
        caret-color: #12346b !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #718096 !important;
        -webkit-text-fill-color: #718096 !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] button {
        background: #174a91 !important;
        border-radius: 10px;
    }

    /* Standard buttons */
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #dce6f3;
        border-radius: 12px;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] p {
        color: #173765 !important;
    }

    /* Divider */
    hr {
        border-color: #d8e3f1 !important;
    }

    /* Hero information card */
    .welcome-card {
        background: linear-gradient(
            120deg,
            #12346b,
            #2365b7
        );
        padding: 23px 25px;
        border-radius: 17px;
        margin: 12px 0 22px 0;
        box-shadow: 0 8px 22px rgba(18, 52, 107, 0.15);
    }

    .welcome-card h3 {
        color: #ffffff !important;
        margin-top: 0;
        margin-bottom: 8px;
    }

    .welcome-card p {
        color: #edf4ff !important;
        margin-bottom: 0;
        line-height: 1.7;
    }

    /* Footer */
    .footer-text {
        color: #667994 !important;
        font-size: 13px;
        text-align: center;
        padding: 12px 0;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .block-container {
            padding-top: 1rem;
        }

        div[data-testid="stChatMessage"] {
            padding: 10px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)




@st.cache_resource
def create_chatbot():
    return FAQChatbot()


try:
    chatbot = create_chatbot()

except Exception as error:
    st.error(
        "Unable to load FAQMate. Please check your "
        "FAQ database and installed Python packages."
    )

    with st.expander("Technical error details"):
        st.code(str(error))

    st.stop()




if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to CodeAlpha Chatbot.\n\n"
                "I'm your smart FAQ assistant. I can help "
                "you find information about admissions, "
                "examinations, library services, and more.\n\n"
                "What would you like to know today?"
            )
        }
    ]




st.markdown(
    """
    <div class="hero-title">🤖 CodeAlpha Chatbot</div>
    <div class="hero-subtitle">
        Your intelligent assistant for quick and reliable
        answers to frequently asked questions.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="welcome-card">
        <h3>Welcome to your smart FAQ assistant</h3>
        <p>
            Ask your question in natural language.
            FAQMate searches its knowledge base and finds
            the most relevant available answer.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## 🤖 CodeAlpha Chatbot")
    st.caption("SMART FAQ ASSISTANT")

    st.divider()

    st.markdown("### 📚 Knowledge Base")

 

    st.write(
        "Ask questions about the topics stored in the "
        "FAQ database."
    )

    st.divider()

    st.markdown("### 💡 Try asking")

    example_questions = [
        "What is your name?",
        "How can I contact support?",
        "How do I reset my password?",
        "How can I apply for admission?",
        "How do I get my exam timetable?",
    ]

    for index, example in enumerate(example_questions):

        if st.button(
            example,
            key=f"example_{index}",
            use_container_width=True
        ):
            st.session_state.pending_question = example
            st.rerun()

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 Welcome back to CodeAlpha Chatbot. "
                    "What would you like to know today?"
                )
            }
        ]

        st.rerun()

    st.divider()

    st.caption(
        "Built with Python, NLTK, Scikit-learn and Streamlit."
    )


# ==================================================
# DASHBOARD METRICS
# ==================================================

user_count = sum(
    1 for message in st.session_state.messages
    if message["role"] == "user"
)

assistant_count = sum(
    1 for message in st.session_state.messages
    if message["role"] == "assistant"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Your Questions", user_count)

with col2:
    st.metric("🤖 Bot Responses", assistant_count)

with col3:
    st.metric("📚 FAQs Available", len(chatbot.faqs))


st.divider()

st.markdown("### 💬 Chat with CodeAlpha Chatbot")

st.caption(
    "Enter a question below, or select an example "
    "from the sidebar to get started."
)




for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🤖" if message["role"] == "assistant" else "🧑"
    ):

        st.markdown(message["content"])

        if message.get("matched_question"):

            with st.expander("🔎 View matching details"):

                st.markdown(
                    f"**Matched FAQ:** "
                    f"{message['matched_question']}"
                )

                st.markdown(
                    f"**Text similarity:** "
                    f"{message['confidence']:.2%}"
                )




pending_question = st.session_state.pop(
    "pending_question",
    None
)

user_question = st.chat_input(
    "✍️ Type your question here..."
)

question = pending_question or user_question

if question:

    # Save and display the user's question.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    # Find the most relevant answer.
    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("🔍 Searching the FAQ database..."):

            result = chatbot.get_response(question)

        st.markdown(result["answer"])

        if result["matched"]:

            with st.expander("********🔎******** "):

                st.markdown(
                    f"**Matched FAQ:** "
                    f"{result['matched_question']}"
                )

                st.markdown(
                    f"**Text similarity:** "
                    f"{result['confidence']:.2%}"
                )

    # Save the answer and its matching information.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "matched_question": result["matched_question"],
            "confidence": result["confidence"],
            "matched": result["matched"]
        }
    )




st.divider()

st.markdown(
    """
    <div class="footer-text">
        FAQMate · CodeAlpha AI Internship — Task 2<br>
        Intelligent FAQ Retrieval · Built with Python
    </div>
    """,
    unsafe_allow_html=True
)
