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
    properties = input("Enter the properties as a comma-separated list (e.g., string Name, decimal Price):\n> ")
    project_name = os.path.basename(project_path)
    namespace = f"{project_name}.Models"
    prompt = f"""Generate a C# model class file. Namespace: {namespace}, Model Name: {model_name}, Properties: {properties}. Instructions: Create a public class with an 'Id' property. Add specified properties with data annotations. Return only raw C# code."""
    print("\n✅ Prompt engineered. Generating C# code...")
    generated_code = ai_provider.generate_text(prompt).strip()
    print("\n--- 🤖 Generated C# Code ---\n" + generated_code + "\n-----------------------------\n")
    if input("Do you want to save this file? [y/n]: ").lower() == 'y':
        FileManager().create_file(os.path.join(project_path, "Models", f"{model_name}.cs"), generated_code)
    else:
        print("❌ Aborted.")

# --- Function for Controller Creation (no changes) ---
def handle_create_controller(ai_provider, project_path):
    print("\n--- Create New C# Controller ---")
    if not os.path.isdir(project_path):
        print(f"❌ Error: Project path '{project_path}' does not exist.")
        return
    model_name = input("Enter the Model name for the controller (e.g., Product):\n> ").strip().capitalize()
    context_name = input("Enter your DbContext class name (e.g., ApplicationDbContext):\n> ").strip()
    project_name = os.path.basename(project_path)
    controller_name = f"{model_name}sController"
    prompt = f"""Generate a complete C# controller with full async CRUD actions. Project: {project_name}, Model: {model_name}, DbContext: {context_name}, Controller: {controller_name}. Instructions: Inherit from Controller, use DI for the DbContext, generate Index, Details, Create (GET/POST), Edit (GET/POST), Delete (GET/POST) actions. Use [ValidateAntiForgeryToken]. Return only raw C# code."""
    print("\n✅ Prompt engineered. Generating C# controller code...")
    generated_code = ai_provider.generate_text(prompt).strip()
    print("\n--- 🤖 Generated C# Code ---\n" + generated_code + "\n-----------------------------\n")
    if input("Do you want to save this file? [y/n]: ").lower() == 'y':
        FileManager().create_file(os.path.join(project_path, "Controllers", f"{controller_name}.cs"), generated_code)
    else:
        print("❌ Aborted.")

# --- Function for General Analysis (no changes) ---
def handle_general_analysis(ai_provider, project_path):
    print("\n🔍 Running general analysis...")
    analyzer = ContextAnalyzer(project_path)
    report = analyzer.analyze()
    if "error" in report:
        print(f"❌ Analysis failed: {report['error']}")
        return
    done_items = [f"Model '{m}' has a Controller." for m in report["models"] if m in report["controllers"]]
    remaining_items = [f"Model '{m}' is missing a Controller." for m in report["models"] if m not in report["controllers"]]
    if not done_items and not remaining_items:
        print("ℹ️ No models found to analyze.")
        return
    status_report = f"Completed: {', '.join(done_items) or 'None'}. Missing: {', '.join(remaining_items) or 'None'}."
    prompt = f"You are an expert ASP.NET project manager. Based on this status, give a brief, friendly summary and suggest the next logical step. Status: {status_report}"
    print("✅ Analysis logic complete. Generating summary...")
    ai_summary = ai_provider.generate_text(prompt)
    print("\n--- 🤖 AI Project Analysis ---\n" + ai_summary + "\n-----------------------------\n")

# --- NEW Function for View Generation ---
def handle_generate_views(ai_provider, project_path):
    """Orchestrates the generation of all 5 standard CRUD views for a model."""
    print("\n--- Generate CRUD Views ---")
    if not os.path.isdir(project_path):
        print(f"❌ Error: Project path '{project_path}' does not exist.")
        return

    model_name = input("Enter the Model name to generate views for (e.g., Product):\n> ").strip().capitalize()
    properties_str = input(f"Enter the properties of the '{model_name}' model (e.g., Name, Price, CreatedDate):\n> ")
    
    project_name = os.path.basename(project_path)
    view_folder_path = os.path.join(project_path, "Views", f"{model_name}s")
    views_to_generate = ["Index", "Create", "Edit", "Details", "Delete"]

    for view_name in views_to_generate:
        print(f"\n--- Generating '{view_name}' view for '{model_name}' ---")
        
        prompt = f"""
        You are an expert ASP.NET Core developer specializing in Razor views.
        Generate the C# Razor code for the '{view_name}.cshtml' view for a model named '{model_name}'.

        Project Namespace: {project_name}
        Model Name: {model_name}
        Model Properties: {properties_str}

        Specific Instructions for '{view_name}' view:
        - Index View: Create a table listing all items. Include columns for properties. Add 'Edit', 'Details', 'Delete' links for each row and a 'Create New' link at the top.
        - Create View: Generate a form with input fields for all specified properties. Use 'asp-for' tag helpers. Include a 'Create' button and a 'Back to List' link.
        - Edit View: Generate a form similar to the Create view but include a hidden input for the 'Id'.
        - Details View: Display all properties of a single item in a definition list (`<dl>`). Include 'Edit' and 'Back to List' links.
        - Delete View: Display the details of the item to be deleted and a confirmation form with a 'Delete' button.
        
        The model is located at `@model {project_name}.Models.{model_name}`.
        Only return the raw C# Razor code for the {view_name}.cshtml file. Do not include any extra text or markdown.
        """
        
        generated_code = ai_provider.generate_text(prompt).strip()
        print("\n--- 🤖 Generated Razor Code ---\n" + generated_code + "\n-----------------------------\n")

        if input(f"Do you want to save this '{view_name}.cshtml' file? [y/n]: ").lower() == 'y':
            FileManager().create_file(os.path.join(view_folder_path, f"{view_name}.cshtml"), generated_code)
        else:
            print("❌ Aborted for this file.")
    print("\n✅ View generation process complete.")


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
        print("[3] Generate CRUD Views for a Model")
        print("[4] Run General Project Analysis")
        print("[q] Quit")
        choice = input("> ").lower()

        if choice == '1': handle_create_model(ai_provider, project_path)
        elif choice == '2': handle_create_controller(ai_provider, project_path)
        elif choice == '3': handle_generate_views(ai_provider, project_path)
        elif choice == '4': handle_general_analysis(ai_provider, project_path)
        elif choice == 'q':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()