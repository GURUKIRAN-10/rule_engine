class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def is_operand(self):
        return self.node_type == "operand"

    def is_operator(self):
        return self.node_type == "operator"
