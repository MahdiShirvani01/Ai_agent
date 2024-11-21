import streamlit as st
import llm
import generate_output, page_movement
import os


# title
page_icon = ":book:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
page_title = "AI Agent to generate stories for children"
layout = 'wide'

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + page_icon)

if 'page' not in st.session_state:
    st.session_state.page = 1

if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# page 1, enter your api key
if st.session_state.page == 1:

    api_key = st.text_input("Enter your Groq api key:", type="password")
    
    if api_key and len(api_key) == 56:
        st.session_state.api_key = api_key

    # goint to next page
    if st.button("Next", use_container_width=True):
        if st.session_state.api_key:
            os.environ["GROQ_API_KEY"] = st.session_state.api_key
            page_movement.go_to_page(2) 
        else:
            st.warning("Please enter your correct API key before anything !")


# page 2, enter your topic and wait for generation
elif st.session_state.page == 2 and st.session_state.api_key != None:
    
    st.write(f"Your API Key: `{st.session_state.api_key}`")

    # choosing your topic
    topic = st.text_input('Enter topic', placeholder='star war')

    # books context and donload link
    if st.button("Get your book", use_container_width=True):
        with st.spinner('Generating ...'):
            result = llm.llm_setup(st.session_state.api_key, topic=topic)
            st.markdown(result)
            docx_file = generate_output.generate_docx(result)
            docx_download_link = generate_output.download_docx(docx_file, f"{topic} ebook.docx")
            st.markdown(docx_download_link, unsafe_allow_html=True)

    # back to api key page
    if st.button("back", use_container_width= True):
        st.session_state.api_key = None
        page_movement.go_to_page(1)
