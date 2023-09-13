import asyncio
from typing import Tuple

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextCompletion
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/", credential=credential)
ai_key = client.get_secret("AIKey1")

#NSD Copilot has similar functionality being run with the completion API on semantic kernel.

async def completion_api(
        kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    """
    Create a semantic function whose prompt describes the parameters to be collected to build an NSD.
    
    Args:
        kernel: The instance of the semantic kernel.
    """
    #The prompt is an adapted version of the system message in a chat completion API.
    sk_prompt = """
    The system summarises the key properties of an NSD in the following format:
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
    ----
    RULES
    If you are asked information about the NSD or any of the parameters, only present information from this system message.
    Ask them about the properties of the network service design they would like to make.
    Extract the relevant information from the user response to fill out as many fields as you can.
    Don't autofill any fields unless you get the information from the user prompt.
    Display the information and ask if they want to update it. 
    Keep prompting the user with questions to fill out all of the categories.
    Do not ask them to give you information about all of the sections, prompt them to give you information about individual sections. 
    Allow the user to add more than one network function definition to the design.
    Don't ask for multiple fields in one question.
    Always display the summary in a JSON format as shown above.
    Don't ask for information again if you can already fill in a field from a user input.
    {{$chat_history}}
    User: {{$user_input}}
    ChatBot: 
    """
    #Create the semantic function  
    chat_func = kernel.create_semantic_function(
        sk_prompt, max_tokens=500, temperature=0.5
    )
    #Create the new context
    context = kernel.create_new_context()
    context["chat_history"] = ""
    return chat_func, context

async def chat(
        kernel: sk.Kernel, chat_func: sk.SKFunctionBase, context: sk.SKContext
) -> bool:
    """
    Interact with the user and call the semantic function to generate a response.

    Args:
        kernel: The instance of the semantic kernel with the completion service and semantic function loaded.
        chat_func: The semantic function to extract information from the user.
        context: Context (chat history) to help improve the LLMs performance.

    Returns:
        bool: If False, the conversation ends.
    """
    try:
        #Process user input and add to chat history context
        user_input = input("User: ")
        context["chat_history"] += f"\nUser: {user_input}"
    except KeyboardInterrupt:
        print("\n\nExiting Chat...")
        return False
    except EOFError:
        print("\n\nExiting Chat...")
        return False
    
    if user_input == "exit":
        print("\n\nExiting Chat...")
        return False
    #Run the semantic function with the chat history as context
    answer = await kernel.run_async(chat_func, input_vars=context.variables)
    #Add the system's response to the chat history and print it
    context["chat_history"] += f"\nChatBot: {answer}"
    print(f"ChatBot: {answer}")
    return True

async def main() -> None:
    """
    Instantiate the kernel, add appropriate services and begin a chat with the user.
    """
    kernel = sk.Kernel()
    #Older models like text-davinci-003 are compatible with completion services
    kernel.add_text_completion_service(
        "completion", AzureTextCompletion("text-davinci-003-aiops", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
    )
    #Load the semantic function and empty context to the instance of the kernel
    chat_func, context = await completion_api(kernel)
    #Begin chatting with the user
    print("Welcome to the NSD Generation Copilot! \n Please ensure you are connected to the appropriate VNET. \n Chat to the Copilot to tell it more about the NSD you want to build. \n Once you are happy with your design, enter 'build'.")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)

if __name__ == "__main__":
    asyncio.run(main())