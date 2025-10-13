def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('#', 0, 1) and line[1] == ' ':
            return line.strip('# ')
    raise Exception('Error: No title header found')
    