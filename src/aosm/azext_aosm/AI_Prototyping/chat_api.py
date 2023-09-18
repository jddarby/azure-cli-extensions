import json
import os
import tiktoken
import openai
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#NSD Copilot - open API call to the chat completion service

#TO DO: change the keyvault and endpoint to the new subscription's AI instance
credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/",credential=credential)
key = client.get_secret("AIKey1")

#Preview API can display content filter messages
openai.api_type = "azure"
openai.api_version = "2023-06-01-preview" 
openai.api_base = "https://azopenai-aiops.openai.azure.com/"
openai.api_key = key.value

#System message specifies how the LLM should behave
message = """
Engage in a conversation with the user to obtain relevant information to form a summary of the properties of a network service design.
----
RULES
If you are asked information about the NSD or any of the parameters, only present information from this system message.
Ask them about the properties of the network service design they would like to make.
Extract the relevant information from the user response to fill out as many fields as you can.
Don't autofill any fields unless you get the information from the user prompt.
Display the information and ask if they want to update it. 
{
    "location": "Offering location of the network service design.",
    "publisher_name": "Name of the Publisher resource you want your design published to.",
    "publisher_resource_group_name": "Resource group for the Publisher resource.",
    "acr_artifact_store_name": "Name of the ACR Artifact Store resource. Will be created if it does not exist.",
    "network_functions": [
        {
            "name": "Existing Network Function Definition Group Name.",
            "version": "Existing Network Function Definition Version Name",
            "publisher_offering_location": "Offering location of the publisher of the Network Function Definition",
            "type": "Type of nf in the definition. Valid values are 'cnf' or 'vnf'",
            "multiple_instances": "Whether or not the Network Function Definition will appear more than once in the Network Service Design. Valid values are true or false.",
            "publisher": "Name of the publisher the network function was made under.",
            "publisher_resource_group": "Name of the resource group for the publisher of the network function."
        }
    ],
    "nsdg_name": "Network Service Design Group Name. This is the collection of Network Service Design Versions. Will be created if it does not exist.",
    "nsd_version": "Version of the NSD to be created. This should be in the format A.B.C",
    "nsdv_description": "Description of the NSDV."
}
Keep prompting the user with questions to fill out all of the categories.
Do not ask them to give you information about all of the sections, prompt them to give you information about individual sections. 
Allow the user to add more than one network function definition to the design.
Don't ask for multiple fields in one question.
Always display the summary in a JSON format as shown above.
Don't ask for information again if you can already fill in a field from a user input.
"""
conversation=[{"role": "system", "content": message}]
max_response_tokens = 500
token_limit = 4096

def num_tokens_from_messages(messages):
    """
    Count the number of tokens being processed by the model using the BPE tokeniser for gpt-3.5-turbo.
    https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions#preventing-unsafe-user-inputs

    Args:
        messages (dictionary): Chat transcript including previous user inputs and system responses.

    Returns:
        num_tokens (integer): Number of tokens in the chat transcript.
    """
    #https://github.com/openai/tiktoken/blob/main/README.md
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = 0
    for message in messages:
        num_tokens += 4 #All messages have <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name": #The role assignment shouldn't be counted as a token
                num_tokens += -1
            num_tokens += 2 #All reponses by the system have <im_start>assistant
            return num_tokens

def ai_assistance():
    """
    Outputs an NSD configuration based on user inputs using a chat completion service and gpt-3.5-turbo.

    Returns:
        config (file): A configuration for an NSD.
    """
    print("Welcome to the NSD Generation Copilot!\n Chat to the Copilot to tell it more about the NSD you want to build. \n Once you are happy with your design, ask the copilot to display the information it has and then enter 'build'.")
    while True:
        try:
            #Process user input
            user_input = input("User: ")
            if user_input == "build":
                #Read last assistant message
                print("Thank you! I am now building the NSD based on the information you have given.")
                text = response["choices"][0]["message"]["content"]
                #Identify JSON section
                begin = text.find("{")
                end = text.rfind("}")
                string = text[begin:end+1]
                #Write to a separate file
                nsd = json.loads(string)
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, "input.json")
                with open(file_path, "w", encoding="utf-8") as json_file:
                    json.dump(nsd, json_file, indent=4, ensure_ascii=False)
                return file_path
                break
            #Add the user message to chat transcript
            conversation.append({"role": "user", "content": user_input})
            #Find the number of tokens to be fed into the next request to the LLM
            conv_history_tokens = num_tokens_from_messages(conversation)
            #Assume the LLM responds with the maximum number of tokens and delete the oldest message in the transcript if it exceeds the limit
            while conv_history_tokens + max_response_tokens >= token_limit:
                del conversation[1]
                conv_history_tokens = num_tokens_from_messages(conversation)
            #Call the chat completion service with the gpt-3.5-turbo model to generate a response
            response = openai.ChatCompletion.create(
                engine="gpt35depl1", 
                messages = conversation,
                max_tokens=max_response_tokens,
                temperature=0.5
                )
            #Add assistant's response to the chat transcript and print it out
            conversation.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
            print("\n" + "ChatBot: " + response['choices'][0]['message']['content'] + "\n")
        #Display filter categories and severity if triggered
        except openai.error.InvalidRequestError as e:
            if e.error.code == "content_filter" and e.error.innererror:
                content_filter_result = e.error.innererror.content_filter_result
                for category, details in content_filter_result.items():
                    print(f"{category}:\n filtered={details['filtered']}\n severity={details['severity']}")
                print("Your prompt was filtered, please try to phrase your request more appropriately.")
        #https://learn.microsoft.com/en-gb/azure/ai-services/openai/concepts/content-filter