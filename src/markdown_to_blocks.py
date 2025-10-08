

def markdown_to_blocks(doc):
    
    # Blocks of text
    blocks = []

    # Split doc by double new lines
    parts = doc.split("\n\n")

    for part in parts:
        stripped_block = part.strip()
        if stripped_block != "":
            blocks.append(stripped_block)
    
    return blocks