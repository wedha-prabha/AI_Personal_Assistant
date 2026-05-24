from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True
)

def save_chat(user,response):

    memory.save_context(

        {"input":user},
        {"output":response}
    )


def load_chat():

    return memory.load_memory_variables({})