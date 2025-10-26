#Import functions

# Old import - BedrockChat deprecated in LangChain 1.0+
# from langchain_community.chat_models import BedrockChat
# Updated import for LangChain 1.0+
from langchain_aws import ChatBedrock
# Old import - deprecated in LangChain 1.0+
# from langchain.chains import ConversationChain
# Updated import for LangChain 1.0+ - ConversationChain not available in langchain_community.chains
# from langchain_community.chains import ConversationChain
# ConversationChain has been deprecated, we'll implement conversation logic manually

# Old memory imports - not available in LangChain 1.0+
#from langchain_community.memory import ConversationSummaryBufferMemory
#from langchain.memory.summary_buffer import ConversationSummaryBufferMemory

# Simple memory implementation for LangChain 1.0+
class SimpleConversationMemory:
    def __init__(self, max_token_limit=512):
        self.conversation_history = []
        self.max_token_limit = max_token_limit
    
    def save_context(self, inputs, outputs):
        """Save conversation context"""
        human_message = inputs.get("input", "")
        ai_message = outputs.get("output", "")
        
        self.conversation_history.append(f"Human: {human_message}")
        self.conversation_history.append(f"Assistant: {ai_message}")
        
        # Simple token limit management (approximate)
        while len(self.conversation_history) > 10:  # Keep last 10 exchanges
            self.conversation_history.pop(0)
    
    def load_memory_variables(self, inputs):
        """Load memory variables"""
        history = "\n".join(self.conversation_history)
        return {"history": history}
    
    def clear(self):
        """Clear conversation history"""
        self.conversation_history = []

#import transformers

#function to invoke model
def get_llm():
    # Old approach with BedrockChat (deprecated)
    # llm = BedrockChat(
    #     model_id="amazon.titan-text-express-v1", #set the foundation model
    #     model_kwargs= {                          #configure the properties for Titan
    #         "temperature": 1,  
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     }
    # )
    
    # Updated approach for LangChain 1.0+ using ChatBedrock
    # AUTHENTICATION METHODS:
    
    # Method 1: Default AWS credential chain (current approach)
    # Uses environment variables, AWS CLI config, or IAM roles
    
    # Option A: Use default credentials (current)
    llm = ChatBedrock(
        model_id="amazon.titan-text-express-v1", #set the foundation model
        model_kwargs= {                          #configure the properties for Titan
            "temperature": 1,  
            "topP": 0.5,
            "maxTokenCount": 100,
        },
        region_name="us-east-1"  # Add region (required for ChatBedrock)
    )
    
    # Option B: Use specific AWS profile (uncomment and replace 'your-profile-name')
    # import boto3
    # import os
    # 
    # # Set profile name - replace with your actual profile name
    # profile_name = os.getenv('AWS_PROFILE', 'your-profile-name')
    # session = boto3.Session(profile_name=profile_name)
    # 
    # llm = ChatBedrock(
    #     model_id="amazon.titan-text-express-v1",
    #     model_kwargs={
    #         "temperature": 1,
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     },
    #     client=session.client('bedrock-runtime', region_name='us-east-1')
    # )
    
    # Method 2: Explicit credentials (uncomment to use)
    # import boto3
    # session = boto3.Session(
    #     aws_access_key_id='YOUR_ACCESS_KEY',
    #     aws_secret_access_key='YOUR_SECRET_KEY',
    #     region_name='us-east-1'
    # )
    # llm = ChatBedrock(
    #     model_id="amazon.titan-text-express-v1",
    #     model_kwargs={
    #         "temperature": 1,
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     },
    #     client=session.client('bedrock-runtime')
    # )
    
    # Method 3: Using AWS profile (uncomment to use)
    # import boto3
    # session = boto3.Session(profile_name='your-profile-name')
    # llm = ChatBedrock(
    #     model_id="amazon.titan-text-express-v1",
    #     model_kwargs={
    #         "temperature": 1,
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     },
    #     client=session.client('bedrock-runtime')
    # )
    
    return llm

#test the model
#    return llm.invoke(input_text)
#response = get_llm("Hello, which LLM model you are")
#print(response)

##Create a memory function for this chat session
def create_memory():
    # Old approach with ConversationSummaryBufferMemory (commented out)
    # llm=get_llm()
    # memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=512) #Maintains a summary of previous messages
    # return memory
    
    # Updated approach for LangChain 1.0+ - Simple memory implementation
    memory = SimpleConversationMemory(max_token_limit=512) #Maintains conversation history
    return memory


##Create a chat client function
def get_chat_response(input_text, memory): 
    
    llm = get_llm()
    
    # Old approach using ConversationChain (deprecated in LangChain 1.0+)
    # conversation_with_memory = ConversationChain(            #create a conversation chain
    #     llm = llm,                                           #using the Bedrock LLM
    #     memory = memory,                                     #with the summarization memory
    #     verbose = True                                       #print out some of the internal states of the chain while running
    # )
    # chat_response = conversation_with_memory.invoke(input = input_text) #pass the user message and summary to the model
    # return chat_response['response']
    
    # Updated approach for LangChain 1.0+ - Manual conversation handling
    try:
        # Get conversation history from memory
        memory_variables = memory.load_memory_variables({})
        history = memory_variables.get('history', '')
        
        # Create prompt with conversation history
        if history:
            full_prompt = f"{history}\nHuman: {input_text}\nAssistant:"
        else:
            full_prompt = f"Human: {input_text}\nAssistant:"
        
        print(f"Prompt being sent to LLM: {full_prompt}")  # Debug output (verbose mode)
        
        # Get response from LLM
        response = llm.invoke(full_prompt)
        
        # Extract response content
        if hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = str(response)
        
        # Save conversation to memory
        memory.save_context(
            {"input": input_text}, 
            {"output": response_text}
        )
        
        return response_text
        
    except Exception as e:
        print(f"Error in get_chat_response: {e}")
        
        # Check for specific AWS authentication errors
        if "ExpiredTokenException" in str(e) or "ExpiredToken" in str(e):
            return "⚠️ AWS credentials have expired. Please run 'aws configure' or 'aws sso login' to refresh your credentials, then try again."
        
        if "UnauthorizedOperation" in str(e) or "AccessDenied" in str(e):
            return "⚠️ AWS access denied. Please check your AWS permissions for Bedrock access."
        
        if "ValidationException" in str(e) and "model" in str(e).lower():
            return "⚠️ Model access issue. Please ensure you have requested access to Amazon Titan models in the AWS Bedrock console."
        
        # Simple fallback without memory
        try:
            response = llm.invoke(f"Human: {input_text}\nAssistant:")
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            
            # More specific error messages for fallback
            if "ExpiredTokenException" in str(fallback_error):
                return "⚠️ AWS credentials expired. Please refresh your AWS credentials and try again."
            
            return "I'm sorry, I'm having trouble connecting to AWS Bedrock. Please check your AWS credentials and try again."

