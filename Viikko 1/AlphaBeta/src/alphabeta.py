TEMPLATE_FIELD = '|e|e|e|\n|e|e|e|\n|e|e|e|\n'
HUGE_NUMBER = 1000000


class AlphaBetaNode(object):
    def __init__(self):
        pass

    def generate_children(self):
        pass

    def is_max_node(self):
        pass

    def is_end_state(self):
        pass

    def value(self):
        pass


class TicTacToe(AlphaBetaNode):
    """Class that contains current state of the game and implements AlphaBetaNode methods
    :attr state: Current state of the board (str)
    :attr state: Indicates whose turn it is (Boolean)
    """

    def __init__(self, state, crosses_turn):
        super().__init__()
        self.state = state
        self.crosses_turn = crosses_turn

    def is_end_state(self):
        return ('?' not in self.state) or self.won('x') or self.won('o')

    def won(self, c):
        triples = [self.state[0:3], self.state[3:6], self.state[6:9], self.state[::3], self.state[1::3],
                   self.state[2::3], self.state[0] + self.state[4] + self.state[8],
                   self.state[2] + self.state[4] + self.state[6]]
        combo = 3 * c
        return combo in triples

    def __str__(self):
        field = TEMPLATE_FIELD
        for c in self.state:
            field = field.replace('e', c, 1)

        return field

    def is_max_node(self):
        return self.crosses_turn

    def generate_children(self):
        """
        Generates list of all possible states after this turn
        :return: list of TicTacToe objects
        """
        children = []
        
        for i in range(len(self.state)):
            new_state = list(self.state)
            if new_state[i] == '?':
                if self.crosses_turn:
                    new_state[i] = 'x'
                    new_state = "".join(new_state)
                    children.append(TicTacToe(new_state, False))
                else:
                    new_state[i] = 'o'
                    new_state = "".join(new_state)
                    children.append(TicTacToe(new_state, True))

        return children

    def value(self):
        """
        Current score of the game (0, 1, -1)
        :return: int
        """
        if self.won('x'):
            return 1
        if self.won('o'):
            return -1

        return 0

def alpha_beta_value(node):
    """Implements the MinMax algorithm with alpha-beta pruning
    :param node: State of the game (TicTacToe)
    :return: int
    """
    if node.is_max_node():
        value = max_value(node, -1, 1)
        return value
        
    else:
        value = min_value(node, -1, 1)
        return value
    


def max_value(node, alpha, beta):
    v = -HUGE_NUMBER
    
    if node.is_end_state():
        return node.value()
    
    for child in node.generate_children():
        v = max(v, min_value(child, alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            return v

    return v


def min_value(node, alpha, beta):
    v = HUGE_NUMBER
    
    if node.is_end_state():
        return node.value()
    
    for child in node.generate_children():
        v = min(v, max_value(child, alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            return v

    return v

def alpha_beta_value_track(node):
    """Implements the MinMax algorithm with alpha-beta pruning
    :param node: State of the game (TicTacToe)
    :return: tuple (int, TicTacToe or None)
    """
    if node.is_max_node():
        value, best_child = max_value_track(node, -1, 1)
        return value, best_child
        
    else:
        value, best_child = min_value_track(node, -1, 1)
        return value, best_child

def max_value_track(node, alpha, beta):
    v = -HUGE_NUMBER
    best_child = None
    
    if node.is_end_state():
        return (node.value(), best_child)
    
    for child in node.generate_children():
        prev_v = v
        v = max(v, min_value_track(child, alpha, beta)[0])
        if v > prev_v:
            best_child = child
        alpha = max(alpha, v)
        if alpha >= beta:
            return (v, best_child)

    return (v, best_child)


def min_value_track(node, alpha, beta):
    v = HUGE_NUMBER
    best_child = None
    
    if node.is_end_state():
        return (node.value(), best_child)
    
    for child in node.generate_children():
        prev_v = v
        v = min(v, max_value_track(child, alpha, beta)[0])
        if v < prev_v:
            best_child = child
        beta = min(beta, v)
        if alpha >= beta:
            return (v, best_child)

    return (v, best_child)
