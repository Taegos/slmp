from vanilla.utility.debugger import Debugger
from tabulate import tabulate
import random
import functools

class Simulator:
    @classmethod
    def run(cls, nodes, packet_loss_chance, round_count, debug=True):
        Debugger.set_enabled(debug)
        Debugger.log("Initial states:")
        cls.__print_node_states(nodes)
        current_round = 1
        while current_round <= round_count:
            Debugger.log("Round: " + str(current_round))
            messages = cls.__collect_messages(nodes)
            cls.__publish_messages(messages, nodes, packet_loss_chance)
            cls.__act_all(nodes)
            cls.__print_node_states(nodes)
            current_round += 1
            Debugger.log("")
        Debugger.log("Simulation Complete")

    @classmethod
    def __collect_messages(cls, nodes):
        messages = []
        for node in nodes:
            message = node.send()
            if message is not None:
                messages.append(message)
        return messages

    @classmethod
    def __publish_messages(cls, messages, nodes, packet_loss_chance):
        for message in messages:
            content = message.content
            for node in nodes:
                if content.sender_id == node.get_id():
                    continue
                if random.random() <= packet_loss_chance:
                    # print("Message from {0} to {1} was lost due to packet loss.".
                    # format(message.sender_id, vehicle.id))
                    continue
                if message.type == "VIEW_BROADCAST" or \
                   content.receiver_id == node.get_id():
                    node.receive(message)

    @classmethod
    def __act_all(cls, nodes):
        for vehicle in nodes:
            vehicle.act()

    @classmethod
    def __print_node_states(cls, nodes):
        states = []
        for vehicle in nodes:
            states.append(vehicle.as_displayable())
        states = sorted(states, key=functools.cmp_to_key(cls.__cmp))
        Debugger.log(tabulate(states, headers="keys", tablefmt="grid"))

    @classmethod
    def __cmp(cls, a, b):
        if a["context"] > b["context"]:
            return 1
        return -1

