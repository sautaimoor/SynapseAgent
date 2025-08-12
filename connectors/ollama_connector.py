import requests
import json

class OllamaConnector:
    """
    Handles all communication with a local Ollama server.
    """
    def __init__(self, base_url="http://localhost:11434", model="llama3"):
        self.base_url = f"{base_url}/api/generate"
        self.model = model
        print("✅ Ollama Connector initialized.")

    def generate_text(self, prompt):
        """
        Sends a prompt to the local Ollama API and returns the response.
        """
        try:
            print(f"🧠 Sending prompt to local model '{self.model}'...")
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False  # We want the full response at once
            }
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # The response from Ollama is a JSON string, we need to parse it
            response_json = response.json()
            return response_json.get("response", "Error: No 'response' key in Ollama output.")

        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to the Ollama server. Is it running?"
        except Exception as e:
            return f"Error communicating with Ollama API: {e}"