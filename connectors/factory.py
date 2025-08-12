from .gemini_connector import GeminiConnector
from .ollama_connector import OllamaConnector
# We will add imports for other connectors here later

def get_provider(config):
    """
    Reads the config and returns an instance of the active AI provider.
    """
    active_provider_name = config.get('active_provider')
    providers_config = config.get('providers', {})

    if active_provider_name == "gemini":
        gemini_config = providers_config.get('gemini', {})
        try:
            return GeminiConnector(api_key=gemini_config.get('api_key'), model_name=gemini_config.get('model'))
        except ValueError as e:
            print(f"Error initializing Gemini: {e}")
            return None

    elif active_provider_name == "ollama":
        ollama_config = providers_config.get('ollama', {})
        return OllamaConnector(base_url=ollama_config.get('base_url'), model=ollama_config.get('model'))

    # TODO: Add logic for 'openai' and 'deepseek' later

    else:
        print(f"Error: Unknown or unsupported provider '{active_provider_name}'")
        return None