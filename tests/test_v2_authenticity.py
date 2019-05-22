from V2.authenticity_node import AuthenticityNode
from V2.certificate import Certificate
from V2.identity import Identity
from utility.crypto_helper import generate_key_pair, sign
import unittest


class TestAuthenticity(unittest.TestCase):

    def test_functional(self):
        node_a = AuthenticityNode("a")
        node_b = AuthenticityNode("b")
        message_a = node_a.send()
        message_b = node_b.send()
        node_b.receive(message_a)
        node_a.receive(message_b)

    def test_authenticity(self):
        node_a = AuthenticityNode("a")
        node_b = AuthenticityNode("b")
        message_a = node_a.send()
        key_pair = generate_key_pair()
        invalid_identity = Identity(5, key_pair.public)
        invalid_signature = sign(invalid_identity, key_pair.private)
        invalid_certificate = Certificate(invalid_signature, invalid_identity)
        message_a.content.certificate = invalid_certificate
        self.assertRaises(ValueError, node_b.receive, message_a)

if __name__ == '__main__':
    unittest.main()