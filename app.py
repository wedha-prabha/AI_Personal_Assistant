import streamlit as st

from models.oss_model import get_oss_response
from models.frontier_model import get_frontier_response
from memory.chat_memory import load_chat_history, save_chat
from guardrails.safety import check_safety
from observability.logger import log_trace

st.set_page_config(
    page_title="AI Personal Assistant",
    layout="wide",
    page_icon="🤖",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()
    st.session_state.log_output = ""
    st.session_state.last_prompt = ""
    st.session_state.last_response = ""

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 10px;
    }
    .chat-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: none;
        color: #ffffff;
    }
    .assistant-bubble,
    .user-bubble {
        background: rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 16px;
        margin-bottom: 12px;
        border: none;
        color: #ffffff;
    }
    .assistant-bubble strong,
    .user-bubble strong,
    .chat-card strong,
    .chat-card em {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("AI Personal Assistant")
    st.markdown("#### Conversational interface with Open Source and Frontier assistants")
with header_col2:
    st.metric("Messages", len(st.session_state.chat_history))
    st.metric("Last assistant", st.session_state.chat_history[-1]["assistant"] if st.session_state.chat_history else "None")

with st.sidebar:
    st.header("Quick prompts")
    suggestions = [
        "Explain your purpose in one sentence",
        "How can I use you for my daily work?",
        "What's the difference between Open Source and Frontier?",
    ]
    for suggestion in suggestions:
        if st.button(suggestion, key=f"suggestion_{suggestion}"):
            st.session_state.prompt_text = suggestion
    st.divider()
    st.markdown("**Assistant controls**")
    st.write("Choose the assistant below, then ask a question.")
    if st.button("Clear all history", key="sidebar_clear_history"):
        st.session_state.chat_history = []
        st.session_state.log_output = ""
        st.session_state.last_prompt = ""
        st.session_state.last_response = ""
        st.rerun()
    st.divider()
    st.markdown("#### Tips")
    st.write("- Use Frontier for higher-quality cloud responses")
    st.write("- Use Open Source for local inference and experimentation")
    st.write("- Click a suggestion to fill the prompt field")

assistant = st.selectbox("Choose Assistant", ["Open Source", "Frontier"], key="assistant_choice")

chat_tab, history_tab = st.tabs(["💬 Chat", "🕘 History"])

with chat_tab:
    with st.container():
        st.markdown("### Start a conversation")
        prompt = st.text_area("Ask something", height=140, key="prompt_text")

        if st.button("Send", key="send_button", type="primary"):
            prompt_value = st.session_state.prompt_text
            if not prompt_value or not prompt_value.strip():
                st.warning("Please enter a prompt before sending.")
            elif not check_safety(prompt_value):
                st.error("Unsafe request")
            else:
                if assistant == "Open Source":
                    response = get_oss_response(prompt_value)
                else:
                    response = get_frontier_response(prompt_value)

                save_chat(prompt_value, response, assistant=assistant)
                st.session_state.chat_history = st.session_state.chat_history + [
                    {"assistant": assistant, "input": prompt_value, "output": response}
                ]
                st.session_state.last_prompt = prompt_value
                st.session_state.last_response = response
                st.session_state.log_output = log_trace(prompt_value, response, assistant_name=assistant)
                st.success("Response generated")

    st.markdown("---")
    st.markdown("### Conversation")
    if st.session_state.chat_history:
        for entry in reversed(st.session_state.chat_history[-20:]):
            if entry.get("assistant") == "Open Source":
                st.markdown(
                    f"<div class='assistant-bubble'><strong>Open Source:</strong> {entry['output']}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='assistant-bubble'><strong>Frontier:</strong> {entry['output']}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"<div class='user-bubble'><strong>You:</strong> {entry['input']}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No conversation history yet. Send a prompt to begin.")

with history_tab:
    st.markdown("### Saved conversation history")
    if st.session_state.chat_history:
        for entry in reversed(st.session_state.chat_history):
            st.markdown(
                f"<div class='chat-card'><strong>{entry.get('assistant', 'Assistant')}</strong><br><em>{entry['input']}</em><br><br>{entry['output']}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("History is empty. Ask a question in the Chat tab to populate it.")

with st.expander("Observability / Langfuse output", expanded=True):
    if st.session_state.log_output:
        st.code(st.session_state.log_output)
    else:
        st.info("No logs to display yet.")
