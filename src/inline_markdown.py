from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res_list = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            res_list.append(node)
            continue
        node_list = node.text.split(delimiter)
        if len(node_list) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for idx, n in enumerate(node_list):
            if idx % 2 != 0:
                res_list += [TextNode(n, text_type)]
            else:
                res_list += [TextNode(n, TextType.TEXT)]
    return res_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    res_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res_list += [node]
            continue
        link_list = extract_markdown_images(node.text)
        base_text = node.text
        for alt, link in link_list:
            sections = base_text.split(f"![{alt}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                res_list += [TextNode(sections[0], TextType.TEXT)]
            res_list += [TextNode(alt, TextType.IMAGE, link)]
            base_text = "".join(sections[1:])
        if base_text != "":
            res_list += [TextNode(base_text, TextType.TEXT)]
    return res_list
    
def split_nodes_link(old_nodes):
    res_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res_list += [node]
            continue
        link_list = extract_markdown_links(node.text)
        base_text = node.text
        for alt, link in link_list:
            sections = base_text.split(f"[{alt}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                res_list += [TextNode(sections[0], TextType.TEXT)]
            res_list += [TextNode(alt, TextType.LINK, link)]
            base_text = "".join(sections[1:])
        if base_text != "":
            res_list += [TextNode(base_text, TextType.TEXT)]
    return res_list

def text_to_textnodes(text):
    base_node = TextNode(text, TextType.TEXT)
    res = split_nodes_delimiter([base_node], "**", TextType.BOLD)
    res = split_nodes_delimiter(res, "*", TextType.ITALIC)
    res = split_nodes_delimiter(res, "`", TextType.CODE)
    res = split_nodes_link(res)
    res = split_nodes_image(res)
    return res