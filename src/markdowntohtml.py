from htmlnode import *
from textnode import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []
    previousblocktype = ""
    listnodes = []
    for b in blocks:
        blocktype = block_to_block_type(b)
        # finish list if next item isn't list element
        if (blocktype != BlockType.UNORDERED_LIST and previousblocktype == BlockType.UNORDERED_LIST):
            htmlnodes.append(ParentNode("ul",listnodes))
            listnodes = []
        if (blocktype != BlockType.ORDERED_LIST and previousblocktype == BlockType.ORDERED_LIST):
            htmlnodes.append(ParentNode("ol",listnodes))
            listnodes = []

        if (blocktype == BlockType.PARAGRAPH):
            textnodes = text_to_textnodes(b.replace("\n"," "))
            htmlnodes.append(ParentNode("p",[text_node_to_html_node(n) for n in textnodes]))
        elif (blocktype == BlockType.HEADING):
            heading_level_endplace = b.find(" ")
            htmlnodes.append(LeafNode("h"+ str(heading_level_endplace),b[heading_level_endplace+1:]))
        elif (blocktype == BlockType.CODE):
            #todo: remove first and last ```
            htmlnodes.append(ParentNode("pre",[LeafNode("code",b[4:-3])]))
        elif (blocktype == BlockType.QUOTE):
            print("blockquote=}" + b + "{")
            htmlnodes.append(LeafNode("blockquote",(b[2:]).replace("\n> ","\n").replace("\n>","\n")))
        elif (blocktype == BlockType.UNORDERED_LIST):
            for el in b.split("\n"):
                li = (el.split("- "))[1]
                listnodes.append(LeafNode("li",li))
        elif (blocktype == BlockType.ORDERED_LIST):
            for el in b.split("\n"):
                li = el[el.find(".")+2:]
                print("el=>" + el + "<-")
                print("li=>" + li + "<-")
                listnodes.append(LeafNode("li",li))

        previousblocktype = blocktype

    # in case last block was a list
    if (previousblocktype == BlockType.UNORDERED_LIST):
        htmlnodes.append(ParentNode("ul",listnodes))
    if (previousblocktype == BlockType.ORDERED_LIST):
        htmlnodes.append(ParentNode("ol",listnodes))        

    return ParentNode("div",htmlnodes)
    
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for b in blocks:
        blocktype = block_to_block_type(b)
        if (blocktype == BlockType.HEADING):
            heading_level_endplace = b.find(" ")
            if heading_level_endplace == 1:
                return b[heading_level_endplace:].strip()
    raise("No title found")