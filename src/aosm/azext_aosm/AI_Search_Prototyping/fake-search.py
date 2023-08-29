import asyncio
from typing import Tuple

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding, AzureTextCompletion
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/", credential=credential)
ai_key = client.get_secret("AIKey1")

async def fake_repo(kernel: sk.Kernel) -> None:
    await kernel.memory.save_information_async("fake-repo", id="nf1", text="https://hub.docker.com/_/nginx")
    await kernel.memory.save_information_async("fake-repo", id="nf2", text="https://hub.docker.com/_/haproxy")
    await kernel.memory.save_information_async("fake-repo", id="nf3", text="https://hub.docker.com/r/ubuntu/squid")
    await kernel.memory.save_information_async("fake-repo", id="nf4", text="https://hub.docker.com/_/traefik")
    await kernel.memory.save_information_async("fake-repo", id="nf5", text="https://hub.docker.com/_/consul")
    await kernel.memory.save_information_async("fake-repo", id="dummy", text="Dummy place filler")

async def examples(kernel) -> None:
    questions = [
        "What is nf1?"
        "What is nf2?"
        "What is nf3?"
        "What is nf4?"
        "What is nf5?"
        "What is dummy?"
    ]

    for question in questions:
        result = await kernel.memory.search_async("fake-repo", question)

async def completion_api(
        kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    sk_prompt = """
    The system can suggest the most appropriate network service design based on its memories of network functions is has access to.
    Do not suggest network functions outside of the ones stored in your volatile memory store.
    If more than one network function matches the needs of the user, the most appropriate one's name and description.
    It can say 'I don't know' if it doesn't have enough information to give an appropriate network function.
    
    Examples of network functions the system can recommend:
    - {{$fact1}} {{recall $fact1}}
    - {{$fact2}} {{recall $fact2}}
    - {{$fact3}} {{recall $fact3}}
    - {{$fact4}} {{recall $fact4}}
    - {{$fact5}} {{recall $fact5}}
    - {{$fact6}} {{recall $fact6}}
    
    Chat:
    {{$chat_history}}
    User: {{$user_input}}
    ChatBot: """.strip()

    chat_func = kernel.create_semantic_function(
        sk_prompt, max_tokens=400, temperature=0.8
    )

    context = kernel.create_new_context()
    context["fact1"] = "What is nf1?"
    context["fact2"] = "What is nf2?"
    context["fact3"] = "What is nf3?"
    context["fact4"] = "What is nf4?"
    context["fact5"] = "What is nf5?"
    context["fact6"] = "What is dummy?"

    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "fake-repo"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = 0.4
    #There is also a LIMIT_PARAM that controls the maximum number of memories the system can call at any given time.
    context["chat_history"] = ""

    return chat_func, context

async def chat(
        kernel: sk.Kernel, chat_func: sk.SKFunctionBase, context: sk.SKContext
) -> bool:
    try:
        user_input = input("User: ")
        context["user_input"] = user_input
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False
    
    if user_input == "exit":
        print("\n\nExiting chat...")
        return False
    
    answer = await kernel.run_async(chat_func, input_vars=context.variables)
    context["chat_history"] += f"\nUser: {user_input}\nChatBot: {answer}"
    print(f"ChatBot: {answer}")
    return True

async def main() -> None:
    kernel = sk.Kernel()
    kernel.add_text_completion_service(
        "completion", AzureTextCompletion("text-davinci-003-aiops", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
    )
    kernel.add_text_embedding_generation_service(
        "embedding", AzureTextEmbedding("text-embedding-ada-002", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
    )
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    kernel.import_skill(sk.core_skills.TextMemorySkill())
    
    await fake_repo(kernel)

    await examples(kernel)

    chat_func, context = await completion_api(kernel)

    print("Begin Chatting (type 'exit' to exit): \n")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)

if __name__ == "__main__":
    asyncio.run(main())