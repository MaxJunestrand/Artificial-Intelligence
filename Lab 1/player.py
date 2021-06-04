#!/usr/bin/env python3
import random
import time
from operator import itemgetter

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

# Global vars
start_time = 0
transposition_table = {}

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)
            node.compute_and_get_children() # Initialize game tree; also returns children.

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        return None

    
    def search_best_next_move(self, model, initial_tree_node):
        # Global vars
        global start_time
        start_time = current_milli_time()
        global transposition_table

        # Local variables
        best_move = 0
        best_val = -99999
        depth = 0
        children_nodes =  initial_tree_node.compute_and_get_children()
        # Simple move order
        # Best nodes will always be sorted given how we add elements to it. So we start with best option.
        best_nodes = []
        while not abort():
              depth = depth + 1
              #print("Depth: " + str(depth))
              # make it a set to remove duplicates
              for child_node in set(best_nodes + children_nodes):
                  move_val = minimax(child_node, depth, -99999, 99999, 1)
                  transposition_table[child_node.state] = move_val
                  if move_val > best_val:
                      best_val = move_val
                      best_move = child_node.move

                      best_nodes.append(child_node)

        return ACTION_TO_STR[best_move]


def current_milli_time():
    return round(time.time() * 1000)

def abort():
    global start_time
    return (current_milli_time() - start_time) > 45

def minimax(node, depth, alfa, beta, player):
    global transposition_table
    # Check trans table
    state = node.state
    if state in transposition_table:
        #print("HEJ NU ANVÄNDS JAG!")
        #print(str(len(transposition_table)))
        return transposition_table[state]

    
    if abort() or depth == 0:
        v = heuristic_value(state)
        #v = simple_heuristic(state)
    elif player == 0:
        childrenNodes =  node.compute_and_get_children()
        v = -99999
        for child in childrenNodes:                
            v = max(v, minimax(child, depth-1, alfa, beta, 1))
            alfa = max(alfa, v)
            if beta <= alfa:
                break # Beta Prune
    else: # player B
        childrenNodes =  node.compute_and_get_children()
        v = 99999
        for child in childrenNodes:                
            v = min(v, minimax(child, depth-1, alfa, beta, 0))
            beta = min(beta, v)
            if beta <= alfa:
                break # Alfa Prune
    return v


def simple_heuristic(state):
    s = state.get_player_scores()
    return s[0] - s[1]

# Function for creating a heuristic value to a state, currently that is a value for the current placement of player hook
# Takes state and returns an integer
# This function calculates a value to a position on the 20x20 board by calculating the distance to each fish polynomically, but also making it more valuable
# to be really close to a fish.
# Example on WolframAlpha: https://www.wolframalpha.com/input/?i=z+%3D+%28x%5E2+%2B+y%5E2%29%5E%281%2F10%29+%2B+4%28%28x-2%29%5E2+%2B+%28y-2%29%5E2%29%5E%281%2F10%29
# Higher value fish of course has a higher effect
def heuristic_value(state):
    fishPosDict = state.get_fish_positions() #get dictionary of fishes pos, key:fish number   data: fish position (tuple positions in x and y)
    fishPointDict = state.get_fish_scores()  #get dictionary of fishes scores, key:fish number   data: fish point
    hookPosDict = state.get_hook_positions() #get dictionary of hook pos, key:hook number   data: hook position        hook 0: player hook, hook 1: AI hook

    heurValue = 0

    if len(fishPosDict) == 0: #if there is no fish we only count points
        return 999999

    h0 = hookPosDict.get(0)[0] #player1 hook x pos
    h1 = hookPosDict.get(1)[0] #player2 hook x pos    
    for key, value in fishPosDict.items():
        # calulate player 1s position to fish
        fishXPos =  value[0]       #fish x pos
        
        xDiff = xDistance(h0,h1,fishXPos)
        yDiff = hookPosDict.get(0)[1] -value[1]

        z = pow((pow(xDiff,2)+pow(yDiff,2)),0.2)  # This looks like this: ((x)^2 + (y)^2)^(1/10)
        z = fishPointDict.get(key) * z   # we multiply by the points on the fish.
        heurValue -= z

        hookedFishPlayer = state.get_caught()[0] #fishes on the hook also have a value
        if hookedFishPlayer is not None:
            heurValue += hookedFishPlayer

        # Substract players 2
        xDiff = xDistance(h1,h0,fishXPos)

        yDiff = hookPosDict.get(1)[1] -value[1]
        z = pow((pow(xDiff,2)+pow(yDiff,2)),0.2)  # This looks like this: ((x-2)^2 + (y-2)^2)^(1/10)
        z = fishPointDict.get(key) * z   # we multiply by the points on the fish.
        heurValue += z

        hookedFishAI = state.get_caught()[1] #fishes on the hook also have a value
        if hookedFishAI is not None:
            heurValue -= hookedFishAI

    return heurValue

#h0 is your hook xpos, h1 is enemy hook xpos, fishXPos is the fish's xpos
def xDistance(h0, h1, fishXPos):
    if h0 < h1 and h1 < fishXPos:   #if player2 hook between, and you have to go left
        xDiff = h0 + (20 - fishXPos) 
    elif fishXPos < h1 and h1 < h0: #if player2 hook between, and you have to go right
        xDiff = fishXPos + (20-h0) 
    else:                           #if no fishy business
        xDiff = h0 - fishXPos
    return xDiff
