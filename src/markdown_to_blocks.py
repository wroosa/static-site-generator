

def markdown_to_blocks(doc):
    
    # Blocks of text
    blocks = []

    # Split doc by double new lines
    parts = doc.split("\n\n")

    for part in parts:
        if part !="":
            blocks.append(part.strip())
    
    return blocks