#!/bin/bash

# Setup script for AWS Bedrock Chatbot

echo "Setting up AWS Bedrock Chatbot environment..."

# Create virtual environment
python -m venv bedrock-chatbot-env

# Activate virtual environment
source bedrock-chatbot-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Setup complete! To activate the environment, run:"
echo "source bedrock-chatbot-env/bin/activate"
echo ""
echo "To run the chatbot:"
echo "streamlit run chatfrontend.py"