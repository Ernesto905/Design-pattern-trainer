import streamlit as st
from streamlit_ace import st_ace
import anthropic
import openai
import time
from streamlit_extras.buy_me_a_coffee import button
from dotenv import load_dotenv
import os

import ast

load_dotenv()

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "Claude"
if "problem" not in st.session_state:
    st.session_state.problem = ""

def init_anthropic_client(api_key):
    return anthropic.Anthropic(api_key=api_key)

def init_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)


def check_syntax(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

patterns = {
    "Singleton": {
        "description": "Ensures a class has only one instance and provides a global point of access to it.",
        "url": "https://refactoring.guru/design-patterns/singleton/python/example",
    },
    "Factory": {
        "description": "Provides an interface for creating objects in a superclass, allowing subclasses to alter the type of objects that will be created.",
        "url": "https://refactoring.guru/design-patterns/factory-method/python/example",
    },
    "Observer": {
        "description": "Defines a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.",
        "url": "https://refactoring.guru/design-patterns/observer/python/example",
    },
    "Decorator": {
        "description": "Allows behavior to be added to an individual object, either statically or dynamically, without affecting the behavior of other objects from the same class.",
        "url": "https://refactoring.guru/design-patterns/decorator/python/example",
    },
    "Strategy": {
        "description": "Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.",
        "url": "https://refactoring.guru/design-patterns/strategy/python/example",
    },
}

topics = [
    "Animal related",
    "Workout related",
    "Tech related",
    "Biology related",
    "Business related",
]
difficulties = ["Very Easy", "Easy", "Medium", "Hard", "Grey Beard"]

def generate_prompt(pattern, difficulty, topic):
    if st.session_state.model_choice == "Claude":
        message = st.session_state.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            temperature=0.7,
            system="You are an expert Python developer specializing in design patterns.",
            messages=[
                {
                    "role": "user",
                    "content": f"""Generate a Python coding prompt for implementing the {pattern} design pattern.
            The difficulty level should be {difficulty}.
            The context or theme of the problem should be related to {topic}.
            Provide a clear problem statement and any specific requirements.

            Format the response as follows:
            Problem: [Problem statement]
            Requirements:
            - [Requirement 1]
            - [Requirement 2]
            - ...""",
                }
            ],
        )
        return message.content[0].text
    else:
        response = st.session_state.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer specializing in design patterns.",
                },
                {
                    "role": "user",
                    "content": f"""Generate a Python coding prompt for implementing the {pattern} design pattern.
                The difficulty level should be {difficulty}.
                The context or theme of the problem should be related to {topic}.
                Provide a clear problem statement and any specific requirements.

                Format the response as follows:
                Problem: [Problem statement]
                Requirements:
                - [Requirement 1]
                - [Requirement 2]
                - ...""",
                },
            ],
        )
        return response.choices[0].message.content

def check_code(pattern, code, problem):
    system_prompt = "You are an expert Python developer specializing in design patterns."

    human_prompt = f"""Analyze the following code and determine if it correctly implements the {pattern} design pattern and solves the given problem.
    Rate the implementation on a scale of 1-5, where 1 is completely incorrect and 5 is excellent.
    Provide brief suggestions for improvement if necessary.
    You will be very critical but fair, and precise in your scoring. Everything
    should be in python.

    Problem:
    {problem}

    Code:
    {code}

    Please format your response as follows:
    Score: [1-5]
    Suggestions: [Your suggestions here]
    """

    if st.session_state.model_choice == "Claude":
        response = st.session_state.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": human_prompt,
                }
            ],
        )
        return response.content[0].text
    else:
        response = st.session_state.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Python developer."},
                {"role": "user", "content": human_prompt},
            ],
        )
        return response.choices[0].message.content

st.set_page_config(page_title="Design Pattern Learner", page_icon="🐍", layout="wide")

st.title("🐍 Python Design Pattern Learner")

