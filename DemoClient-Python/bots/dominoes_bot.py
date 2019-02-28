
def calculateMove(gameState):
    print(gameState)
    dom_li = [a for sub in gameState['center_dominoes'] for a in sub]  # make 2-dimension center_dominos into 1-dimension
    my_points = [a for sub in gameState['MyDominoes'] for a in sub]  # make 2-dimension MyDominoes into 1-dimension
    order_of_domino = check_to_move(dom_li, my_points)
    print(order_of_domino)
    move = {"suitable_domino": gameState["MyDominoes"][order_of_domino],
            "Position": check_position(gameState, order_of_domino)}

    return move


def check_to_move(dom_li, my_points):
    for my_point in my_points:
        if my_point == dom_li[0] or my_point == dom_li[-1]:
            order_of_domino = my_points.index(my_point) // 2
            return order_of_domino
        else:
            continue


def check_position(gameState, order_of_domino):
    my_domino = gameState["MyDominoes"][order_of_domino]
    center_dominoes = gameState["center_dominoes"]

    if my_domino[1] == center_dominoes[0][0] or my_domino[0] == center_dominoes[0][0]:
        return "L"
    elif my_domino[1] == center_dominoes[-1][1] or my_domino[0] == center_dominoes[-1][1]:
        return "R"
