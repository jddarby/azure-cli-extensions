import asyncio
from typing import Tuple

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding, AzureTextCompletion
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/", credential=credential)
ai_key = client.get_secret("AIKey1")

async def nf_repo(kernel: sk.Kernel) -> None:
    await kernel.memory.save_information_async("nf-repo", id="nginx", text="Nginx is an open source reverse proxy server for HTTP, HTTPS, SMTP, POP3, IMAP protocols as well as a load balancer, HTTP cache and a web server (origin server). For more, see: https://hub.docker.com/_/nginx")
    await kernel.memory.save_information_async("nf-repo", id="apache_http", text="https://en.wikipedia.org/wiki/Apache_HTTP_Server")
    await kernel.memory.save_information_async("nf-repo", id="haproxy", text="HAProxy is a free, open source high availability solution, providing load balancing and proxying for TCP and HTTP-based applications by spreading requests across multiple servers. It is written in C and has a reputation for being fast and efficient (in terms of processor and memory usage). For more information, see: https://hub.docker.com/_/haproxy")
    await kernel.memory.save_information_async("nf-repo", id="squid", text="Squid is a caching proxy for the Web supporting HTTP, HTTPS, FTP, and more. It reduces bandwidth and improves response time by caching and reusing frequently-requested web pages. Squid has extensive access controls and makes a great server accelerator. It runs on most available operating systems, including Windows and is licensed under the GNU GPL. For more information, see: https://hub.docker.com/r/ubuntu/squid")
    await kernel.memory.save_information_async("nf-repo", id="traefik", text="Traefik is a modern reverse proxy and load balancer that makes deploying microservices easy. For more information, see: https://hub.docker.com/_/traefik")
    await kernel.memory.save_information_async("nf-repo", id="consul", text="Consul is a distributed, highly-available, and multi-datacenter aware tool for service discovery, configuration, and orchestration. Consul enables rapid deployment, configuration, and maintenance of service-oriented architectures at massive scale. For more informaiton, see: https://hub.docker.com/_/consul")
    await kernel.memory.save_information_async("nf-repo", id="sas", text="Microsoft Internal network function. For more information, follow the link: https://dev.azure.com/msazuredev/AzureForOperators/_git/afosas-aosm-nfd")

#Nginx, HAProxy, Squid, Traefik, Consul information is taken from the appropriate sections on Docker Hub
#Apache HTTP information is taken from wikipedia
#SAS information is still being worked on

async def examples(kernel) -> None:
    questions = [
        "What is nginx?"
        "What is apache?"
        "What is HAProxy?"
        "What is squid?"
        "What is traefik?"
        "What is consul?"
        "What is SAS?"
    ]

    for question in questions:
        result = await kernel.memory.search_async("nf-repo", question)

async def completion_api(
        kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    sk_prompt = """
    The system can suggest the most appropriate network service design based on its memories of network functions is has access to.
    Do not suggest network functions outside of the ones stored in your volatile memory store.
    Do not make up information if it doesn't already exist.
    If more than one network function matches the needs of the user, the most appropriate one's name and description.
    It can say 'I don't know' if it doesn't have enough information to give an appropriate network function.
    
    Examples of network functions the system can recommend:
    - {{$fact1}} {{recall $fact1}}
    - {{$fact2}} {{recall $fact2}}
    - {{$fact3}} {{recall $fact3}}
    - {{$fact4}} {{recall $fact4}}
    - {{$fact5}} {{recall $fact5}}
    - {{$fact6}} {{recall $fact6}}
    - {{$fact7}} {{recall $fact7}}
    
    Chat:
    {{$chat_history}}
    User: {{$user_input}}
    ChatBot: """.strip()

    chat_func = kernel.create_semantic_function(
        sk_prompt, max_tokens=400, temperature=0.8
    )

    context = kernel.create_new_context()
    context["fact1"] = "What is nginx?"
    context["fact2"] = "What is apache?"
    context["fact3"] = "What is HAProxy?"
    context["fact4"] = "What is squid?"
    context["fact5"] = "What is traefik?"
    context["fact6"] = "What is consul?"
    context["fact7"] = "What is SAS?"

    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "nf-repo"
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
    await nf_repo(kernel)

    await examples(kernel)

    chat_func, context = await completion_api(kernel)

    print("Begin Chatting (type 'exit' to exit): \n")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)

if __name__ == "__main__":
    asyncio.run(main())