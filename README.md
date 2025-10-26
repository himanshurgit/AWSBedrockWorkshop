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

## AWS Authentication Setup

The application uses AWS Bedrock, so you need to configure AWS credentials. **AWS SSO is the recommended method** for secure authentication.

### Method 1: AWS SSO Configuration (Recommended)

AWS Single Sign-On (SSO) provides secure, temporary credentials and is the preferred authentication method.

#### Step 1: Configure AWS SSO
```bash
aws configure sso
```

You'll be prompted to enter:
- **SSO session name**: `bedrock-session` (or any name you prefer)
- **SSO start URL**: Your organization's SSO URL (e.g., `https://your-org.awsapps.com/start`)
- **SSO region**: The region where your SSO is configured (e.g., `us-east-1`)
- **SSO registration scopes**: Press Enter for default (`sso:account:access`)

#### Step 2: Complete SSO Setup
The CLI will open your browser to complete authentication. After successful login:
- **Account ID**: Select your AWS account
- **Role name**: Choose the appropriate role (e.g., `PowerUserAccess`, `AdministratorAccess`)
- **Default region**: `us-east-1` (or your preferred region)
- **Output format**: `json`

#### Step 3: Login with SSO
```bash
aws sso login --profile default
```

Or if you created a named profile:
```bash
aws sso login --profile your-profile-name
```

#### Step 4: Set Default Profile (Optional)
To make your SSO profile the default:
```bash
export AWS_PROFILE=your-profile-name
```

Make it permanent by adding to your shell profile:
```bash
# For zsh (macOS default)
echo 'export AWS_PROFILE=your-profile-name' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export AWS_PROFILE=your-profile-name' >> ~/.bashrc
source ~/.bashrc
```

#### Step 5: Verify SSO Authentication
```bash
aws sts get-caller-identity
```

### Method 2: AWS CLI Configuration (Alternative)
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region (e.g., us-east-1)
- Output format (json)

### Method 3: Environment Variables (Development Only)
```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1
```

### Refreshing Expired SSO Credentials

If you see "ExpiredTokenException" errors, refresh your SSO login:
```bash
aws sso login
```

SSO tokens typically expire after 1-8 hours depending on your organization's settings.

### Required AWS Permissions
Your AWS role/user needs these permissions:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- `bedrock:GetFoundationModel` (optional, for model information)

### Bedrock Model Access
**Good news!** AWS Bedrock models are now **enabled by default** for all AWS accounts. You no longer need to request access to foundation models like Amazon Titan.

Simply ensure your AWS role/user has the required permissions listed above to invoke the models.

### Troubleshooting Authentication

**Common Issues:**

- **ExpiredTokenException**: Run `aws sso login` to refresh credentials
- **AccessDenied**: Check your IAM role has Bedrock permissions
- **ValidationException**: Ensure model access is granted in Bedrock console
- **Region errors**: Verify Bedrock is available in your selected region

**Check your current authentication:**
```bash
aws sts get-caller-identity
aws bedrock list-foundation-models --region us-east-1
```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Option A: Install using requirements file (Recommended)**
   ```bash
   pip install -r requirements.txt
   ```

   **Option B: Use the automated setup script**
   
   **For macOS/Linux:**
   ```bash
   ./setup.sh
   ```
   
   **For Windows:**
   ```cmd
   setup.bat
   ```

3. **Create and activate virtual environment (Manual setup)**
   
   **For macOS/Linux:**
   ```bash
   python -m venv bedrock-chatbot-env
   source bedrock-chatbot-env/bin/activate
   pip install -r requirements.txt
   ```
   
   **For Windows:**
   ```cmd
   python -m venv bedrock-chatbot-env
   bedrock-chatbot-env\Scripts\activate.bat
   pip install -r requirements.txt
   ```

4. Configure AWS credentials (see AWS Authentication Setup section above)

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
├── chatbackend.py      # Backend logic and AWS Bedrock integration
├── chatfrontend.py     # Streamlit frontend interface
├── requirements.txt    # Python dependencies (cross-platform)
├── setup.sh           # Automated setup script (macOS/Linux)
├── setup.bat          # Automated setup script (Windows)
└── README.md          # Project documentation
```

## Changelog

### Latest Updates (26-Oct-2025)

**🚀 Major Updates for LangChain 1.0+ Compatibility**

- **Updated LangChain Integration**: Migrated from deprecated modules to latest LangChain 1.0+ compatible imports
  - Replaced `langchain_community.chat_models.BedrockChat` with `langchain_aws.ChatBedrock`
  - Implemented custom memory management replacing deprecated `ConversationSummaryBufferMemory`
  - Removed dependency on deprecated `langchain.chains.ConversationChain`

- **Enhanced AWS Authentication**: 
  - Added comprehensive AWS SSO setup guide (now recommended method)
  - Improved error handling for expired tokens and authentication issues
  - Added multiple authentication method examples in code

- **Bedrock Model Access Simplified**: 
  - Updated documentation to reflect that Bedrock models are now enabled by default
  - Removed outdated model access request procedures

- **Dependencies Updated**: 
  - Added `langchain-aws==0.1.17` for latest Bedrock integration
  - Updated all LangChain ecosystem packages to latest versions
  - Complete `requirements.txt` with pinned versions for reproducible builds

- **Improved Setup Process**:
  - Added automated setup scripts for both macOS/Linux (`setup.sh`) and Windows (`setup.bat`)
  - Cross-platform installation instructions with manual and automated options
  - Enhanced installation instructions with multiple options
  - Better error messages and troubleshooting guidance

- **Code Modernization**:
  - Implemented backward compatibility with commented legacy code
  - Added comprehensive error handling for common AWS issues
  - Improved conversation memory management with custom implementation

## Contributing

This project is part of an educational workshop. Feel free to experiment with different models, parameters, or UI improvements as part of your learning journey.

## License

This content is for public use as part of the AWS Bedrock Workshop educational materials.
