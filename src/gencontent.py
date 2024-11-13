import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return line[2:]
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        md_file = file.read()
    with open(template_path, 'r') as file:
        template_file = file.read()
        
    content = markdown_to_html_node(md_file).to_html()
    title = extract_title(md_file)
    template_file = template_file.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w+') as output_file_handler:
        output_file_handler.write(template_file)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for path in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, path)
        to_path = os.path.join(dest_dir_path, path)
        if os.path.isfile(from_path):
            to_path = to_path.replace(".md", ".html")
            generate_page(from_path, template_path, to_path)
        else:
            generate_pages_recursive(from_path, template_path, to_path)