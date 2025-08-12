import json
import os
from connectors.factory import get_provider
from core.analyzer import ContextAnalyzer
from core.file_manager import FileManager

# --- Configuration Loader (no changes) ---
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "config.json not found."}
    except json.JSONDecodeError:
        return {"error": "config.json is not formatted correctly."}

# --- Function to Handle Model Creation (no changes) ---
def handle_create_model(ai_provider, project_path):
    print("\n--- Create New C# Model ---")
    if not os.path.isdir(project_path):
        print(f"❌ Error: Project path '{project_path}' does not exist.")
        return
        
    model_name = input("Enter the model name (e.g., Product, User):\n> ").strip().capitalize()
    properties = input("Enter the properties as a comma-separated list (e.g., string Name, decimal Price, int StockLevel):\n> ")
    
    project_name = os.path.basename(project_path)
    namespace = f"{project_name}.Models"

    prompt = f"""
    You are an expert C# ASP.NET Core developer. Your task is to generate a C# model class file.
    Namespace: {namespace}, Model Name: {model_name}, Properties: {properties}
    Instructions:
    1. Generate a public class for the model. Include a public integer property named 'Id'.
    2. Add the specified properties. Use appropriate data types and data annotations.
    3. Only return the raw C# code without any extra text or markdown.
    """
    
    print("\n✅ Prompt engineered. Generating C# code with the AI...")
    generated_code = ai_provider.generate_text(prompt).strip()
    
    print("\n--- 🤖 Generated C# Code ---\n" + generated_code + "\n-----------------------------\n")
    
    confirm = input("Do you want to save this file? [y/n]: ").lower()
    
    if confirm == 'y':
        file_manager = FileManager()
        file_path = os.path.join(project_path, "Models", f"{model_name}.cs")
        file_manager.create_file(file_path, generated_code)
    else:
        print("❌ Aborted. File not saved.")

# --- NEW Function for General Analysis ---
def handle_general_analysis(ai_provider, project_path):
    """Orchestrates the general project analysis and reports the status."""
    print("\n🔍 Running general analysis...")
    analyzer = ContextAnalyzer(project_path)
    report = analyzer.analyze()

    if "error" in report:
        print(f"❌ Analysis failed: {report['error']}")
        return

    # Logic to determine what's done vs. remaining
    done_items = []
    remaining_items = []
    for model in report["models"]:
        # A model is 'done' if a controller with the pluralized name exists
        # This is a simplification; a real check would be more complex
        if model in report["controllers"]:
            done_items.append(f"Model '{model}' has a matching Controller.")
        else:
            remaining_items.append(f"Model '{model}' is missing a corresponding Controller.")
    
    if not done_items and not remaining_items:
        print("ℹ️ No models found to analyze. Try creating a model first.")
        return

    # Engineer the prompt for the AI
    prompt = f"""
    You are an expert ASP.NET project manager. Based on the following status report, provide a short, user-friendly summary for the developer. 
    Highlight what is complete and what the most logical next step is.

    STATUS REPORT:
    - Completed Items: {', '.join(done_items) if done_items else 'None'}
    - Missing Items: {', '.join(remaining_items) if remaining_items else 'None'}

    YOUR SUMMARY:
    """

    print("✅ Analysis logic complete. Generating summary with the AI...")
    ai_summary = ai_provider.generate_text(prompt)
    
    print("\n--- 🤖 AI Project Analysis ---")
    print(ai_summary)
    print("-----------------------------\n")


# --- Main Function with Updated Menu ---
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
        print("[2] Run General Project Analysis")
        print("[q] Quit")
        choice = input("> ").lower()

        if choice == '1':
            handle_create_model(ai_provider, project_path)
        elif choice == '2':
            handle_general_analysis(ai_provider, project_path)
        elif choice == 'q':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()