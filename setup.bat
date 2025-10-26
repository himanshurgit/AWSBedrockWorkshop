@echo off
REM Setup script for AWS Bedrock Chatbot (Windows)

echo Setting up AWS Bedrock Chatbot environment...

REM Create virtual environment
python -m venv bedrock-chatbot-env

REM Activate virtual environment
call bedrock-chatbot-env\Scripts\activate.bat

REM Upgrade pip
pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

echo.
echo Setup complete! To activate the environment, run:
echo bedrock-chatbot-env\Scripts\activate.bat
echo.
echo To run the chatbot:
echo streamlit run chatfrontend.py

pause