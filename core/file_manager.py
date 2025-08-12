import os

class FileManager:
    """Handles safe creation and modification of files."""

    def create_file(self, file_path, content):
        """
        Creates a new file with the given content.
        It will create parent directories if they don't exist.
        Returns True on success, False on failure.
        """
        try:
            # Ensure the parent directory exists
            parent_dir = os.path.dirname(file_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
                print(f"📁 Created directory: {parent_dir}")

            # Write the content to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Successfully saved file: {file_path}")
            return True
        except IOError as e:
            print(f"❌ Error saving file {file_path}: {e}")
            return False