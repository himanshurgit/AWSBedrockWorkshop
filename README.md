# AWS Bedrock Chatbot

This project is part of the [AWS Bedrock Workshop (Build a Gen AI Chatbot) - Level 100](https://shorturl.at/uvmzn) course.

## Overview

A conversational AI chatbot built using AWS Bedrock and Streamlit. This application demonstrates how to create an interactive chat interface powered by Amazon's Titan foundation model, featuring conversation memory and a user-friendly web interface.

## Features

- **Conversational AI**: Powered by Amazon Titan Text Express v1 model
- **Memory Management**: Maintains conversation context using LangChain's ConversationSummaryBufferMemory
- **Interactive UI**: Clean, responsive Streamlit-based chat interface
- **Session Persistence**: Chat history preserved during the session
- **Real-time Responses**: Immediate AI responses with conversation flow

## Architecture

The application consists of two main components:

### Backend (`ChatBackend.py`)
- **Model Integration**: Configures and manages AWS Bedrock LLM connection
- **Memory System**: Implements conversation summarization with token limits
- **Response Generation**: Handles chat logic and response processing

### Frontend (`chatfrontend.py`)
- **User Interface**: Streamlit-based chat interface
- **Session Management**: Maintains chat history and memory state
- **Real-time Interaction**: Handles user input and displays responses

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials
- Required Python packages (see Installation)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install required dependencies:
   ```bash
   pip install streamlit langchain langchain-community boto3
   ```

3. Configure AWS credentials:
   ```bash
   aws configure
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run chatfrontend.py
   ```

2. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Start chatting with the AI assistant through the web interface

## Configuration

The chatbot is configured with the following default settings:
- **Model**: Amazon Titan Text Express v1
- **Temperature**: 1.0 (creative responses)
- **Top P**: 0.5 (focused sampling)
- **Max Tokens**: 100 per response
- **Memory Limit**: 512 tokens for conversation summary

These settings can be modified in the `get_llm()` function within `ChatBackend.py`.

## File Structure

```
├── ChatBackend.py      # Backend logic and AWS Bedrock integration
├── chatfrontend.py     # Streamlit frontend interface
└── README.md          # Project documentation
```

## Contributing

This project is part of an educational workshop. Feel free to experiment with different models, parameters, or UI improvements as part of your learning journey.

## License

This content is for public use as part of the AWS Bedrock Workshop educational materials.
