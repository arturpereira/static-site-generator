import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
                "div",
                "Hello, world!",
                None,
                {"class": "greeting", "href": "https://boot.dev"}
            )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
                "p",
                "What a strange world",
                None,
                {"class": "primary"},
            )
        self.assertEqual(
                node.__repr__(),
                "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",)


    def test_tag_is_none(self): 
        node = HTMLNode(value="Value")
        self.assertEqual(node.tag, None)
    
    def test_to_html_no_children(self):
        node = LeafNode(
                "div",
                "Hello, world!",
                {"class": "greeting", "href": "https://boot.dev"}
            )
        self.assertEqual(
            node.to_html(),
            '<div class="greeting" href="https://boot.dev">Hello, world!</div>',
        )
    
    def test_to_html_no_tag(self): 
        node = LeafNode(tag=None, value="Value")
        self.assertEqual(node.to_html(), "Value")
        
    def test_parent_no_tag_raises(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_children_raises(self):
        node = ParentNode(
            "p",
        )
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_parent_one_child(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b></p>")
        
    def test_parent_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_nested_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text</p>")
        
    def test_nested_parent_with_no_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
    
