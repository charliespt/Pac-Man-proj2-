# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # print "Action: ", legalMoves[chosenIndex]
        # successorGameState = gameState.generatePacmanSuccessor(legalMoves[chosenIndex])
        # print "Pacman Position: ", successorGameState.getPacmanPosition()
        # print "Ghost Position: ", successorGameState.getGhostPositions()
        # print "Food Position \n", successorGameState.getFood()
        # print "Score", self.evaluationFunction(gameState, legalMoves[chosenIndex]) 
        # minDisCurrent  = 9999
        # for food in gameState.getFood().asList():
        #   if (util.manhattanDistance(gameState.getPacmanPosition(),food) < minDisCurrent):
        #     minDisCurrent = util.manhattanDistance(gameState.getPacmanPosition(),food)
        # minDisNew = 9999
        # for food in successorGameState.getFood().asList():
        #   if (util.manhattanDistance( successorGameState.getPacmanPosition(),food) < minDisNew):
        #     minDisNew = util.manhattanDistance( successorGameState.getPacmanPosition(),food)
        # print "Old Min", minDisCurrent
        # print "New Min", minDisNew
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        def dis1(pos):
          return ((pos[0]-1,pos[1]),(pos[0],pos[1]-1),(pos[0]+1,pos[1]),(pos[0],pos[1]+1))
        def dis2(pos):
          return ((pos[0]-2,pos[1]),(pos[0],pos[1]-2),(pos[0]+2,pos[1]),(pos[0],pos[1]+2),(pos[0]-1,pos[1]-1),(pos[0]-1,pos[1]+1),(pos[0]+1,pos[1]-1),(pos[0]+1,pos[1]+1))
        ghostsPos =  successorGameState.getGhostPositions()
        evalScore = 0
        for p in ghostsPos:
          if (p in dis1(newPos)):
            return -200
          if (p in dis2(newPos)):
            evalScore -= 200
        if currentGameState.getFood().count() > newFood.count():
          evalScore+=50
        minDisCurrent = 9999
        for food in currentGameState.getFood().asList():
          if (util.manhattanDistance(currentGameState.getPacmanPosition(),food) < minDisCurrent):
            minDisCurrent = util.manhattanDistance(currentGameState.getPacmanPosition(),food)
        minDisNew = 9999
        for food in newFood.asList():
          if (util.manhattanDistance(newPos,food) < minDisNew):
            minDisNew = util.manhattanDistance(newPos,food)
        if minDisCurrent < minDisNew:
          evalScore -= 20
        if minDisCurrent > minDisNew:
          evalScore += 20
        return evalScore

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        def getScore(state,depth,agentIndex): 
          # print "Depth: ",depth
          # print "Agent Index: ",agentIndex
          actions = state.getLegalActions(agentIndex)
          # print "Actions: ",actions
          if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          scores = []
          for action in  actions:
            if (depth == 1 and agentIndex == gameState.getNumAgents()-1):
              scores += [self.evaluationFunction(state.generateSuccessor(agentIndex, action))]
            elif (agentIndex == gameState.getNumAgents()-1):
              scores += [getScore(state.generateSuccessor(agentIndex, action),depth-1,0)]
            else:
              scores += [getScore(state.generateSuccessor(agentIndex, action),depth,agentIndex+1)]
          if agentIndex == 0:
            return max(scores)
          else:
            return min(scores)

        actions = gameState.getLegalActions(0)
        scores = []
        for action in actions:
          scores += [getScore(gameState.generateSuccessor(0, action),self.depth,1)]
        return actions[scores.index(max(scores))]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBeta(state,depth,alpha,beta,agentIndex): 
          #print depth,alpha,beta,agentIndex
          actions = state.getLegalActions(agentIndex)
          if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          scores = []
          for action in  actions:
            if (depth == 1 and agentIndex == gameState.getNumAgents()-1):
              rv = self.evaluationFunction(state.generateSuccessor(agentIndex, action))
              scores += [rv]
              if agentIndex == 0:
                alpha = max(rv,alpha)
              else:
                beta = min(rv,beta)
            elif (agentIndex == gameState.getNumAgents()-1):
              rv = alphaBeta(state.generateSuccessor(agentIndex, action),depth-1,alpha,beta,0)
              scores += [rv]
              beta = min(rv,beta)
            else:
              rv = alphaBeta(state.generateSuccessor(agentIndex, action),depth,alpha,beta,agentIndex+1)
              scores += [rv]
              if agentIndex == 0:
                alpha = max(rv,alpha)
              else:
                beta = min(rv,beta)
            if beta < alpha:
              break
          if agentIndex == 0:
            return max(scores)
          else:
            return min(scores)

        alpha = -99999
        beta = 99999
        actions = gameState.getLegalActions(0)
        scores = []
        for action in actions:
          val = alphaBeta(gameState.generateSuccessor(0, action),self.depth,alpha,beta,1)
          if val > alpha:
            move = action
            alpha = val
          if beta < alpha:
            break
        return move

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
        def getScore(state,depth,agentIndex): 
          # print "Depth: ",depth
          # print "Agent Index: ",agentIndex
          actions = state.getLegalActions(agentIndex)
          # print "Actions: ",actions
          if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          scores = []
          for action in  actions:
            if (depth == 1 and agentIndex == gameState.getNumAgents()-1):
              scores += [self.evaluationFunction(state.generateSuccessor(agentIndex, action))]
            elif (agentIndex == gameState.getNumAgents()-1):
              scores += [getScore(state.generateSuccessor(agentIndex, action),depth-1,0)]
            else:
              scores += [getScore(state.generateSuccessor(agentIndex, action),depth,agentIndex+1)]
          if agentIndex == 0:
            return max(scores)
          else:
            return float(sum(scores))/len(scores)

        actions = gameState.getLegalActions(0)
        scores = []
        for action in actions:
          scores += [getScore(gameState.generateSuccessor(0, action),self.depth,1)]
        return actions[scores.index(max(scores))]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    ghostsPosition = currentGameState.getGhostPositions()
    food = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    dis=util.manhattanDistance
    score = 0
    for g in ghostStates:
      pos = g.getPosition()
      if dis(pacmanPosition,pos) < 10:
        if g.scaredTimer > 0:
          score -= (dis(pacmanPosition,pos)-g.scaredTimer)*500
        else:
          score += dis(pacmanPosition,pos)*200
    score -= food.count()*2
    # minDis = 99999
    # for f in food.asList():
    #   if (dis(pacmanPosition,f) < minDis):
    #     minDis = dis(pacmanPosition,f)
    # score -= minDis




    return score


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

