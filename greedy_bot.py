import random

def think(rootstate, quip):
	for i in rootstate.get_moves():
		state = rootstate.copy()
		state.apply_move(i)
		if state.get_score()[rootstate.get_whos_turn()] > rootstate.get_score()[rootstate.get_whos_turn()]:
			return i

	return random.choice(rootstate.get_moves())
