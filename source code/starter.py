import subprocess
import sys
import importlib
import os

# List of required libraries
required_libraries = [
    "customtkinter",
    "Pillow"  # For PIL, the actual package name is Pillow
]

# Standard libraries
standard_libraries = [
    "os",
    "sqlite3"
]

def install_and_import(library):
    try:
        # Check if the library is already installed
        importlib.import_module(library)
        print(f"{library} is already installed.")
    except ImportError:
        # If not installed, install the library
        print(f"{library} is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        print(f"{library} installed successfully.")

def main():
    # Install and import all required libraries
    for library in required_libraries:
        install_and_import(library)
    
    # Check for standard libraries (no installation required)
    for library in standard_libraries:
        try:
            importlib.import_module(library)
            print(f"{library} is part of the standard library.")
        except ImportError:
            print(f"Error: {library} should be part of the standard library but was not found.")
    
    # Get the current directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run the main application file
    home_page_path = os.path.join(current_dir, "home_page.py")
    subprocess.run([sys.executable, home_page_path])

if __name__ == "__main__":
    main()
