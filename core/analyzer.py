import os

class ContextAnalyzer:
    """
    Scans and analyzes a given project directory to understand its structure.
    """
    def __init__(self, project_path):
        self.project_path = project_path
        self.analysis_report = {}

    def analyze(self):
        """
        Performs the analysis of the project directory.
        Returns a dictionary containing the analysis report.
        """
        if not os.path.isdir(self.project_path):
            self.analysis_report = {"error": "The provided path is not a valid directory."}
            return self.analysis_report

        file_count = 0
        dir_count = 0
        file_types = {}

        for root, dirs, files in os.walk(self.project_path):
            dir_count += len(dirs)
            file_count += len(files)
            for file in files:
                extension = os.path.splitext(file)[1]
                if extension:
                    file_types[extension] = file_types.get(extension, 0) + 1
        
        self.analysis_report = {
            "total_directories": dir_count,
            "total_files": file_count,
            "file_type_counts": file_types
        }
        return self.analysis_report

    def get_report_as_text(self):
        """
        Formats the analysis report into a human-readable text block.
        """
        if "error" in self.analysis_report:
            return self.analysis_report["error"]

        if not self.analysis_report:
            return "No analysis has been run yet."

        report_lines = [
            "--- Project Analysis Summary ---",
            f"Total Directories: {self.analysis_report.get('total_directories', 0)}",
            f"Total Files: {self.analysis_report.get('total_files', 0)}",
            "\nFile Type Distribution:"
        ]
        
        # Sort file types by count for cleaner presentation
        sorted_file_types = sorted(
            self.analysis_report.get('file_type_counts', {}).items(),
            key=lambda item: item[1],
            reverse=True
        )

        for ext, count in sorted_file_types:
            report_lines.append(f"  - {ext}: {count}")
        
        return "\n".join(report_lines)