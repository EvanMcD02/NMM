import sys
import NMM  # This is necessary for the project

BANNER = """
    __      _(_)_ __  _ __   ___ _ __| | |
    \ \ /\ / / | '_ \| '_ \ / _ \ '__| | |
     \ V  V /| | | | | | | |  __/ |  |_|_|
      \_/\_/ |_|_| |_|_| |_|\___|_|  (_|_)
"""

RULES = """                                                                                       
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    The game is ends when a player (the loser) has less than three 
    pieces on the board.
"""

MENU = """
    Game commands (first character is a letter, second is a digit):
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game

"""


## Uncomment the following lines when you are ready to do input/output tests!
## Make sure to uncomment when submitting to Codio.
def input( prompt=None ):
    if prompt != None:
        print( prompt, end="" )
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip( "\n" )
    print( aaa_str )
    return aaa_str


def count_mills(board, player):
    """
count_mills function takes in the current state of the board and one player, counts how many of the mills
are held by the player, and returns the count. This can be used to determine if a player has formed a new mill by
calling it before and after a placement is done.
    """
    count = 0  # number of mills found
    for mill in board.MILLS:  #  for each mill
        first_point = mill[0] #  first point in the mill
        second_point = mill[1] #  second point in the mill
        third_point = mill[2] #  third point in the mill
        if board.points[first_point] == player and board.points[second_point] == player and board.points[third_point] == player:  #  if the player has a mill
            count += 1
    return count


def place_piece_and_remove_opponents(board, player, destination):
    """
        This function is used to place a piece for player. If a mill is created, it removes an opponent’s piece (From
the functions you've created, which one is the suitable choice for removing a piece from the board?). It takes
three parameters: board, player, and destination.
- If a placement is invalid (cannot place a piece in an occupied spot), the function needs to raise a
RuntimeError.
- If the placement is valid, it needs to place the piece at the destination (which method from the Board
class is used to assign a piece in the board?). If a new mill is created, remove an opponent’s piece (From
the functions you've created, which one is the suitable choice for removing a piece from the board?).
Mills created can be determined by calling count_mills before and after the move.
    """
    mill_count = count_mills(board, player)  #  number of mills found
    #  if placement is invalid
    if board.points[destination] != " ":
        raise RuntimeError("Invalid placement")
    else:
        #  place the piece at the destination
        NMM.Board.assign_piece(board, player, destination)
    #  if current player's count increased
    if count_mills(board, player) > mill_count:  #  if a mill was formed
        #  remove an opponent’s piece
        print("A mill was formed!")
        remove_piece(board, get_other_player(player))


def move_piece(board, player, origin, destination):
    """
        This function is used to move a piece. It takes in board, player, origin, and destination. It needs to
raise a RuntimeError if a movement is invalid. If a movement is valid, it needs to check adjacency (if
necessary), remove the player’s piece from the origin point, and call the appropriate functions to place the piece
for player at the destination point and remove any opponent pieces if new mills were formed (From the
functions you've created, which one is the suitable choice for placing a piece and removing an opponent’s
piece?).
    """
    if board.points[origin] != player:  #  if the origin point is not the player's
        raise RuntimeError("Invalid command: Origin point does not belong to player")
    if board.points[origin] == player:
        if destination not in NMM.Board.ADJACENCY[origin]:  #  if the destination point is not adjacent to the origin point
            raise RuntimeError("Invalid command: Destination is not adjacent")
        if destination in NMM.Board.ADJACENCY[origin]:  #  if the destination point is adjacent to the origin point
            NMM.Board.clear_place(board, origin)  #  remove the player's piece from the origin point
            place_piece_and_remove_opponents(board, player, destination)  #  place the piece for player at the destination point


def points_not_in_mills(board, player):
    """
        This function will create a list of all points of player that aren't in mills. Use the list “mills” in
the Board class. Be careful because one piece can be part of horizontal mill, but not in a complete mill that is
vertical.
    """
    player_points = placed(board, player)  #  list of points where player's pieces have been placed
    points_set = set(player_points)  #  set of points where player's pieces have been placed
    mill_set = set()
    for mill in board.MILLS:  #  for each mill
        if mill[0] in player_points and mill[1] in player_points and mill[2] in player_points:  #  if the mill is in player_points
            mill_set.add(mill[0])
            mill_set.add(mill[1])
            mill_set.add(mill[2])
    points_not_in_mill = list(points_set - mill_set)  #  list of all points of player that aren't in mills
    return points_not_in_mill


