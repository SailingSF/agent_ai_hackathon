from openai import OpenAI

def get_perplexity_response(query_string, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Provide accurate and up-to-date information based on the user's query."
        },
        {
            "role": "user",
            "content": query_string
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3-sonar-large-32k-online",
            messages=messages,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # This block will only run if the script is executed directly
    api_key = "PERPLEXITY_API_KEY"
    
    # Test the function with a sample query
    """ query = "What are the latest developments in artificial intelligence?"
    result = get_perplexity_response(query, api_key)

    if result:
        print("Query:", query)
        print("\nResponse:")
        print(result)
    else:
        print("Failed to get a response.") """

    # Allow user to input their own queries
    while True:
        user_query = input("\nEnter your query (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        result = get_perplexity_response(user_query, api_key)
        if result:
            print("\nResponse:")
            print(result)
        else:
            print("Failed to get a response.")
