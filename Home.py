import streamlit as st
from streamlit_ace import st_ace
import anthropic
import openai
import time
from streamlit_extras.buy_me_a_coffee import button
from dotenv import load_dotenv
import os

from utils import check_code, check_syntax, generate_prompt


load_dotenv()

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "env_api_key" not in st.session_state:
    st.session_state.env_api_key = ""
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "Claude"
if "problem" not in st.session_state:
    st.session_state.problem = ""


def init_anthropic_client(api_key):
    st.session_state.client = anthropic.Anthropic(api_key=api_key)
    st.session_state.client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hello"}],
    )
    st.sidebar.success(
        f"API connection successful with {st.session_state.model_choice}!"
    )


def init_openai_client(api_key):
    st.session_state.client = openai.OpenAI(api_key=api_key)
    st.session_state.client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
    )
    st.sidebar.success(
        f"API connection successful with model {st.session_state.model_choice}!"
    )


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


st.set_page_config(page_title="Design Pattern Trainer", page_icon="🐍", layout="wide")

st.title("🐍 Practice Design Patterns")

st.sidebar.title("API Configuration")

st.session_state.api_key = st.sidebar.text_input(
    "Enter your API key",
    type="password",
    key="api_key_input",
)


model_choice = st.sidebar.radio(
    "Choose AI model",
    ["Claude", "ChatGPT"],
)
st.session_state.model_choice = model_choice

if st.session_state.model_choice == "Claude":
    st.session_state.env_api_key = os.getenv("ANTHROPIC_API_KEY")
elif st.session_state.model_choice == "ChatGPT":
    st.session_state.env_api_key = os.getenv("OPENAI_API_KEY")

if st.session_state.env_api_key:
    st.sidebar.success(f"API key loaded from .env file!")

if st.sidebar.button("Submit API Key"):
    # Ask for forgiveness, not for permission
    if st.session_state.model_choice == "Claude":
        try:
            init_anthropic_client(st.session_state.api_key)
        except Exception:
            try:
                init_anthropic_client(st.session_state.env_api_key)
            except Exception as e:
                st.sidebar.error(f"""API connection failed. Please check your
                key and try again.\n\n\nMessage from API provider: {str(e)}""")
    else:
        try:
            init_openai_client(st.session_state.api_key)
        except Exception:
            try:
                init_openai_client(st.session_state.env_api_key)
            except Exception as e:
                st.sidebar.error(f"""API connection failed. Please check your
                key and try again.\n\n\nMessage from API provider: {str(e)}""")


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

# UI Terminal
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
