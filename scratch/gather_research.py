import os
import shutil
import glob

def gather_research():
    base_dir = r"c:\Users\lenovo\legal assistant"
    target_dir = os.path.join(base_dir, "Research_Publication_Workspace")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    subdirs = {
        "Code_and_Experiments": os.path.join(target_dir, "Code_and_Experiments"),
        "Data_and_Results": os.path.join(target_dir, "Data_and_Results"),
        "Publication_Drafts": os.path.join(target_dir, "Publication_Drafts"),
        "Visualizations": os.path.join(target_dir, "Visualizations"),
        "Learning_and_Docs": os.path.join(target_dir, "Learning_and_Docs")
    }
    
    for d in subdirs.values():
        os.makedirs(d, exist_ok=True)
        
    def copy_files(src_pattern, dest_folder):
        for file in glob.glob(os.path.join(base_dir, src_pattern), recursive=True):
            if os.path.isfile(file) and "Research_Publication_Workspace" not in file:
                dest_path = os.path.join(dest_folder, os.path.basename(file))
                # avoid overwriting with the same name, or handle it
                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(os.path.basename(file))
                    dest_path = os.path.join(dest_folder, f"{name}_copy{ext}")
                shutil.copy2(file, dest_path)
                print(f"Copied: {file} -> {dest_path}")

    # 1. Code and Experiments
    copy_files(r"research\experiments\*.py", subdirs["Code_and_Experiments"])
    copy_files(r"benchmarks\*.py", subdirs["Code_and_Experiments"])
    copy_files(r"scratch\get_mlflow_metrics.py", subdirs["Code_and_Experiments"])
    
    # 2. Data and Results
    copy_files(r"research\results\*", subdirs["Data_and_Results"])
    copy_files(r"benchmarks\*.json", subdirs["Data_and_Results"])
    
    # 3. Publication Drafts
    copy_files(r"research\publication\*", subdirs["Publication_Drafts"])
    copy_files(r"research\generate_paper.py", subdirs["Publication_Drafts"])
    
    # 4. Visualizations
    copy_files(r"research\visualizations\*", subdirs["Visualizations"])
    
    # 5. Learning and Docs
    copy_files(r"docs\**\*", subdirs["Learning_and_Docs"])
    copy_files(r"learning_notes\*", subdirs["Learning_and_Docs"])
    copy_files(r"research\datasets\LEARNING_NOTES.md", subdirs["Learning_and_Docs"])
    
    print("Research gathering complete.")

if __name__ == "__main__":
    gather_research()
