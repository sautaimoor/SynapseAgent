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

# --- Function for General Analysis (no changes) ---
def handle_general_analysis(ai_provider, project_path):
    print("\n🔍 Running general analysis...")
    analyzer = ContextAnalyzer(project_path)
    report = analyzer.analyze()

    if "error" in report:
        print(f"❌ Analysis failed: {report['error']}")
        return

    done_items = []
    remaining_items = []
    for model in report["models"]:
        if model in report["controllers"]:
            done_items.append(f"Model '{model}' has a matching Controller.")
        else:
            remaining_items.append(f"Model '{model}' is missing a corresponding Controller.")
    
    if not done_items and not remaining_items:
        print("ℹ️ No models found to analyze. Try creating a model first.")
        return

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
    
    print("\n--- 🤖 AI Project Analysis ---\n" + ai_summary + "\n-----------------------------\n")

# --- NEW Function for Controller Creation ---
def handle_create_controller(ai_provider, project_path):
    """Orchestrates the process of creating a new C# controller."""
    print("\n--- Create New C# Controller ---")
    if not os.path.isdir(project_path):
        print(f"❌ Error: Project path '{project_path}' does not exist.")
        return

    model_name = input("Enter the name of the Model to create a controller for (e.g., Product):\n> ").strip().capitalize()
    context_name = input("Enter the name of your DbContext class (e.g., ApplicationDbContext):\n> ").strip()

    project_name = os.path.basename(project_path)
    controller_name = f"{model_name}sController" # Pluralize for convention

    prompt = f"""
    You are an expert C# ASP.NET Core MVC developer. Your task is to generate a complete C# controller file with full CRUD functionality.

    Project Namespace: {project_name}
    Model Name: {model_name}
    DbContext Name: {context_name}
    Controller Name: {controller_name}

    Instructions:
    1. Create a public class named {controller_name} that inherits from 'Controller'.
    2. Add necessary 'using' statements for MVC, EntityFrameworkCore, and the project's Models namespace.
    3. Implement a constructor with dependency injection for the {context_name}.
    4. Generate standard async CRUD action methods: Index, Details, Create (GET and POST), Edit (GET and POST), Delete (GET and POST/DeleteConfirmed).
    5. The Index action should retrieve and display a list of all {model_name} objects.
    6. The POST actions should include the [HttpPost] and [ValidateAntiForgeryToken] attributes.
    7. Ensure all actions that take an 'id' parameter handle the case where the id is null or the object is not found.
    8. Only return the raw C# code without any extra text or markdown formatting.
    """

    print("\n✅ Prompt engineered. Generating C# controller code with the AI...")
    generated_code = ai_provider.generate_text(prompt).strip()

    print("\n--- 🤖 Generated C# Code ---\n" + generated_code + "\n-----------------------------\n")

    confirm = input("Do you want to save this file? [y/n]: ").lower()

    if confirm == 'y':
        file_manager = FileManager()
        file_path = os.path.join(project_path, "Controllers", f"{controller_name}.cs")
        file_manager.create_file(file_path, generated_code)
    else:
        print("❌ Aborted. File not saved.")


# --- Main Function with Final Menu ---
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
        print("[2] Create a new C# Controller")
        print("[3] Run General Project Analysis")
        print("[q] Quit")
        choice = input("> ").lower()

        if choice == '1':
            handle_create_model(ai_provider, project_path)
        elif choice == '2':
            handle_create_controller(ai_provider, project_path)
        elif choice == '3':
            handle_general_analysis(ai_provider, project_path)
        elif choice == 'q':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()