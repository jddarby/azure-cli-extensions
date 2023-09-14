import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import asyncio
#NSD Copilot successfully implemented with the chat completion API
credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/",credential=credential)
ai_key = client.get_secret("AIKey1")

system_message = """
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

kernel = sk.Kernel()

kernel.add_chat_service(
    "chat-gpt",
    AzureChatCompletion("gpt35depl1", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
)

prompt_config = sk.PromptTemplateConfig.from_completion_parameters(
    max_tokens=400, temperature=0.5
)

prompt_template = sk.ChatPromptTemplate(
    "{{$user_input}}", kernel.prompt_template_engine, prompt_config
)

prompt_template.add_system_message(system_message)

function_config = sk.SemanticFunctionConfig(prompt_config, prompt_template)
chat_function = kernel.register_semantic_function("Chatbot", "Chat", function_config)

async def chat() -> bool:
    context_vars = sk.ContextVariables()

    try:
        user_input = input("User: ")
        context_vars["user_input"] = user_input
    except KeyboardInterrupt:
        print("\nExiting Chat...")
        return False
    except EOFError:
        print("\nExiting Chat...")
        return False
    
    response = await kernel.run_async(chat_function, input_vars=context_vars)
    print(f"Chatbot: {response}")
    return True

async def main() -> None:
    chatting = True
    while chatting:
        chatting = await chat()

if __name__ == "__main__":
    asyncio.run(main())