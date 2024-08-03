import streamlit as st 
import ast

# -----------------------------------
# Helper functions
# -----------------------------------
def check_syntax(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def check_code(pattern, code, problem):
    system_prompt = (
        "You are an expert Python developer specializing in design patterns."
    )

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


