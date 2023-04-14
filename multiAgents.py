# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
student id: 202005881
surname: Joseph
initials: TWJ
programme code: BSc Computer Science
"""

from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


numStatesGenerated = 0
numPrune = 0


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
        Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
            Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        PACMAN = 0
        GHOSTS = range(1, gameState.getNumAgents())
        INFINITY = 1e308

        def TERMINAL(state, depth):
            return state.isWin() or state.isLose() or depth < 0

        def A_B_SEARCH(state, depth):

            actions = filter(lambda a: a != Directions.STOP,
                             state.getLegalActions(PACMAN))
            results = [(action, MIN_VALUE(state.generateSuccessor(
                PACMAN, action), depth, -INFINITY, INFINITY)) for action in actions]
            action, value = max(results, key=lambda t: t[1])

            return action, value

        def MIN_VALUE(state, depth, a, b):
            # indicate numPrine and numStatesGenerated are global variables
            global numPrune, numStatesGenerated

            numStatesGenerated = numStatesGenerated + 1
            if TERMINAL(state, depth):
                return self.evaluationFunction(state)

            # create array to store all the possible actions the ghosts can make
            ghost_successors = []

            # add every possible action the ghosts can make to the array
            for ghost in GHOSTS:
                for ghost_action in state.getLegalActions(ghost):
                    ghost_successors.append(
                        (state.generateSuccessor(ghost, ghost_action), ghost_action, self.evaluationFunction(state)))

            # order all the possible actions the ghosts can take in ascending order
            ghost_successors.sort(reverse=False, key=lambda a: a[2])

            # find action that will give us the lowest possible value
            while ghost_successors:
                b = min(b, MAX_VALUE(ghost_successors[0][0], depth-1, a, b))

                # prune actions that are unlikely to be chosen
                if b <= a:
                    numPrune = numPrune + 1
                    return b
                ghost_successors = ghost_successors[1:]

            return b

        def MAX_VALUE(state, depth, a, b):
            # indicate numPrine and numStatesGenerated are global variables
            global numPrune, numStatesGenerated

            numStatesGenerated = numStatesGenerated + 1
            if TERMINAL(state, depth):
                return self.evaluationFunction(state)

            # filter the list of actions that pacman can take to avoid the STOP action
            actions_pacman = filter(lambda a: a != Directions.STOP,
                                    state.getLegalActions(PACMAN))

            # create array to store the possible moves pacman can make
            pacman_successors = []

            # add every possible action pacman can make to the array
            for action_pacman in actions_pacman:
                pacman_successors.append(
                    (state.generateSuccessor(PACMAN, action_pacman), action_pacman, self.evaluationFunction(state)))

            # order all the possible actions pacman can take in descending order based on score
            pacman_successors.sort(reverse=True, key= lambda a: a[2])

            # find the action that gives us the largest possible value
            while pacman_successors:
                a = max(a, MIN_VALUE(pacman_successors[0][0], depth-1, a, b))

                # prune actions that are unlikely to be taken
                if a >= b:
                    numPrune = numPrune + 1
                    return a
                pacman_successors = pacman_successors[1:]
            return a

        action, value = A_B_SEARCH(gameState, self.depth)

        # YOUR CODE HERE: print required output here
        print "Number of State Generated: ", numStatesGenerated
        print "Number of prunings ", numPrune

        # will output and append results to a new external file
        output = open('partAoutput.txt', 'a')
        # converts variables to strings
        stateGenerated = repr(numStatesGenerated)
        pruns = repr(numPrune)
        # writes to external file
        output.write("Number of State Generated: " + stateGenerated + "\n")
        output.write("Number of prunings: " + pruns + "\n")
        output.close()

        return action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
