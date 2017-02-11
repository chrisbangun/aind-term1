"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import sys
import math
import random

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def position_value(game, player):
    """

    :param game:
    :param player:
    :return:
    """
    def distance_to_center(_player):
        player_location = game.get_player_location(_player)
        center_x = (game.width - 1) / 2
        center_y = (game.height - 1) / 2
        return math.sqrt(math.pow(center_x - player_location[0], 2) + math.pow(center_y - player_location[1], 2))

    my_position = len(game.get_legal_moves(player)) - distance_to_center(player)
    opp_position = len(game.get_legal_moves(game.get_opponent(player))) - distance_to_center(game.get_opponent(player))

    if my_position > opp_position:
        return (3 * my_position / 2) - (opp_position / 2)
    return (my_position / 2) - (3 * opp_position / 2)


def longest_path(game, player):
    """
    count max number of moves a player has
    assume other player doesn't move
    :param game:
    :param player:
    :return:
    """

    def longest_path_internal(board, _player):
        longest = 0
        legal_moves = board.get_legal_moves(_player)
        for move in legal_moves:
            new_board = board.forecast_move(move)
            path_length = longest_path_internal(new_board, _player) + 1
            if path_length > longest:
                longest = path_length
            if longest > 10:
                break
        return longest

    player1_longest_path = longest_path_internal(game, player)
    player2_longest_path = longest_path_internal(game, game.get_opponent(player))

    if player1_longest_path <= player2_longest_path or player1_longest_path == 0:
        return float("-inf")
    return float("inf")


def get_open_area(game, player):

    def get_surrounding_space(__space):
        row = __space[0]
        col = __space[1]
        lower_row = row - 1
        higher_row = row + 1
        lower_col = col - 1
        higher_col = col + 1
        surrounding_spaces = []
        if row > 0:
            surrounding_spaces.append(tuple([lower_row, col]))
            if col > 0:
                surrounding_spaces.append(tuple([lower_row, lower_col]))
                surrounding_spaces.append(tuple([row, lower_col]))
            if col < game.width:
                surrounding_spaces.append(tuple([lower_row, higher_col]))
                surrounding_spaces.append(tuple([row, higher_col]))

        if row < game.height:
            surrounding_spaces.append(tuple([higher_row, col]))
            if col > 0:
                surrounding_spaces.append(tuple([higher_row, lower_col]))
            if col < game.width:
                surrounding_spaces.append(tuple([higher_row, higher_col]))

        return surrounding_spaces

    initial_loc = game.get_player_location(player)
    to_examine = [initial_loc]
    seen = set()
    accessible = set()
    blank_spaces = game.get_blank_spaces()
    while len(to_examine) > 0:
        space = to_examine.pop(0)
        for _space in get_surrounding_space(space):
            if _space in seen:
                continue
            seen.add(_space)
            if _space in blank_spaces:
                accessible.add(_space)
                to_examine.append(_space)
    return accessible


def mid_game_eval(game, player):

    def center_score(player_loc):
        center = game.width / 2
        return - abs(player_loc[0] - center) - abs(player_loc[1] - center)

    my_cords = game.get_player_location(player)
    opp_cords = game.get_player_location(game.get_opponent(player))

    height = abs(my_cords[0] - opp_cords[0])
    width = abs(my_cords[1] - opp_cords[1])

    my_legal_moves = len(game.get_legal_moves(player))
    opp_legal_moves = len(game.get_legal_moves(game.get_opponent(player)))
    mobility_score = my_legal_moves - opp_legal_moves
    proximity_to_center = center_score(my_cords) - center_score(opp_cords)
    return 3 * mobility_score + proximity_to_center


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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return mid_game_eval(game, player)
    # board_size = game.width * game.height
    # blank_spaces_left = len(game.get_blank_spaces())
    # if blank_spaces_left < 40:
    # if blank_spaces_left <= 10:
    #     return longest_path(game, player)

    #     my_open_area = get_open_area(game, player)
    #     opp_open_area = get_open_area(game, game.get_opponent(player))
    #     if len(my_open_area) == 0:
    #         return float("-inf")
    #     if len(opp_open_area) == 0:
    #         return float("inf")
    #     if not my_open_area.intersection(opp_open_area):
    #         return longest_path(game, player)
    #     return mid_game_eval(game, player)
        # float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(
        # game.get_opponent(player))))
        # return mid_game_eval(game, player)
    # return mid_game_eval(game, player)
    # else:
        # my_open_area = get_open_area(game, player)
        # opp_open_area = get_open_area(game, game.get_opponent(player))
        # if len(my_open_area) == 0:
        #     return float("-inf")
        # if len(opp_open_area) == 0:
        #     return float("inf")
        # if not my_open_area.intersection(opp_open_area):
        #     if len(my_open_area) == len(opp_open_area):
        #         return float("inf") if game.active_player == player else float("-inf")
        #     return float("inf") if len(my_open_area) > len(opp_open_area) else float("-inf")
        # return float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))




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

        # Try to get the search method (minimax or alphabeta)
        try:
            search_method = getattr(self, self.method)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                                      format(self.__class__.__name__, self.method))

        if not self.iterative:
            return search_method(game, self.search_depth)[1]

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            best_score = float("-inf")
            for depth in range(1, sys.maxsize**10):
                score, move = search_method(game, depth)
                if score > best_score:
                    best_score = score
                    best_move = move
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
            return self.score(game, player), (-1, -1)

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if maximizing_player:
            v = float("-inf")
            for move in legal_moves:
                next_game = game.forecast_move(move)
                score = self.minimax(next_game, depth - 1, False)[0]
                if score > v:
                    v = score
                    best_move = move
            return v, best_move
        else:
            v = float("inf")
            for move in legal_moves:
                next_game = game.forecast_move(move)
                score = self.minimax(next_game, depth - 1, True)[0]
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
            return self.score(game, player), (-1, -1)

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()

        if maximizing_player:
            v = float("-inf")
            for move in legal_moves:
                next_game = game.forecast_move(move)
                score = self.alphabeta(next_game, depth - 1, alpha, beta, False)[0]
                if score > v:
                    v = score
                    best_move = move
                if v >= beta:  # Pruning
                    return v, best_move
                alpha = max(alpha, v)
            return v, best_move
        else:
            v = float("inf")
            for move in legal_moves:
                next_game = game.forecast_move(move)
                score = self.alphabeta(next_game, depth - 1, alpha, beta, True)[0]
                if score < v:
                    v = score
                    best_move = move
                if v <= alpha:  # Pruning
                    return v, best_move
                beta = min(beta, v)
            return v, best_move
