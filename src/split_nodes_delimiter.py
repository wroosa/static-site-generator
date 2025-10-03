from textnode import TextType, TextNode

# Helper function to skip elements of an enum
def skip(iterator, n):
    for _ in range(n):
        next(iterator, None)

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        # Only split nodes that are text that has not already been identified
        if node.text_type == TextType.TEXT:

        # Find all the runs of the delimiter and where they start
            runs = []
            start = None
            count = 0
            last_end = 0

            text_enum = enumerate(node.text)
            for i, c in text_enum:
                if c == delimiter:
                    if count == 0:
                        start = i
                    count +=1
                elif count:
                    runs.append((start, count))
                    close = node.text.find(count * delimiter, i + 1)
                    if close != -1:

                        pre = node.text[last_end:start]
                        if pre != '':
                            pre_node = TextNode(pre, TextType.TEXT)
                            new_nodes.append(pre_node)

                        match = node.text[start + count:close]
                        match_node = TextNode(match, text_type)
                        new_nodes.append(match_node)

                        last_end = close + count
                        skip(text_enum, close - i + count)

                    count = 0
            

            if last_end == 0:
                # Add the whole node as text
                new_nodes.append(node)
            elif last_end < len(node.text):
                new_nodes.append(TextNode(node.text[last_end:], TextType.TEXT))
                                 
        else:
            new_nodes.append(node)
        
    return new_nodes


