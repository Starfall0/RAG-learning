from langchain_openai import OpenAIEmbeddings

def get_embedding_function():
    embeddings = OpenAIEmbeddings(
        openai_api_base = "http://localhost:1234/v1",
        api_key="your-api-key",
        model = "text-embedding-nomic-embed-text-v1.5-embedding",
        check_embedding_ctx_length= False
    )
    return embeddings
