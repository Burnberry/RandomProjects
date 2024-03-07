from Code.Util.Node import Node


class Path:
    def __init__(self, positions):
        self.start = Node(positions.pop(0))
        prev = self.start

        for pos in positions:
            node = Node(pos)
            node.chain(prev)
            prev = node

        self.end = prev

    def get_positions(self):
        node = self.start
        positions = [node.position]
        while node.child:
            node = node.child
            positions.append(node.position)

        return positions
