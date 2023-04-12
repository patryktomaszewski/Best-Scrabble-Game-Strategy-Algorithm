from collections import defaultdict


class Node:
    def __init__(self):
        self.edges = defaultdict(Node)
        self.final = False


class DAWG:
    def __init__(self):
        self.root = Node()
        self.counter = 0

    def add_word(self, word):
        node = self.root
        for char in word:
            node = node.edges[char]
        if not node.final:
            node.final = True
            node.number = self.counter
            self.counter += 1

    def compress(self):
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            edges = sorted(node.edges.keys())
            for char in edges:
                child = node.edges[char]
                if len(child.edges) == 1 and not child.final:
                    node.edges[char] = list(child.edges.values())[0]
                else:
                    queue.append(child)


    def lookup(self, word):
        node = self.root
        for char in word:
            if char not in node.edges.keys():
                return None
            node = node.edges[char]
        return node


    def has_word(self, word):
        node = self.lookup(word)
        if node is None:
            return False
        return node.final

    def __len__(self):
        return self.counter
