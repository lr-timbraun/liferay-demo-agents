import json
import os
import shutil
import sys
import zipfile

def package_stylebook(source_dir, output_zip):
    """
    Packages the contents of a Stylebook directory into a ZIP file.
    Only style-book.json and frontend-tokens-values.json are included.
    """
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory {source_dir} not found.")
        sys.exit(1)

    # Required files
    required_files = ["style-book.json", "frontend-tokens-values.json"]
    
    # Check if files exist in the source dir
    for f in required_files:
        if not os.path.exists(os.path.join(source_dir, f)):
            print(f"Error: Required file {f} missing in {source_dir}.")
            sys.exit(1)

    # Create the zip file in the project root
    stylebook_folder_name = os.path.basename(source_dir.rstrip('/\\'))
    print(f"Packaging {source_dir} into {output_zip}...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in required_files:
            file_path = os.path.join(source_dir, f)
            # Add file to zip inside a nested subdirectory (required by Liferay DXP)
            arcname = os.path.join(stylebook_folder_name, f)
            zipf.write(file_path, arcname=arcname)

    print(f"Successfully created {output_zip}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python package-stylebook.py <source_directory> <output_zip_name>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_zip = sys.argv[2]
    package_stylebook(source_dir, output_zip)
