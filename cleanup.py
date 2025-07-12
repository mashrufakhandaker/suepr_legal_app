import os
import shutil

def clean_pycache(path):
    for root, dirs, files in os.walk(path):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            print(f"Removing: {pycache_path}")
            shutil.rmtree(pycache_path)

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.abspath(__file__))
    clean_pycache(project_path)
    print("Cleanup complete.")