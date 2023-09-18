import asyncio
from typing import Tuple

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding, AzureChatCompletion
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#Search program to semantically compare descriptions of network functions to a user's needs

#TO DO: change the keyvault and endpoint to the new subscription's AI instance
credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://azopenai-dev-kv.vault.azure.net/", credential=credential)
ai_key = client.get_secret("AIKey1")

async def fake_repo(kernel: sk.Kernel) -> None:
    """
    Information to be written to the memories.
    
    Args:
        kernel: The instance of the semantic kernel.
    """
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
    await kernel.memory.save_information_async("fake-repo", id="nf3", text="nf3 is great for load balancing and security.")
    await kernel.memory.save_information_async("fake-repo", id="nf4", text="nf4 is great for security and hosting any proxy server.")
    await kernel.memory.save_information_async("fake-repo", id="nf5", text="nf5 is great for hosting any proxy server and fault tolerance and recovery.")
    await kernel.memory.save_information_async("fake-repo", id="nf6", text="nf6 is a great network function for configuring a resource bundle, AKS cluster, data retention, persistent storage, DNS zone, Azure Key Vault, managed identity, and encryption settings. It also includes properties for configuring the nf6 Search service and inter-nf6 Search interface encryption.")

async def examples(kernel) -> None:
    """
    Definitions of the network functions loaded from the memory to be used as context for the LLM.

    Args:
        kernel: The instance of the semantic kernel.
    """
    questions = [
        "What is nf1?",
        "What is nf2?",
        "What is nf3?",
        "What is nf4?",
        "What is nf5?",
        "What is nf6?"
    ]
    #Search through the volatile memory store to find the answer to the questions to be used as examples.
    for question in questions:
        print(f"\nQuestion: {question}")
        result = await kernel.memory.search_async("fake-repo", question)
        print(f"Answer: {result[0].text}")

async def completion_api(
        kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    """
    Create a semantic function and context for the LLM to search through when talking to the user.
    
    Args:
        kernel: The instance of the semantic kernel with necessary features to write a semantic function and add context.
    Returns:
        chat_func: Specifications of the semantic function being written.
        context: Context necessary for the LLM to make a decision.
    """
    #Load examples from memories into the semantic prompt using semantic function's TextMemorySkill
    sk_prompt = """
    The system can suggest the most appropriate network service design based on its memories of network functions is has access to.
    Do not suggest network functions outside of the ones stored in your volatile memory store.
    If more than one network function matches the needs of the user, suggest all compatible options in the following format:
    Network Function - reason for choosing network function.
    Let the user choose which one they prefer.
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
    #Create the semantic function
    chat_func = kernel.create_semantic_function(
        sk_prompt, max_tokens=400, temperature=0.8
    )
    #Setting up the definitions of the network functions as context variables
    context = kernel.create_new_context()
    context["fact1"] = "What is nf1?"
    context["fact2"] = "What is nf2?"
    context["fact3"] = "What is nf3?"
    context["fact4"] = "What is nf4?"
    context["fact5"] = "What is nf5?"
    context["fact6"] = "What is nf6?"
    #Accessing contents of the volatile memory store using semantic kernel's TextMemorySkill
    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "fake-repo"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = 0.4
    #Chat history is added as context
    context["chat_history"] = ""
    return chat_func, context

async def chat(
        kernel: sk.Kernel, chat_func: sk.SKFunctionBase, context: sk.SKContext
) -> bool:
    """
    Process the user input through the semantic function to have a conversation.

    Args:
        kernel: The instance of the semantic kernel.
        chat_func: The semantic function dictating the conversation between the user and the system.
        context: Supporting information for the LLM including the network functions definitions from the memories, the core skills for searching through a memory store and chat history.

    Returns:
        bool: If False, the conversation ends.
    """
    try:
        #Process user input and store as context variable to feed to semantic function
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
    #Invoke response using the chat completion service
    answer = await kernel.run_async(chat_func, input_vars=context.variables)
    #Add the system's response to the chat history and print it
    context["chat_history"] += f"\nUser: {user_input}\nChatBot: {answer}"
    print(f"ChatBot: {answer}")
    return True

async def main() -> None:
    """
    Instantiating the kernel, loading it with a chat and embedding service, loading the memories and running the chat function.
    """
    kernel = sk.Kernel()  
    #The semantic function prompt is simple enough to be run with a chat completion service without changing the system message
    kernel.add_chat_service(
        "chat", AzureChatCompletion("gpt35depl1", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
    )
    #Adding an embedding service so that the kernel can process its memories
    kernel.add_text_embedding_generation_service(
        "embedding", AzureTextEmbedding("text-embedding-ada-002", "https://azopenai-aiops.openai.azure.com/", ai_key.value)
    )
    #Instantiating a volatile memory store
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    #Importing one of semantic kernel's core skill responsible for reading a memory store
    kernel.import_skill(sk.core_skills.TextMemorySkill())
    #Loading the network function definitions to the volatile memory store
    await fake_repo(kernel)
    #Searching through the memory store to set examples for the semantic function
    await examples(kernel)
    #Loading the semantic function and context to the kernel
    chat_func, context = await completion_api(kernel)
    #Running the semantic function through the loaded kernel
    print("Begin Chatting (type 'exit' to exit): \n")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)

if __name__ == "__main__":
    asyncio.run(main())