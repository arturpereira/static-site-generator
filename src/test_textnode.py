import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self): 
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_url_is_none(self): 
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_different_texttype_not_eq(self): 
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
        
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_wrong_type(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("Value", TextType.INVALID, None))
            
    def test_text_node_to_html_node_type_normal(self):
        node = text_node_to_html_node(TextNode("Value", TextType.TEXT, None))
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Value")
        self.assertEqual(node.to_html(), "Value")
        
    def test_text_node_to_html_node_type_bold(self):
        node = text_node_to_html_node(TextNode("Value", TextType.BOLD, None))
        self.assertEqual(node.to_html(), "<b>Value</b>")
        
    def test_text_node_to_html_node_type_italic(self):
        node = text_node_to_html_node(TextNode("Value", TextType.ITALIC, None))
        self.assertEqual(node.to_html(), "<i>Value</i>")
        
    def test_text_node_to_html_node_type_code(self):
        node = text_node_to_html_node(TextNode("Value", TextType.CODE, None))
        self.assertEqual(node.to_html(), "<code>Value</code>")
        
    def test_text_node_to_html_node_type_link(self):
        node = text_node_to_html_node(TextNode("Value", TextType.LINK, url="google.com"))
        self.assertEqual(node.to_html(), '<a href="google.com">Value</a>')
        
    def test_text_node_to_html_node_type_image(self):
        node = text_node_to_html_node(TextNode("Value", TextType.IMAGE, url="google.com"))
        self.assertEqual(node.to_html(), '<img src="google.com" alt="Value"></img>')

if __name__ == "__main__":
    unittest.main()
    
