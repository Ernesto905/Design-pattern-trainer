# Python Design Pattern Learner

This is a Streamlit application that helps users learn and practice Python design patterns. The app generates coding problems based on selected design patterns, difficulty levels, and topics, and provides feedback on user-submitted solutions.

## Features

- Choose from various design patterns, difficulty levels, and topics
- Generate coding problems using AI (Claude or ChatGPT)
- Write and submit code solutions
- Receive AI-powered feedback on your implementation
- Syntax checking for submitted code
- Option to use Vim keybindings in the code editor

## Deployment

The site is [deployed](https://designpatterns.streamlit.app/) and ready to use. 

## Running Locally

If you want to run the application locally:

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Run the Streamlit app:
   ```
   streamlit run Home.py
   ```

## Feedback

I appreciate your feedback! Please use the feedback button in the app to share your thoughts and suggestions.