def placed(board, player):
    """
        This function returns a list of points where player's pieces have been placed
    """
    list_of_points_played = []  #  list of points where player's pieces have been placed
    for point,value in board.points.items():  #  for each point on the board
        if value == player:  #  if the point is the player's
            list_of_points_played.append(point)
    return list_of_points_played


def remove_piece(board, player):
    """
        This function will remove a piece belonging to player from board. It needs to determine which points are
valid to remove (functions points_not_in_mills and placed are helpful), loop and get input until a
valid piece is removed, and handle the removal of the piece from the board (by calling the board
clear_place method in the Board class).
    """
    list_of_points_played = placed(board, player)  #  list of points where player's pieces have been placed
    list_of_points_not_in_mills = points_not_in_mills(board, player)  #  list of all points of player that aren't in mills
    print(board)
    while True:
    #  if there are no points to remove
        try:
            #  if len(list_of_points_not_in_mills) > 0:
                #  loop and get input until a valid piece is removed

            command = input("Remove a piece at :> ").strip().lower()
            if command in list_of_points_not_in_mills or len(list_of_points_not_in_mills) == 0:  #  if the player's point is not in a mill or there are no points to remove
                board.clear_place(command)  # remove the player's piece from the point
                break
            elif command in list_of_points_played and command not in list_of_points_not_in_mills:  #  if the point is in a mill
                raise RuntimeError("Invalid command: Point is in a mill")
            elif command not in list_of_points_played and command not in list_of_points_not_in_mills and command in NMM.Board.ADJACENCY:  #  if the point is not the player's
                raise RuntimeError("Invalid command: Point does not belong to player")
            else:
                raise RuntimeError("Invalid command: Not a valid point")
        except RuntimeError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))
            continue


def is_winner(board, player):
    """
        This function will be used to decide if a game was won. A game has been won if the opposing player has been
reduced to fewer than three pieces.
    """
    count = 0  # number of pieces the opposing player has
    for point,value in board.points.items():  #  for each point on the board
        if value == get_other_player(player):  #  if the point is the opposing player's
            count += 1
    if count < 3:  #  if the opposing player has been reduced to fewer than three pieces
        return True
    else:
        return False


def get_other_player(player):
    """
    Get the other player.
    """
    return "X" if player == "O" else "O"


def main():
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        placed_count = 0  # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent

        # PHASE 1
        print(player + "'s turn!")
        # placed = 0
        command = input("Place a piece at :> ").strip().lower()
        # Go back to top if reset
        print()
        # Until someone quits or we place all 18 pieces...
        while command != 'q' and command != 'r' and placed_count != 18:
            try:
                if command == 'h':
                    print(MENU)
                #  if the command is not two characters
                elif len(command) != 2:
                    raise RuntimeError("Command must be two characters")
                #  if the command is not a valid point
                elif command not in NMM.Board.ADJACENCY:
                    raise RuntimeError("Invalid command: Not a valid point")
                else:
                    #  call the place_piece_and_remove_opponents function
                    place_piece_and_remove_opponents(board, player, command)
                    #  increment the placed_count
                    placed_count += 1
                    #  switch players
                    player = get_other_player(player)


            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            # Prompt again
            if command != 'h':
                print(board)
                print(player + "'s turn!")
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        if command == 'r':
            continue

        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.split()
            try:
                #check to see if the list has two items
                if len(command) != 2:
                    raise RuntimeError("Invalid number of points")
                #  check to make sure command list has two items
                elif len(command[0]) == 2 and len(command[1]) == 2:
                    source_point = command[0]
                    destination_point = command[1]
                else:
                    raise RuntimeError("Invalid command format")
                if source_point in NMM.Board.ADJACENCY and destination_point in NMM.Board.ADJACENCY:
                    #  call the move_piece function
                    move_piece(board, player, source_point, destination_point)
                    #  switch players
                    player = get_other_player(player)
                else:
                    raise RuntimeError("Invalid command: Not a valid point")
                if is_winner(board, get_other_player(player)):  # if is_winner returns True
                    print(BANNER)  # display the banner
                    return  # exit the program

            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
                # Display and reprompt
            print(board)
            # display_board(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        # If we ever quit we need to return
        if command == 'q':
            return


if __name__ == "__main__":
    main()
