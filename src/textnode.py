from enum import Enum

from htmlnode import LeafNode

import re

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self,other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None,value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img",value="",props={"src":text_node.url,"alt":text_node.text})
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    l = []
    for o in old_nodes:
        if o.text_type != TextType.TEXT:
            l.append(o)
        else:
            t = o.text.split(delimiter)
            if len(t) == 1:
                # no delimiter, append as-is
                l.append(o)
            elif (len(t) % 2) == 0:
                raise Exception("no matching delimiter")
            else:
                n_num = 0
                for nnode in t:
                    n_num +=1
                    if nnode == "":
                        pass #delimiter at start or end of text so empty string
                    elif n_num % 2 == 1:
                        l.append(TextNode(nnode, TextType.TEXT))
                    else:
                        l.append(TextNode(nnode,text_type))
    return l

def extract_markdown_images(text):
    return re.findall(r'!\[([^\]]*)\]\(([^\)]*)\)',text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_li(textnode):
    links = extract_markdown_links(textnode.text)
    if len(links) == 0:
        return [textnode,]
    unprocessedtext=textnode.text
    newnodes = []
    for (linktext,linkaddr) in links:
        sections = unprocessedtext.split(f"[{linktext}]({linkaddr})",1)
        if len(sections[0]) != 0:
            newnodes.append(TextNode(sections[0],TextType.TEXT))
        newnodes.append(TextNode(linktext,TextType.LINK,linkaddr))
        unprocessedtext = sections[1]
    if len(unprocessedtext) != 0:
        newnodes.append(TextNode(unprocessedtext,TextType.TEXT))
    return newnodes

def split_nodes_link(textnodes):
    o = []
    for x in textnodes:
        if x.text_type != TextType.TEXT:
            o.append(x)
        else:
            o += (split_nodes_li(x))
    return o

def split_nodes_img(textnode):
    links = extract_markdown_images(textnode.text)
    if len(links) == 0:
        return [textnode,]
    unprocessedtext=textnode.text
    newnodes = []
    for (linktext,linkaddr) in links:
        sections = unprocessedtext.split(f"![{linktext}]({linkaddr})",1)
        if len(sections[0]) != 0:
            newnodes.append(TextNode(sections[0],TextType.TEXT))
        newnodes.append(TextNode(linktext,TextType.IMAGE,linkaddr))
        unprocessedtext = sections[1]
    if len(unprocessedtext) != 0:
        newnodes.append(TextNode(unprocessedtext,TextType.TEXT))
    return newnodes

def split_nodes_image(textnodes):
    o = []
    for x in textnodes:
        if x.text_type != TextType.TEXT:
            o.append(x)
        else:
            o += (split_nodes_img(x))
    return o

def text_to_textnodes(text):
    textnodes = [TextNode(text,TextType.TEXT),]
    # BOLD = "bold"
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    # ITALIC = "italic"
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    # CODE = "code"
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    # IMAGE = "image"
    textnodes = split_nodes_image(textnodes)
    # LINK = "link"
    textnodes = split_nodes_link(textnodes)
    return textnodes

def markdown_to_blocks(text):
    sections = text.split("\n\n")
    l = []
    for s in sections:
        t = s.strip()
        if len(t) != 0:
            l.append(t)
    return l

class BlockType(Enum):

       PARAGRAPH                = "paragraph"
       HEADING                = "heading"
       CODE                = "code"
       QUOTE                = "quote"
       UNORDERED_LIST                = "unordered_list"
       ORDERED_LIST                = "ordered_list"

def block_to_block_type(text):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if (re.match(r"^#{1,6} ",text)):
        return BlockType.HEADING
    # Code blocks must start with 3 backticks and end with 3 backticks.
    if (text.startswith("```") and text.endswith("```")):
        return BlockType.CODE
    
    lines = text.split("\n")
    blockquote = True
    unorderedlist = True
    orderedlist = True
    n = 0
    for l in lines:
        n += 1
        if not l.startswith(">"):
            blockquote = False
        if not l.startswith("- "):
            unorderedlist = False
        if not l.startswith(str(n) + "."):
            orderedlist =False
    # Every line in a quote block must start with a > character.
    if blockquote:
        return BlockType.QUOTE
    # Every line in an unordered list block must start with a - character, followed by a space.
    if unorderedlist:
        return BlockType.UNORDERED_LIST
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    if orderedlist:
        return BlockType.ORDERED_LIST
    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH
