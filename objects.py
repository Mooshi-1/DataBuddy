from enum import Enum

class QCTYPE(Enum):
    SR = 'spiked recovery'
    DL = 'dilution'
    CTL = 'control'
    CAL = 'calibrator'
    SH = 'shooter'
    MOA = 'method of addition'

def QC_handler(QC):
    
#enum example
#can use this to create other objects
# def text_node_to_html_node(text_node):
#     if text_node.text_type == TextType.TEXT:
#         return LeafNode(value=text_node.text)
#     if text_node.text_type == TextType.BOLD:
#         return LeafNode(tag="b",value=text_node.text)
#     if text_node.text_type == TextType.ITALIC:
#         return LeafNode(tag="i",value=text_node.text)
#     if text_node.text_type == TextType.CODE:
#         return LeafNode(tag="code",value=text_node.text)
#     if text_node.text_type == TextType.LINK:
#         return LeafNode(tag="a",value=text_node.text, props={"href": text_node.url})
#     if text_node.text_type == TextType.IMAGE:
#         return LeafNode(tag="img",value="", props={"src": text_node.url, "alt": text_node.text})    

#     else:
#         raise Exception("Not valid")

#define QC objects
class QC:
    def __init__(self, type, worksheet, path):
        self.type = type
        self.worksheet = worksheet
        self.path = path

example = QC(QCTYPE.SR, None, pdf_path)
#any subclasses needed?