from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True
)

def save_chat(user,response):

    memory.save_context(
        {"input":user},
        {"output":response}
    )