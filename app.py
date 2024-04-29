import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()
import os

## Load the Groq API key
groq_api_key = os.getenv('GROQ_API_KEY')
# Funciton to get respone from LLAma 2 model

def getLLamaresponse(input_text, no_words, blog_style, creativity):
    # calling llama 3 -8b model with groq
    llm = ChatGroq(temperature=creativity,model="llama3-8b-8192",groq_api_key=groq_api_key)

    # llm = CTransformers(model ="models\llama-2-7b-chat.ggmlv3.q8_0.bin",
    #                     model_type = 'llama',
    #                     config ={'max_new_tokens' :256,
    #                              'temperature' : 0.01})
    # template = """
    # Write a blog for {blog_style} profile for a topic {input_text}
    # within {no_words} words.
    # """
    # prompt = PromptTemplate(input_variables=['blog_style','input_text','no_words'],
    #                         template=template)
    prompt = ChatPromptTemplate.from_template("""
    Write a blog as {blog_style} on a topic {input_text}
    within {no_words} words.
    """)
    # generate the response from llama 2 model
    chain = prompt | llm
    response = chain.invoke({"input_text":input_text, "no_words":no_words, "blog_style":blog_style })
    # response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    print(response.content)
    return response


st.set_page_config(page_title='Generate your choice of Blogs',
                   layout = 'centered',
                   initial_sidebar_state='collapsed')

st.header("Generate your choice of Blogs")

input_text = st.text_input("Enter the Blog Topic")
col1, col2, col3 = st.columns([3,3,3])
with col1:
    no_words = st.text_input("No of Words")
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researcher','Data Scientists','General people','Ocean Vuong','Hank Moody','Chuck Palahniuk'),index=0)
with col3:
    creativity = st.text_input("Level of creativity [scale : 0-1]")

submit = st.button('Generate')

# Final Response

if submit:
    response = getLLamaresponse(input_text, no_words, blog_style, creativity)
    st.write(response.content)



