import re

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [x.strip() for x in blocks if len(x.strip()) > 0]
    return blocks

def block_to_block_type(text):
    if re.findall(r"^(?:\#{1,6}) (?!#)", text):
        return block_type_heading
    if text[:3] == "```" and text[-3:] == "```" and len(text) >= 6: 
        return block_type_code
    split_text = text.split("\n")
    if text[0] == ">":
        for line in split_text:
            if not line[0] == ">":
                return block_type_paragraph
        return block_type_quote
    if text[:2] == "* " or text[:2] == "- ":
        for line in split_text:
            if line[:2] != "* " and line[:2] != "- ":
                return block_type_paragraph
        return block_type_ulist
    if text[:3] == "1. ":
        counter = 1
        for line in split_text:
            if line[:3] != f"{counter}. ":
                return block_type_paragraph
            counter += 1
        return block_type_olist    
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        html_node = block_to_node(block)
        children_nodes.append(html_node)
    return ParentNode("div", children_nodes)

def block_to_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return make_paragraph_block(block)
    if block_type == block_type_heading:
        return make_heading_block(block)
    if block_type == block_type_code:
        return make_code_block(block)
    if block_type == block_type_quote:
        return make_quote_block(block)
    if block_type == block_type_ulist:
        return make_list_block(block, "ul")
    if block_type == block_type_olist:
        return make_list_block(block, "ol")
    raise ValueError("Invalid block type")
            
def make_paragraph_block(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children_nodes = text_to_children(paragraph)
    return ParentNode("p", children_nodes)

def make_heading_block(block):
    h_count = len(block.split(" ")[0])
    children_nodes = text_to_children(block[h_count+1:])
    return ParentNode(f"h{h_count}", children_nodes)

def make_code_block(block):
    cleaned_block = block[3:-3]
    children_nodes = text_to_children(cleaned_block)
    code_block = ParentNode("code", children_nodes)
    return ParentNode("pre", [code_block])

def make_quote_block(block):
    lines = block.split("\n")
    quotes = []
    for line in lines:
        quotes.append(line[1:].strip())
    nodes = text_to_children(" ".join(quotes))
    return ParentNode("blockquote", nodes)

def make_list_block(block, type):
    if type != "ul" and type != "ol":
        raise ValueError("Invalid list type")
    lines = block.split("\n")
    items = []
    for line in lines:
        if type == "ul":
            children_nodes = text_to_children(line[2:])
        else:
            children_nodes = text_to_children(line[3:])
            
        items.append(ParentNode("li", children_nodes))
    
    return ParentNode(type, items)

def text_to_children(text):
    # Transform inner text into TextNode
    text_nodes = text_to_textnodes(text)
    nodes = []
    # Loop through text_nodes and return LeafNodes list
    for tn in text_nodes:
        nodes.append(text_node_to_html_node(tn))
    return nodes