# setup.py
import os
import sys
from pathlib import Path

def setup_project():
    # Create project directories
    directories = [
        "data/documents",
        "data/chroma",
        "src",
        "config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    # Create __init__.py in src directory
    with open("src/__init__.py", "w") as f:
        pass

    # Create .env file with default configurations
    env_content = """# Environment Configuration
DEVICE=cuda if available, otherwise cpu
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print("Created .env file")

    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Place your PDF files in the data/documents directory")
    print("2. Install requirements using: pip install -r requirements.txt")
    print("3. Run the application using: streamlit run app.py")

if __name__ == "__main__":
    setup_project()