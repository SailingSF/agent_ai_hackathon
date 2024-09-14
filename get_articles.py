import requests

def get_perplexity_response(query_string, api_key):
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Provide accurate, relevant and up-to-date information based on the user's query. Be precise and concise. Please "
            },
            {
                "role": "user",
                "content": query_string
            }
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": True,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "day",
        "frequency_penalty": 1
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    api_key = "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"
    
    # Test the function with a sample query
    """ query = "How many stars are there in our galaxy?"
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
