from V2.authenticity_node import AuthenticityNode
from V2.certificate import Certificate
from V2.identity import Identity
from utility.crypto_helper import generate_key_pair, sign
from V3.slmp_server import SLMPServer
from V3.slmp_client import SLMPClient
import unittest


class TestCentralizedSLMP(unittest.TestCase):

    def test_functional(self):
        client0 = SLMPClient("a", 0)
        client1 = SLMPClient("a", 1)
        client2 = SLMPClient("b", 2)
        client3 = SLMPClient("b", 3)
        client4 = SLMPClient("c", 4)
        server = SLMPServer()
        server.join(client0.send())
        server.join(client1.send())
        server.join(client2.send())
        server.join(client3.send())
        server.join(client4.send())
        messages = server.send()
        for message in messages:
            view_broadcast = message.content
            follower_ids = view_broadcast.follower_ids
            if view_broadcast.context == "a":
                self.assertEqual(2, follower_ids)
                self.assertTrue(0 in follower_ids)
                self.assertTrue(1 in follower_ids)
            elif view_broadcast.context == "b":
                self.assertEqual(2, follower_ids)
                self.assertTrue(2 in follower_ids)
                self.assertTrue(3 in follower_ids)
            elif view_broadcast.context == "c":
                self.assertEqual(1, follower_ids)
                self.assertTrue(4 in follower_ids)

if __name__ == '__main__':
    unittest.main()