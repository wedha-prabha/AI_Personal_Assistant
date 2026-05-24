import streamlit as st

from models.oss_model import get_oss_response
from models.frontier_model import get_frontier_response

from memory.chat_memory import save_chat

from guardrails.safety import check_safety

from observability.logger import log_trace

st.title(
    "AI Personal Assistant"
)

option=st.selectbox(

    "Choose Assistant",

    ["Open Source","Frontier"]
)

prompt=st.text_input(
    "Ask something"
)

if st.button(
    "Send"
):

    if not check_safety(
        prompt
    ):

        st.error(
            "Unsafe request"
        )

    else:

        if option=="Open Source":

            response=get_oss_response(
                prompt
            )

        else:

            response=get_frontier_response(
                prompt
            )

        save_chat(
            prompt,
            response
        )

        log_trace(
            prompt,
            response
        )

        st.write(
            response
        )