import datetime
import random
from math import sqrt, log
from uct_bot import Node

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
        depth = 0
        while state.get_moves() != [] and depth < 5:
            state.apply_move(random.choice(state.get_moves()))
            depth += 1

        # Backpropagate
        score = state.get_score()
        rollouts += 1
        while node != None:
            node_score = score[node.playerJustMoved]
            node.Update(node_score)
            node = node.parentNode

        if datetime.datetime.now() - now > datetime.timedelta(seconds = 1):
            break
    quipText = "Fast rollouts per second: " + str(rollouts)
    quip(quipText)
    return sorted(rootnode.children, key=lambda i: i.visits)[-1].move
