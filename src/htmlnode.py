


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

