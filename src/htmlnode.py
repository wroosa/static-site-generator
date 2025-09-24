

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attributes = ""
        if self.props is None:
            return attributes
        
        for prop in self.props:
            attributes += f' {prop}={self.props[prop]}'
        return attributes
    
    def __repr__(self):
        parts = [
            f"tag={self.tag}",
            f"value={self.value}",
            f"children={self.children}",
            f"props={self.props}",
        ]
        return f"HTMLNode({', '.join(parts)})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('All lead nodes must have a value')
        if self.tag is None:
            return self.value
        t = self.tag
        v = self.value
        return f"<{t}{self.props_to_html()}>{v}</{t}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('All parent nodes must have a tag')
        if self.children is None:
            raise ValueError('All parent nodes must have children')
        
        t = self.tag
        open_tag = f"<{t}{self.props_to_html()}>"
        close_tag = f"</{t}>"

        inner_html = ''
        for child in self.children:
            inner_html += child.to_html()
        
        return open_tag + inner_html + close_tag