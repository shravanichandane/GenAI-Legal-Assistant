import os

# Define project structure
project_structure = {
    "backend": {
        "main.py": "",
        "models.py": "",
        "database.py": "",
        "routes": {
            "upload.py": "",
            "analyze.py": "",
            "search.py": "",
            "health.py": ""
        },
        "services": {
            "llm_service.py": "",
            "clause_extractor.py": "",
            "risk_analyzer.py": "",
            "semantic_search.py": ""
        }
    },
    "frontend": {
        "app.py": "",
        "components": {
            "sidebar.py": "",
            "clause_editor.py": "",
            "charts.py": ""
        }
    },
    "requirements.txt": "",
    "README.md": "# Project Documentation\n\nThis is the initial project setup."
}


def create_structure(base_path, structure):
    """
    Recursively creates folders and files based on the structure dictionary.
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # It's a folder
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:  # It's a file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    base_directory = r"C:\Users\lenovo\legal assistant"  # Your project path
    create_structure(base_directory, project_structure)
    print(f"✅ Project structure created successfully in: {base_directory}")
