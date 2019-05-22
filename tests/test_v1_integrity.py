from V1.integrity_node import IntegrityNode
import unittest


class TestIntegrity(unittest.TestCase):

    def test_functional(self):
        node_a = IntegrityNode(1, "a")
        node_b = IntegrityNode(2, "b")
        message_a = node_a.send()
        message_b = node_b.send()
        node_b.receive(message_a)
        node_a.receive(message_b)

    def test_integrity(self):
        node_a = IntegrityNode(1, "a")
        node_b = IntegrityNode(2, "b")
        message = node_a.send()
        message.content.this_field_should_not_be_here = "man in the middle was here ..."
        self.assertRaises(ValueError, node_b.receive, message)

if __name__ == '__main__':
    unittest.main()