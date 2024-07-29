# Python Design Pattern Learner

This Streamlit app helps users learn and practice design patterns in Python. The app generates coding problems based on a selected design patterns, difficulty level, and topic, and provides feedback to user-submitted solutions.

## Features

- Generate coding problems with Claude Sonnet 3.5 or Openai's gpt-4o
- Recieve a grade based on usage of best practices & correctness of your solution
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