# Sidebar for API key input and model selection
st.sidebar.title("API Configuration")

# API Key input
api_key = st.sidebar.text_input(
    "Enter your API key",
    type="password",
    value=st.session_state.api_key,
    key="api_key_input",
)

# Check for API key in .env file
env_api_key = os.getenv("ANTHROPIC_API_KEY" if st.session_state.model_choice == "Claude" else "OPENAI_API_KEY")

if not api_key and env_api_key:
    api_key = env_api_key
    st.sidebar.success("API key loaded from .env file!")

if api_key:
    st.session_state.api_key = api_key

# Model choice
model_choice = st.sidebar.radio(
    "Choose AI model",
    ["Claude", "ChatGPT"],
)
st.session_state.model_choice = model_choice

# Initialize client based on model choice and API key
if st.session_state.api_key:
    if st.session_state.model_choice == "Claude":
        st.session_state.client = init_anthropic_client(st.session_state.api_key)
    else:
        st.session_state.client = init_openai_client(st.session_state.api_key)
    
    if st.sidebar.button("Test API Key"):
        try:
            if st.session_state.model_choice == "Claude":
                st.session_state.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=10,
                    messages=[{"role": "user", "content": "Hello"}],
                )
            else:
                st.session_state.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": "Hello"}],
                )
            st.sidebar.success("API connection successful!")
        except Exception as e:
            st.sidebar.error(f"API connection failed: {str(e)}")

col1, col2, col3 = st.columns(3)
with col1:
    selected_pattern = st.selectbox("Choose a Design Pattern", list(patterns.keys()))
with col2:
    selected_difficulty = st.selectbox("Choose Difficulty", difficulties)
with col3:
    selected_topic = st.selectbox("Choose Topic", topics)

st.header(selected_pattern)
st.write(patterns[selected_pattern]["description"])
st.markdown(f"[Learn more]({patterns[selected_pattern]['url']})")

if st.button("Generate New Problem"):
    if "client" in st.session_state:
        with st.spinner("Generating problem..."):
            st.session_state.problem = generate_prompt(
                selected_pattern, selected_difficulty, selected_topic
            )
    else:
        st.error("Please enter a valid API key to generate a problem.")

if st.session_state.problem:
    st.subheader("Problem")
    st.write(st.session_state.problem)

use_vim = st.checkbox("Use Vim keybindings")

# Code input using streamlit-ace
user_code = st_ace(
    placeholder="Enter your Python code here",
    language="python",
    theme="monokai",
    keybinding="vim" if use_vim else "vscode",
    font_size=14,
    tab_size=4,
    show_gutter=True,
    show_print_margin=False,
    wrap=False,
    auto_update=True,
    readonly=False,
    min_lines=20,
    key="ace_editor",
)

if st.button("Check Code"):
    if "client" in st.session_state:
        if user_code and st.session_state.problem:
            # First, check the syntax
            syntax_valid, syntax_error = check_syntax(user_code)
            
            if syntax_valid:
                with st.spinner("Analyzing your code..."):
                    time.sleep(2)  # Simulate loading
                    result = check_code(
                        selected_pattern, user_code, st.session_state.problem
                    )

                st.subheader("Analysis Result")
                st.markdown(result)
            else:
                st.error(f"Syntax Error: {syntax_error}")
                st.warning("Please fix the syntax errors before submitting for review.")
        else:
            st.warning("Please generate a problem and enter some code before checking.")
    else:
        st.error("Please enter a valid API key to check your code.")

button(username="ernesto9066", floating=True, width=221)

# Google Form URL
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdBn5MA6DCsaib4npqRUCqpR0CRKY_9cnZK7Nngusp_9k9sVg/viewform?usp=sf_link"

st.link_button("Feedback", form_url)

st.markdown(
    """
<style>
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        background-color: #f0f0f0;
    }
</style>
""",
    unsafe_allow_html=True,
)
