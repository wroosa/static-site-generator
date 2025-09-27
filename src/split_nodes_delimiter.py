from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    for node in old_nodes:
        # Only split nodes that are text that has not already been identified
        if node.text_type == TextType.TEXT:

        # Find all the runs of the delimiter and where they start
            runs = []
            start = None
            count = 0
        for i, c in enumerate(node.text):
            if c == delimiter:
                if count == 0:
                    start = i
                count +=1
            elif count:
                runs.append((start, count))
                count = 0
        if count:
            runs.append((start, count))
        
        

        
    return runs
            
                    



test_node = TextNode("hello ``` what's up `` fellow ``` people `` asdkjash `", TextType.TEXT)

print(split_nodes_delimiter([test_node], "`", TextType.CODE))