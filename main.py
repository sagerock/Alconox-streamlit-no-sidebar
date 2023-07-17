import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv()
import openai
import pinecone
import tiktoken

# When you are working locally set your api keys with this:
# openai.api_key = os.getenv('OPENAI_API_KEY')
# pinecone_api_key = os.getenv('PINECONE_API_KEY')

# When you are uploading to Streamlit, set your keys like this:
pinecone_api_key = st.secrets["API_KEYS"]["pinecone"]
openai.api_key = st.secrets["API_KEYS"]["openai"]

pinecone.init(api_key=pinecone_api_key, environment="us-west4-gcp")

# Define the name of the index and the dimensionality of the embeddings
index_name = "sagerock"
dimension = 1536

pineconeindex = pinecone.Index(index_name)

# Import your additional functions from another module or define them here
from utils import get_initial_message, update_chat, answer_query_with_context_pinecone

st.title("Chatbot : ChatGPT General Bot To Ask General Questions")
st.subheader("AI General Chatbot:")

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_area("Query: ", key="input")  # Changed st.text_input to st.text_area

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()
 
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        # response = answer_query_with_context_pinecone(query)
        response = get_chatgpt_response(query)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)
