#Import functions

from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_models import BedrockChat
from langchain.chains import ConversationChain
#import transformers

#function to invoke model
def get_llm():
    llm = BedrockChat(
        model_id="amazon.titan-text-express-v1", #set the foundation model
        model_kwargs= {                          #configure the properties for Titan
            "temperature": 1,  
            "topP": 0.5,
            "maxTokenCount": 100,
        }
            
    )
    return llm

#test the model
#    return llm.invoke(input_text)
#response = get_llm("Hello, which LLM model you are")
#print(response)

##Create a memory function for this chat session
def create_memory():
    llm=get_llm()
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=512) #Maintains a summary of previous messages
    return memory


##Create a chat client function
def get_chat_response(input_text, memory): 
    
    llm = get_llm()
    
    conversation_with_memory = ConversationChain(            #create a conversation chain
        llm = llm,                                           #using the Bedrock LLM
        memory = memory,                                     #with the summarization memory
        verbose = True                                       #print out some of the internal states of the chain while running
    )
    
    chat_response = conversation_with_memory.invoke(input = input_text) #pass the user message and summary to the model
    
    return chat_response['response']

