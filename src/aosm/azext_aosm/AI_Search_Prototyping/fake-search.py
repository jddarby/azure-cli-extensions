import asyncio
from typing import Tuple

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding, AzureTextCompletion, AzureChatCompletion
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/", credential=credential)
ai_key = client.get_secret("AIKey1")

async def fake_repo(kernel: sk.Kernel) -> None:
    await kernel.memory.save_information_async("fake-repo", id="nf1", text="""
nf1 is a powerful network function that has the following features:
Ability to handle more than 10,000 simultaneous connections with a low memory footprint (~2.5 MB per 10k inactive HTTP keep-alive connections). 
Handling of static files, index files and auto-indexing
Reverse proxy with caching
Load balancing[26] with in-band health checks
TLS/SSL with SNI and OCSP stapling support, via OpenSSL
FastCGI, SCGI, uWSGI support with caching
gRPC support since March 2018, version 1.13.10.
Name- and IP address-based virtual servers
IPv6-compatible
WebSockets since 1.3.13, including acting as a reverse proxy and do load balancing of WebSocket applications.
HTTP/1.1 Upgrade (101 Switching Protocols)
HTTP/2 protocol support
HTTP/3 protocol support (experimental since 1.25.0)
URL rewriting and redirection
TLS/SSL support
STARTTLS support
SMTP, POP3, and IMAP proxy
Requires authentication using an external HTTP server or by an authentication script
Other features include upgrading executable and configuration without client connections loss, and a module-based architecture with both core and third-party module support.""")
    await kernel.memory.save_information_async("fake-repo", id="nf2", text="""
nf2 is a powerful network function that supports a variety of features, many implemented as compiled modules which extend the core functionality. These can range from authentication schemes to supporting server-side programming languages such as Perl, Python, Tcl and PHP. Popular authentication modules include mod_access, mod_auth, mod_digest, and mod_auth_digest, the successor to mod_digest. A sample of other features include Secure Sockets Layer and Transport Layer Security support (mod_ssl), a proxy module (mod_proxy), a URL rewriting module (mod_rewrite), custom log files (mod_log_config), and filtering support (mod_include and mod_ext_filter).
Popular compression methods on nf2 include the external extension module, mod_gzip, implemented to help with reduction of the size (weight) of web pages served over HTTP. ModSecurity is an open source intrusion detection and prevention engine for Web applications. nf2 logs can be analyzed through a Web browser using free scripts, such as AWStats/W3Perl or Visitors.
Virtual hosting allows one nf2 installation to serve many different websites. For example, one computer with one nf2 installation could simultaneously serve example.com, example.org, test47.test-server.example.edu, etc.
nf2 features configurable error messages, DBMS-based authentication databases, content negotiation and supports several graphical user interfaces (GUIs).
It supports password authentication and digital certificate authentication. Because the source code is freely available, anyone can adapt the server for specific needs, and there is a large public library of nf2 add-ons.
A more detailed list of features is provided below:
Loadable Dynamic Modules
Multiple Request Processing modes (MPMs) including Event-based/Async, Threaded and Prefork.
Highly scalable (easily handles more than 10,000 simultaneous connections)
Handling of static files, index files, auto-indexing and content negotiation
.htaccess per-directory configuration support
Reverse proxy with caching
Load balancing with in-band health checks
Multiple load balancing mechanisms
Fault tolerance and Failover with automatic recovery
WebSocket, FastCGI, SCGI, AJP and uWSGI support with caching
Dynamic configuration
TLS/SSL with SNI and OCSP stapling support, via OpenSSL or wolfSSL.
Name- and IP address-based virtual servers
IPv6-compatible
HTTP/2 support
Fine-grained authentication and authorization access control
gzip compression and decompression
URL rewriting
Headers and content rewriting
Custom logging with rotation
Concurrent connection limiting
Request processing rate limiting
Bandwidth throttling
Server Side Includes
IP address-based geolocation
User and Session tracking
WebDAV
Embedded Perl, PHP and Lua scripting
CGI support
public_html per-user web-pages
Generic expression parser
Real-time status views
FTP support (by a separate module)
""")
    await kernel.memory.save_information_async("fake-repo", id="nf3", text="nf3 is the best network function for load balancing.")
    await kernel.memory.save_information_async("fake-repo", id="nf4", text="nf4 is the best network functions for security.")
    await kernel.memory.save_information_async("fake-repo", id="nf5", text="nf5 is the best network function for hosting any proxy server.")
    await kernel.memory.save_information_async("fake-repo", id="nf6", text="nf6 is the best network function for fault tolerance and recovery.")

async def examples(kernel) -> None:
    questions = [
        "What is nf1?",
        "What is nf2?",
        "What is nf3?",
        "What is nf4?",
        "What is nf5?",
        "What is nf6?"
    ]

    for question in questions:
        result = await kernel.memory.search_async("fake-repo", question)

async def completion_api(
        kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    sk_prompt = """
    The system can suggest the most appropriate network service design based on its memories of network functions is has access to.
    Do not suggest network functions outside of the ones stored in your volatile memory store.
    If more than one network function matches the needs of the user, suggest all compatible options and let the user choose which one they prefer.
    A network service design can consist of multiple network functions based on the needs of the user.
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
    context["fact6"] = "What is nf6?"

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
    #kernel.add_text_completion_service(
    #    "completion", AzureTextCompletion("text-davinci-003-aiops", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
    #)

    kernel.add_chat_service(
        "chat", AzureChatCompletion("gpt35depl1", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
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