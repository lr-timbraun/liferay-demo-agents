import os
import sys
import zipfile

def package_fragments(collection_dir, output_zip):
    """
    Packages a Liferay Fragment Collection into a ZIP file.
    Follows the strict structure expected by Liferay's importer.
    """
    if not os.path.isdir(collection_dir):
        print(f"Error: Directory {collection_dir} not found.")
        sys.exit(1)

    collection_root_name = os.path.basename(collection_dir.rstrip('/\\'))
    
    # Check for collection metadata
    if not os.path.exists(os.path.join(collection_dir, 'collection.json')):
        print(f"Error: Mandatory 'collection.json' missing in {collection_dir}")
        sys.exit(1)

    print(f"Packaging Fragment Collection '{collection_root_name}' into {output_zip}...")
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(collection_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # The arcname (path inside the ZIP) MUST start with the collection folder name
                relative_path = os.path.relpath(file_path, collection_dir)
                arcname = os.path.join(collection_root_name, relative_path)
                zipf.write(file_path, arcname=arcname)

    print(f"Successfully created {output_zip} in the project root.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python package-fragments.py <collection_directory> <output_zip_name>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_name = sys.argv[2]
    package_fragments(source_dir, output_name)
