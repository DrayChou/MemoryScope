"""
Warning!

This script purges the entire vector store !

"""

import sys
sys.path.append(".")
from memoryscope import MemoryScope, Arguments

arguments = Arguments(
    language="en",
    human_name="user",
    assistant_name="AI",
    memory_chat_class="api_memory_chat",
    generation_backend="openai_generation",
    generation_model="gpt-4o",
    embedding_backend="openai_embedding",
    embedding_model="text-embedding-3-small",
    enable_ranker=False,
)

ms = MemoryScope(arguments=arguments)
msms = ms._context.memory_store.es_store
msms.sync_delete_all()
