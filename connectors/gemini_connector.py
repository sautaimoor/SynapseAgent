import google.generativeai as genai

class GeminiConnector:
    """
    Handles all communication with the Google Gemini API.
    """
    def __init__(self, api_key, model_name="gemini-1.5-pro-latest"):
        if not api_key:
            raise ValueError("API key for Gemini is missing.")
        
        self.api_key = api_key
        self.model_name = model_name
        
        # Configure the generative AI client
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        print("✅ Gemini Connector initialized.")

    def generate_text(self, prompt):
        """
        Sends a prompt to the Gemini API and returns the response.
        """
        try:
            print("🧠 Sending prompt to Gemini API...")
            response = self.model.generate_content(prompt)
            # Add basic safety check
            if not response.parts:
                 return "Error: Received an empty response from the API. This might be due to a safety block."
            return response.text
        except Exception as e:
            print(f"Error communicating with Gemini API: {e}")
            return f"Error: Could not get a response from the API. Details: {e}"