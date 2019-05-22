from vanilla.simulator import Simulator
from vanilla.factory import Factory

factory = Factory(10)
Simulator.run(
    [
        factory.create("a"),
        factory.create("a"),
        factory.create("a"),
        factory.create("b"),
        factory.create("b"),
        factory.create("c"),
        factory.create("c"),
        factory.create("c"),
        factory.create("b"),
        factory.create("b")
    ],
    0.7,
    100,
    True
)
