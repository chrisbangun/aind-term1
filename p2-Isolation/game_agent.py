"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):

    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    blank_spaces_left = len(game.get_blank_spaces())

    def number_of_moves():
        """
        heuristic method used in the beginning of the game
        simply count the number of legal moves
        :return:
        """
        if game.is_loser(player):
            return float("-inf")
        if game.is_winner(player):
            return float("inf")
        return float(len(game.get_legal_moves(player)))

    def open_area():
        """
        heuristic method used in the middle of the game
        return the diff between the number of legal moves
        for both players
        :return:
        """
        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        my_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

        return float(my_moves - opp_moves)

    def longest_path():
        """
        heuristic method when reaching the end of game
        this method computationally more expensive from the previous two heuristics
        :return:
        """
        def longest_path_internal(board, _player):
            longest = 0
            for move in board.get_legal_moves(_player):
                new_board = board.forecast_move(move)
                path_length = longest_path_internal(new_board, _player) + 1
                if path_length > longest:
                    longest = path_length
                if longest > 20:  # try to avoid going more than 20 moves deep
                    break
            return float(longest)

        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        player1_longest_path = longest_path_internal(game, player)
        player2_longest_path = longest_path_internal(game, game.get_opponent(player))

        # it is player1 turn,
        # if both player have the same longest path
        # or player1 longest path is 0
        # return -inf, which means player1 is lost
        if player1_longest_path == player2_longest_path or player1_longest_path == 0:
            return float("-inf")

        if player1_longest_path > player2_longest_path:
            return float("inf")
        return float("-inf")

    if blank_spaces_left < 20:
        # End Game
        return longest_path()
    elif blank_spaces_left <= 42:
        # Middle Game
        return open_area()
    else:
        # Beginning Game
        return number_of_moves()


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        best_move = (-1, -1)

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # if there is no legal moves
        # return (-1, -1)
        if not legal_moves:
            return best_move

        depth = 0
        # Try to get the search method (minimax or alphabeta)
        try:
            search_method = getattr(self, self.method)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                                      format(self.__class__.__name__, self.method))

        if not self.iterative:
            return search_method(game, depth+1)[1]

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            while True:
                best_score = -float("inf")
                score, move = search_method(game, depth)
                if score > best_score:
                    best_score = score
                    best_move = move
                depth += 1

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0 or not game.get_legal_moves():
            if maximizing_player:
                player = game.active_player
            else:
                player = game.inactive_player
            return self.score(game, player), None

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if maximizing_player:
            v = -float("inf")
            for move in legal_moves:
                score = self.minimax(game.forecast_move(move), depth - 1, False)[0]
                if score > v:
                    v = score
                    best_move = move
            return v, best_move
        else:
            v = float("inf")
            for move in legal_moves:
                score = self.minimax(game.forecast_move(move), depth - 1, True)[0]
                if score < v:
                    v = score
                    best_move = move
            return v, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0 or not game.get_legal_moves():
            if maximizing_player:
                player = game.active_player
            else:
                player = game.inactive_player
            return self.score(game, player), None

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if maximizing_player:
            v = -float("inf")
            for move in legal_moves:
                v = max(v, self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, False)[0])
                if v >= beta:  # Pruning
                    return v, move
                if v > alpha:
                    alpha = v
                    best_move = move
            return alpha, best_move
        else:
            v = float("inf")
            for move in legal_moves:
                v = min(v, self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, True)[0])
                if v <= alpha:  # Pruning
                    return v, move
                if v < beta:
                    beta = v
                    best_move = move
            return beta, best_move
