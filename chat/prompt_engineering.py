def create_prompt(query):
    return f"Given the following query, provide an appropriate response:\nQuery: {query}"

if __name__ == "__main__":
    user_query = "What is AI?"
    print(create_prompt(user_query))
