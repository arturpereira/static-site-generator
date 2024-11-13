import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        text = "Text"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "paragraph",
        )
        
    def test_block_to_block_type_heading_one(self):
        text = "# Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "heading",
        )
        
    def test_block_to_block_type_heading_multiple(self):
        text = "###### Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "heading",
        )
        
    def test_block_to_block_type_heading_more_than_six(self):
        text = "####### Heading"
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "heading",
        )
        
    def test_block_to_block_type_heading_no_space(self):
        text = "#####Heading"
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "heading",
        )
        
    def test_block_to_block_type_code(self):
        text = "```Code```"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "code",
        )
        
    def test_block_to_block_type_code_incomplete(self):
        text = "```Code``"
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "code",
        )
        
    def test_block_to_block_type_quote(self):
        text = ">Quote"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "quote",
        )
        
    def test_block_to_block_type_unordered_list_line_one(self):
        text = "- List Item"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "unordered_list",
        )
        
    def test_block_to_block_type_unordered_list_asterisk_one(self):
        text = "* List Item"
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "unordered_list",
        )
        
    def test_block_to_block_type_unordered_list_asterisk_multiple(self):
        text = '''* List Item
        * List Item 2
        * List Item 3'''
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "unordered_list",
        )
        
    def test_block_to_block_type_unordered_list_asterisk_multiple_incorrect(self):
        text = '''* List Item
        * List Item 2
        List Item 3'''
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "unordered_list",
        )
        
    def test_block_to_block_type_unordered_list_no_space(self):
        text = "*List Item"
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "unordered_list",
        )

    def test_block_to_block_type_ordered_list_one(self):
        text = '''1. List Item'''
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "ordered_list",
        )
        
    def test_block_to_block_type_ordered_list_multiple(self):
        text = '''1. List Item
2. List Item 2
3. List Item 3'''
        block_type = block_to_block_type(text)
        self.assertEqual(
            block_type,
            "ordered_list",
        )
        
    def test_block_to_block_type_ordered_list_multiple_incorrect(self):
        text = '''1. List Item
2. List Item 2
4. List Item 3'''
        block_type = block_to_block_type(text)
        self.assertNotEqual(
            block_type,
            "ordered_list",
        )
        
class TestHeadingsBlocksToHTMLNodes(unittest.TestCase):
    def test_h_block_to_html_node(self):
        text = "## paragraph with *italic* and **bold**"
        nodes = markdown_to_html_node(text).to_html()
        self.assertEqual(
            nodes,
            "<div><h2>paragraph with <i>italic</i> and <b>bold</b></h2></div>"
        )
        
    def test_code_block_to_html_node(self):
        text = "```print('hello world!')```"
        nodes = markdown_to_html_node(text).to_html()
        self.assertEqual(
            nodes,
            "<div><pre><code>print('hello world!')</code></pre></div>"
        )
        
    def test_quote_block_to_html_node(self):
        text = ">This is a **bold** quote"
        nodes = markdown_to_html_node(text).to_html()
        self.assertEqual(
            nodes,
            "<div><blockquote>This is a <b>bold</b> quote</blockquote></div>"
        )
        
    def test_ul_block_to_html_node(self):
        text = '''* cool\n* list'''
        nodes = markdown_to_html_node(text).to_html()
        self.assertEqual(
            nodes,
            "<div><ul><li>cool</li><li>list</li></ul></div>"
        )
        
    def test_ol_block_to_html_node(self):
        text = '''1. cool\n2. list'''
        nodes = markdown_to_html_node(text).to_html()
        self.assertEqual(
            nodes,
            "<div><ol><li>cool</li><li>list</li></ol></div>"
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
if __name__ == "__main__":
    unittest.main()
