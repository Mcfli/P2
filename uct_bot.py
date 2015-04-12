import datetime
import random
from math import sqrt, log

class Node:

    def __init__(self, move = None, parent = None, state = None, last = None):
        self.move = move
        self.parentNode = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves()
        self.playerJustMoved = last

    def UCTSelectChild(self):
        m = sorted(self.children, key=lambda i: float(i.wins) / float(i.visits) + sqrt(2 * log(float(self.visits)) / float(i.visits)))[-1]
        return m

    def AddChild(self, m, s, last = None):
        new_node = Node(move=m, parent=self, state=s, last=last)
        self.untriedMoves.remove(m)
        self.children.append(new_node)
        return new_node

    def Update(self, result):
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return '[M:' + str(self.move) + ' W/V:' + str(self.wins) + '/' + str(self.visits) + ' U:' + str(self.untriedMoves) + ']'

    def TreeToString(self, indent):
        s = self.a(indent) + str(self)
        for c in self.children:
            s += c.TreeToString(indent + 1)

        return s

    def IndentString(self, indent):
        s = '\n'
        for i in range(1, indent + 1):
            s += '| '

        return s

    def ChildrenToString(self):
        s = ''
        for c in self.children:
            s += str(c) + '\n'

        return s


def think(rootstate, quip):
    rollouts = 0
    who = rootstate.get_whos_turn()
    range = {'blue': 'red',
     'red': 'blue'}
    rootnode = Node(state=rootstate, last=range[who])
    now = datetime.datetime.now()
    while True:
        node = rootnode
        state = rootstate.copy()

        # Select
        while node.untriedMoves == [] and node.children != []:
            node = node.UCTSelectChild()
            state.apply_move(node.move)

        # Expand
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            w = state.get_whos_turn()
            state.apply_move(m)
            node = node.AddChild(m, state, last=w)

        # Rollout
        while state.get_moves() != []:
            state.apply_move(random.choice(state.get_moves()))

        # Backpropagate
        score = state.get_score()
        rollouts += 1
        while node != None:
            node_score = score[node.playerJustMoved]
            node.Update(node_score)
            node = node.parentNode

        if datetime.datetime.now() - now > datetime.timedelta(seconds = 1):
            break
    quipText = "UCT rollouts per second: " + str(rollouts)
    quip(quipText)
    return sorted(rootnode.children, key=lambda i: i.visits)[-1].move
