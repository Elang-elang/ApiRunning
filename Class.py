import json

class chatAI:
    """
    Unified AI chat client supporting OpenAI (via official SDK), HTTP requests, and Ollama.
    """

    @staticmethod
    def openaiClient(base_url: str, api_key: str) -> str:
        """
        Instantiate the OpenAI client with a custom base URL and API key.
        """
        import openai
        # Create and configure OpenAI SDK client
        return openai.OpenAI(base_url=base_url, api_key=api_key)

    @staticmethod
    def openaiChat(
        client: str,
        model: str,
        prompt: str,
        system: str
    ) -> str:
        """
        Send a chat completion request via the OpenAI SDK.
        """
        import openai
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            response = client.chat.completions.create(model=model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI SDK error: {e}"

    @staticmethod
    def HttpChat(
        api_key: str,
        model: str,
        endpoint: str,
        prompt: str,
        system: str
    ) -> str:
        """
        Send a chat completion request via direct HTTP to a compatible API endpoint.
        """
        import requests
        payload = {"model": model, "messages": []}
        if system:
            payload["messages"].append({"role": "system", "content": system})
        payload["messages"].append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(endpoint, headers=headers, json=payload)
            resp.raise_for_status()
        except requests.RequestException as e:
            return f"HTTP request error: {e}"

        try:
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "No reply content")
        except (ValueError, KeyError) as e:
            return f"Invalid JSON response: {e}"

    @staticmethod
    def OllamaChat(
        model: str,
        prompt: str,
        system: str
    ) -> str:
        """
        Send a chat completion request via Ollama.
        """
        import ollama
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            result = ollama.chat(model=model, messages=messages)
            return result.get("message", {}).get("content", "")
        except Exception as e:
            return f"Ollama error: {e}"
    def ident():
        print("""
    Creator: Elang-elang
    
    Github: https://github.com/Elang-elang
    
    testamentary message:
        
        Thank you for trying this code
        
        have a nice day, while coding
        
""")
