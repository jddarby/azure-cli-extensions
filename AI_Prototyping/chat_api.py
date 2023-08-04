import tiktoken
import openai
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/",credential=credential)
key = client.get_secret("AIKey1")

openai.api_type = "azure"
openai.api_version = "2023-06-01-preview" 
openai.api_base = "https://azopenai-aiops.openai.azure.com/"
openai.api_key = key.value
#The basic function to create a response using the Chat Completion API can be found under the "Creating a Basic Conversation Loop" section in the following link:
#https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions

file_path = "/home/developer/repos/copilot/chat_completion/system_message.txt"
file = open(file_path, 'r')
conversation=[{"role": "system", "content": file.read()}]

max_response_tokens = 500
token_limit = 4096

def num_tokens_from_messages(messages):
    """Count the number of tokens being processed by the model using the BPE tokeniser for gpt-3.5-turbo.

    Args:
        messages (dictionary): Chat transcript including previous user inputs and system responses.

    Returns:
        num_tokens (integer): Number of tokens in the chat transcript.
    """
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    #https://github.com/openai/tiktoken/blob/main/README.md
    num_tokens = 0
    for message in messages:
        num_tokens += 4 #All messages have <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name": #The role assignment shouldn't be counted as a token.
                num_tokens += -1
            num_tokens += 2 #All reponses by the system have <im_start>assistant
            return num_tokens
#This function can be found in the "Managing Conversations" section of the following link:
#https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions#preventing-unsafe-user-inputs

print("Welcome to the NSD Generation Copilot! Chat to the Copilot to tell it more about the NSD you want to build. Once you are happy with your design, enter 'build'.")
while True:
    try:
        user_input = input()
        if user_input == "exit":
            print("Exiting Chat.")
            break    
        conversation.append({"role": "user", "content": user_input})
        conv_history_tokens = num_tokens_from_messages(conversation)
        while conv_history_tokens + max_response_tokens >= token_limit:
            del conversation[1]
            conv_history_tokens = num_tokens_from_messages(conversation)
        response = openai.ChatCompletion.create(
            engine="gpt35depl1", 
            messages = conversation,
            max_tokens=max_response_tokens,
            temperature=0
            )
        conversation.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
        print("\n" + response['choices'][0]['message']['content'] + "\n")
    except KeyboardInterrupt:
        print("Exiting Chat.")
        break 
    except openai.error.InvalidRequestError as e:
        if e.error.code == "content_filter" and e.error.innererror:
            content_filter_result = e.error.innererror.content_filter_result
            for category, details in content_filter_result.items():
                print(f"{category}:\n filtered={details['filtered']}\n severity={details['severity']}")
                print("Your prompt was filtered, please try to phrase your request more appropriately.")
    #This code can be found under the "Annotations Preview" section in the following document:
    #https://learn.microsoft.com/en-gb/azure/ai-services/openai/concepts/content-filter