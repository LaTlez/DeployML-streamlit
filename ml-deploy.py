# API
from hugchat import hugchat
from hugchat.login import Login

# Log in to huggingface and grant authorization to huggingchat
EMAIL = "your email"
PASSWD = "your password"
cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Create your ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

# Non stream response
query_result = chatbot.chat("Hi!")
print(query_result) # or query_result.text or query_result["text"]

# Stream response
for resp in chatbot.query(
    "Hello",
    stream=True
):
    print(resp)

# Web search (new feature)
query_result = chatbot.query("Hi!", web_search=True)
print(query_result)
for source in query_result.web_search_sources:
    print(source.link)
    print(source.title)
    print(source.hostname)

# Create a new conversation
chatbot.new_conversation(switch_to = True) # switch to the new conversation

# Get conversations on the server that are not from the current session (all your conversations in huggingchat)
conversation_list = chatbot.get_remote_conversations(replace_conversation_list=True)
# Get conversation list(local)
conversation_list = chatbot.get_conversation_list()

# Get the available models (not hardcore)
models = chatbot.get_available_llm_models()

# Switch model with given index
chatbot.switch_llm(0) # Switch to the first model
chatbot.switch_llm(1) # Switch to the second model

# Get information about the current conversation
info = chatbot.get_conversation_info()
print(info.id, info.title, info.model, info.system_prompt, info.history)

# Assistant
assistant = chatbot.search_assistant(assistant_name="ChatGpt") # assistant name list in https://huggingface.co/chat/assistants
assistant_list = chatbot.get_assistant_list_by_page(page=0)
chatbot.new_conversation(assistant=assistant, switch_to=True) # create a new conversation with assistant

# [DANGER] Delete all the conversations for the logged in user
chatbot.delete_all_conversations()

# App Interfacing
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat

st.set_page_config(page_title="ChatMATE - Chat Multi-purpose AI Technology")

# Generate empty lists for bot_response and user_input.
## bot_response stores AI generated responses
if 'bot_response' not in st.session_state:
    st.session_state['bot_response'] = ["I'm ChatMATE, How may I help you?"]
## user_input stores User's questions
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_input():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_input()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    chatbot = hugchat.ChatBot(cookie_path="cookies.json")
    response = chatbot.chat(prompt)
    return response

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.user_input.append(user_input)
        st.session_state.bot_response.append(response)

    if st.session_state['bot_response']:
        for i in range(len(st.session_state['bot_response'])):
            message(st.session_state['user_input'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['bot_response'][i], key=str(i))
