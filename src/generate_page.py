from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title
from pathlib import Path
from bs4 import BeautifulSoup

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as file:
        markdown = file.read()

    with open(template_path, 'r') as file:
        template = file.read()

    # Create the final HTML based on the markdown and template
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace('{{ Title }}', title).replace('{{ Content }}', content)
    # pretty_html = BeautifulSoup(html).prettify()

    # Create the HTML file and write the HTML to it
    html_file = Path(dest_path)
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(html)


    
    


