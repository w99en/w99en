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


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
from game import Grid


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

        getAction takes a GameState and returns some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score=successorGameState.getScore()
        foodnumber=successorGameState.getNumFood()

        if successorGameState.hasFood(newPos[0],newPos[1]):
            score+=10
            #food grid
        min_food_distance = float('inf')
        all_food_distance = 0.0

        if(foodnumber!=0):   
            for  row in range(newFood.width):
                for col in range(newFood.height):
                    if newFood[row][col]==True: 
                        distance =pow( pow((newPos[0]-row)*(newPos[0]-row),1.0/2)+pow((newPos[1]-col)*(newPos[1]-col),1.0/2),1.0/2)  
                        all_food_distance += distance
                        min_food_distance=min(distance,min_food_distance)
        else:
            min_food_distance=0
            all_food_distance=0   

        all_ghost_scared = True
        min_ghost_distance =float('inf') 
        for ghostState in newGhostStates: 
            ghost_pos = ghostState.getPosition()  
            distance = pow((newPos[0]-ghost_pos[0])*(newPos[0]-ghost_pos[0]),1.0/2)+pow((newPos[1]-ghost_pos[1])*(newPos[1]-ghost_pos[1]),1.0/2) 
            min_ghost_distance = min(min_ghost_distance,distance)
            if ghostState.scaredTimer > 0:  
                score+=1
            else:
                all_ghost_scared=False

        score-=min_food_distance*0.5
        score-=all_food_distance/10
        if(min_ghost_distance<=4 and not all_ghost_scared):
            if(min_ghost_distance!=0):
                score-=100/min_ghost_distance
        if successorGameState.getCapsules():
            score+=3
        return score


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2',players_number=2):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.players_number=players_number


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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestaction="stop"
        max_value=float('-inf')
        for action in gameState.getLegalPacmanActions():
            if action == 'Stop':
                continue
            successor = gameState.generatePacmanSuccessor(action)
            value=self.minimax(successor, self.depth, 0)
            if value is not None and max_value < value:
               max_value = value
               bestaction = action       
        return bestaction

    def minimax(self,gameState,depth,term):  
        if depth>self.depth*2 or gameState.isWin() or gameState.isLose():  # 到达搜索深度或游戏结束  
            return self.evaluationFunction(gameState)  # 返回评估值和None（因为没有动作可选）
        if term==0:  # 当前是最大化者的回合  
            max_value = float('-inf')   
            legegalActions=gameState.getLegalActions()
            for action in legegalActions:  
                successor = gameState.generatePacmanSuccessor(action)  
                score= self.minimax(successor, depth +1,1-term)  # 切换到下一个玩家（最小化者）  
                max_value=max(score,max_value)   
            return max_value  
        else:  # 当前是最小化者的回合  
                # 如果有多个最小化者，需要遍历每个最小化者的所有可能行动，并选择其中得分最高的一个  
             #  存储所有最小化者行动后的最小得分
            min_value = float('inf')  
            for action in gameState.getLegalActions(1):  
                successor = gameState.generateSuccessor(1, action)  
                # 假设getNextAgentsIndices返回一个包含所有当前轮次的最小化者索引的列表  
                score = self.minimax(successor, depth+1, 1- term)  # 切换到下一个最大化者（可能是玩家或其他最小化者之后的下一个玩家）  
                min_value = min(score,min_value)  
                 # 存储得分和对应的行动  
        # 从所有最小化者的行动中选择得分最高的那个  
            return min_value
        
    # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        max_value=float('-inf')
        bestaction=[]
        for action in gameState.getLegalPacmanActions():
            alpha=float('-inf')
            beta=float('inf')            
            if action == 'Stop':
                continue
            successor = gameState.generatePacmanSuccessor(action)
            value=self.alphabeta_minimax(gameState=successor, depth=0,  term=0,alpha=alpha,beta=beta)
            if max_value < value:
               bestaction=[]
               max_value = value
               bestaction.append(action)
            elif max_value == value:
                bestaction.append(action)
            if max_value>alpha:
                alpha=max_value
        return random.choice(bestaction)

    def alphabeta_minimax(self,gameState,depth,term,alpha,beta):  
        if depth >self.depth or gameState.isWin() or gameState.isLose():  # 到达搜索深度或游戏结束  
            return self.evaluationFunction(gameState)  # 返回评估值和None（因为没有动作可选）
        if term==0:  # 当前是最大化者的回合  
            max_value = float('-inf')   
            for action in gameState.getLegalActions():  
                successor = gameState.generatePacmanSuccessor(action)  
                score= self.alphabeta_minimax(successor, depth +1,1-term,alpha,beta)  # 切换到下一个玩家（最小化者）  
                if score is not None:  
                    max_value = max(score,max_value)  
                    if max_value > beta: 
                        return max_value
                    alpha = max(alpha,max_value)                  
            return max_value  
        else:  # 当前是最小化者的回合  
                # 如果有多个最小化者，需要遍历每个最小化者的所有可能行动，并选择其中得分最高的一个  
             #  存储所有最小化者行动后的最小得分
            score = []
            min_value = float('inf')  
            for action in gameState.getLegalActions(1):  
                successor = gameState.generateSuccessor(1, action)  
                # 假设getNextAgentsIndices返回一个包含所有当前轮次的最小化者索引的列表  
                score.append(self.alphabeta_minimax(successor, depth, (term+1)%gameState.getNumAgents(),alpha,beta))  # 切换到下一个最大化者（可能是玩家或其他最小化者之后的下一个玩家）  
                if score is not None:
                    min_value = min(score,min_value)  
                    if min_value < alpha: 
                        return min_value
                    beta = min(beta,min_value)  
                 # 存储得分和对应的行动  
        # 从所有最小化者的行动中选择得分最高的那个  
            return min_value
    


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
