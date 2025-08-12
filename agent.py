import json
from connectors.factory import get_provider
from core.analyzer import ContextAnalyzer
from core.file_manager import FileManager
import os # We need os for path joining

# --- Configuration Loader (no changes) ---
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "config.json not found."}
    except json.JSONDecodeError:
        return {"error": "config.json is not formatted correctly."}

# --- New Function to Handle Model Creation ---
def handle_create_model(ai_provider, project_path):
    """Orchestrates the process of creating a new C# model."""
    print("\n--- Create New C# Model ---")
    if not os.path.isdir(project_path):
        print(f"❌ Error: Project path '{project_path}' does not exist.")
        return
        
    model_name = input("Enter the model name (e.g., Product, User):\n> ").strip().capitalize()
    properties = input("Enter the properties as a comma-separated list (e.g., string Name, decimal Price, int StockLevel):\n> ")
    
    # Guess the namespace from the project folder name
    project_name = os.path.basename(project_path)
    namespace = f"{project_name}.Models"

    # Engineer the prompt for the AI
    prompt = f"""
    You are an expert C# ASP.NET Core developer. Your task is to generate a C# model class file.
    
    Namespace: {namespace}
    Model Name: {model_name}
    Properties: {properties}

    Instructions:
    1. Generate a public class for the model.
    2. Include a public integer property named 'Id' as the primary key.
    3. Add the properties as specified by the user.
    4. Use appropriate data types.
    5. Add necessary 'using' statements (e.g., System.ComponentModel.DataAnnotations).
    6. Do NOT include any other text, explanation, or markdown formatting. Only return the raw C# code.
    """
    
    print("\n✅ Prompt engineered. Generating C# code with the AI...")
    generated_code = ai_provider.generate_text(prompt).strip()
    
    # --- Human-in-the-Loop Verification ---
    print("\n--- 🤖 Generated C# Code ---")
    print(generated_code)
    print("-----------------------------\n")
    
    confirm = input("Do you want to save this file? [y/n]: ").lower()
    
    if confirm == 'y':
        file_manager = FileManager()
        file_path = os.path.join(project_path, "Models", f"{model_name}.cs")
        file_manager.create_file(file_path, generated_code)
    else:
        print("❌ Aborted. File not saved.")


# --- Refactored Main Function with Command Loop ---
def main():
    print("🚀 Welcome to Project Synapse!")
    
    config = load_config()
    if "error" in config:
        print(f"❌ {config['error']}")
        return

    ai_provider = get_provider(config)
    if not ai_provider:
        print("❌ Could not initialize AI provider. Exiting.")
        return
        
    project_path = input("First, please enter the full path to your target ASP.NET project:\n> ")

    while True:
        print("\n--- Synapse Menu ---")
        print("[1] Create a new C# Model")
        print("[2] Analyze Project (coming soon)")
        print("[q] Quit")
        choice = input("> ").lower()

        if choice == '1':
            handle_create_model(ai_provider, project_path)
        elif choice == '2':
            print("Feature coming soon!")
            # TODO: Add call to analyzer here
        elif choice == 'q':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()