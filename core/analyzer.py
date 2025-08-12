import os

class ContextAnalyzer:
    """
    Scans and analyzes a given project directory to identify key components like models and controllers.
    """
    def __init__(self, project_path):
        self.project_path = project_path
        self.analysis_report = {}

    def analyze(self):
        """
        Performs a deep analysis to find C# models and controllers by filename.
        """
        if not os.path.isdir(self.project_path):
            self.analysis_report = {"error": "The provided path is not a valid directory."}
            return self.analysis_report

        models_path = os.path.join(self.project_path, "Models")
        controllers_path = os.path.join(self.project_path, "Controllers")

        found_models = self._find_classes_in_dir(models_path, ".cs")
        # For controllers, we strip the 'Controller' suffix to match them to models
        found_controllers = [name.replace("Controller", "") for name in self._find_classes_in_dir(controllers_path, "Controller.cs")]

        self.analysis_report = {
            "models": found_models,
            "controllers": found_controllers
        }
        return self.analysis_report

    def _find_classes_in_dir(self, directory, suffix):
        """Helper function to find files with a specific suffix and extract a class name."""
        if not os.path.isdir(directory):
            return []
        
        class_names = []
        for filename in os.listdir(directory):
            if filename.endswith(suffix):
                # 'Product.cs' -> 'Product'
                # 'ProductsController.cs' -> 'Products'
                class_name = filename.replace(suffix, "")
                class_names.append(class_name)
        return class_names