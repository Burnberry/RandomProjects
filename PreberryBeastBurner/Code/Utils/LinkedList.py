class Node:
    def __init__(self, obj, prev=None, next=None):
        self.obj = obj
        self.prev = prev
        self.next = next


class CircleLinkedList:
    def __init__(self, objects):
        nodes = [Node(obj) for obj in objects]
        self.length = len(nodes)
        for i in range(self.length):
            node = nodes[i]
            node.prev = nodes[(i-1)%self.length]
            node.next = nodes[(i+1)%self.length]

        self.currentNode = nodes[0]

    def next(self):
        self.currentNode = self.currentNode.next
        return self.currentNode.obj

    def prev(self):
        self.currentNode = self.currentNode.prev
        return self.currentNode.obj

    def remove(self):
        if self.length == 1:
            # Empty list
            self.currentNode = None
            self.length = 0
            print("Empty L list")
            return
        if self.length == 0:
            # Incorrect usage
            print("Empty L list")
            return
        else:
            prev_node, next_node = self.currentNode.prev, self.currentNode.next
            prev_node.next = next_node
            next_node.prev = prev_node
            self.length -= 1
            return

    def remove_node(self, obj):
        if self.length == 0:
            # Incorrect usage
            print("Empty L list")
            return
        elif self.currentNode.obj is obj:
            return self.remove()
        else:
            cur_node = self.currentNode
            self.next()
            while self.currentNode is not cur_node:
                if self.currentNode.obj is obj:
                    self.remove()
                    break
                self.next()
            self.currentNode = cur_node
    def add(self, obj, move=0):
        new_node = Node(obj)

        if self.length == 0:
            new_node.prev = new_node
            new_node.next = new_node
            prev_node = new_node
        elif self.length == 1:
            new_node.prev = self.currentNode
            new_node.next = self.currentNode
            prev_node = self.currentNode
            prev_node.prev = new_node
            prev_node.next = new_node
        else:
            prev_node, next_node = self.currentNode, self.currentNode.next
            new_node.prev = prev_node
            new_node.next = next_node

            prev_node.next = new_node
            next_node.prev = new_node

        self.currentNode = new_node
        self.move(move)

        self.currentNode = prev_node

        self.length += 1

    def move(self, move, follow=False):
        if move == 0:
            return

        node = self.currentNode
        next_cur_node = node

        prev_node, next_node = self.currentNode.prev, self.currentNode.next
        prev_node.next = next_node
        next_node.prev = prev_node

        if not follow:
            next_cur_node = prev_node

        for i in range(move):
            self.next()

        prev_node, next_node = self.currentNode, self.currentNode.next
        prev_node.next = node
        next_node.prev = node

        self.currentNode = next_cur_node
