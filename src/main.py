import os
import shutil
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    copy_contents()
    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )

def copy_contents():
    static_path = "./static"
    public_path = "./public"
    # Clear directory
    print("Deleting public directory...")
    clear_public_directory(public_path)
    # Copy files from static to public
    print("Copying static files to public directory...")
    copy_files(static_path, public_path)
    
def clear_public_directory(public_path):
    # Clear public directory
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
        
def copy_files(path, destination):
    # Copy files from static
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        file_destination = os.path.join(destination, f)
        if os.path.isfile(file_path):
            print(f"From: {file_path}, To: {destination}/{f}")
            if not os.path.isdir(destination):
                os.mkdir(destination)
            shutil.copy(file_path, file_destination)
        else:
            copy_files(file_path, file_destination)
    
if __name__ == "__main__":
    main()
    