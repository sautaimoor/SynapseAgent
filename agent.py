import json
from connectors.factory import get_provider
from core.analyzer import ContextAnalyzer

def load_config():
    """Loads the configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "config.json not found."}
    except json.JSONDecodeError:
        return {"error": "config.json is not formatted correctly."}

def main():
    """Main entry point for the Synapse Agent."""
    print("🚀 Welcome to Project Synapse!")
    
    # --- Step 1: Load Config and AI Provider ---
    config = load_config()
    if "error" in config:
        print(f"❌ {config['error']}")
        return

    ai_provider = get_provider(config)
    if not ai_provider:
        print("❌ Could not initialize AI provider. Please check your config. Exiting.")
        return
    
    # --- Step 2: Get Project Path and Analyze ---
    project_path = input("Please enter the full path to the ASP.NET project to analyze:\n> ")
    analyzer = ContextAnalyzer(project_path)
    analysis_data = analyzer.analyze()

    if "error" in analysis_data:
        print(f"❌ Analysis failed: {analysis_data['error']}")
        return
        
    # --- Step 3: Engineer the Prompt ---
    # Get the human-readable text report from the analyzer
    analysis_text = analyzer.get_report_as_text()
    
    # Create a detailed prompt for the AI
    prompt = f"""
    You are an expert software architect. I will provide you with a summary of the files in an application directory. 
    Based *only* on this file summary, please provide a one-paragraph, high-level overview of what this project likely is and what technologies it uses.

    Here is the file summary:
    {analysis_text}

    Your summary:
    """
    
    print("\n✅ Analysis complete. Generating project summary with the AI...")
    
    # --- Step 4: Call the AI and Get Response ---
    ai_summary = ai_provider.generate_text(prompt)
    
    print("\n--- 🤖 AI Project Summary ---")
    print(ai_summary)
    print("----------------------------\n")

if __name__ == "__main__":
    main()