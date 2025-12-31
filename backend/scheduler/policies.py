def can_schedule(node):
    return node.cpu < 30 and node.ram < 50
