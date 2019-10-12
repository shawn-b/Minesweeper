# Your previous Plain Text content is preserved below:
# 
# You are presented with a board of squares. Some squares contain mines (bombs), others don't.  Each square that is not a bomb will contain an integer representing how many bombs are adjacent to it.
# 
# When as square is selected:
# 
# 1) if its a mine, the player loses the game
# 2) if its a number > 0, the board will reveal the selected square
# 3) if it is 0, we will reveal all other adjacent 0 valued squares and each square adjacent to those 0 valued square
# 
# Example:
# this is the fully revealed board
# 
# 1 1 1 _ _
# 1 M 2 1 _
# 1 2 M 1 _
# _ 1 1 1 _
# _ _ _ _ _

# 1 1 1 _ _
# 1 M 1 _ _
# 1 1 M _ _
# _ _ _ _ _

# [(1,1), (2,2)]
# [0,0]
# 
# Will look like this to the player

# X X X X X
# X X X X X 
# X X X X X 
# X X X X X 
# X X X X X  
# 
# Clicking the square in the lowest right most corner looks like (X represents a hidden square)
# 
# X X 1 _ _
# X X 2 1 _
# 1 2 X 1 _
# _ 1 1 1 _
# _ _ _ _ C
# 
# Prompt
# Please implement the following methods for a minesweeper game!
# 
# 1) generate_game_board(R, C, M)
#   Create a RxC grid filled with M randomly placed mines
# 2) select_space(x ,y)
#   Select a space given (x,y) coordinate and reveal the correct squares

import random
import os
import re

class Minesweeper:
    
    # =========================================================================
    # Initialize game board state
    def __init__(self, R=5, C=5, M=2):

        # Check that board game size meets minimum requirements
        if R < 5 or C < 5:
            print("Game board needs to be at least 5x5.")
            exit()

        # Check if number of mines exceeds game board spaces
        valid_tile_count = R * C - 1
        if M > valid_tile_count:
            print(f"Please choose a maximum of {valid_tile_count} mines for the {R}x{C} game board.")
            exit()

        # Number of non-mines for checking if player wins
        self.non_mine_count = R * C - M
        
        self.row_count = R
        self.col_count = C
        self.mine_count = M
        self.game_board = [[0 for y in range(C)] for x in range(R)]
        self.game_board_UI = [["X" for y in range(C)] for x in range(R)]
        self.mine_locations = []

        # Set mine locations on game board
        while len(self.mine_locations) < M:
            coords = (random.randint(0, C - 1), random.randint(0, R - 1))
            if coords not in self.mine_locations:
                self.mine_locations.append(coords)
                self.game_board[coords[0]][coords[1]] = "M"
               
        # Set non-mine locations on game board
        for mine in self.mine_locations:
            for coords in self.get_surrounding_coords(mine):
                if coords in self.mine_locations:
                    continue
                self.game_board[coords[0]][coords[1]] += 1
    
    # =========================================================================
    # Get list of valid surrounding coordinates given an (x,y) pair
    def get_surrounding_coords(self, loc):
        surroundings = [
            (loc[0] - 1, loc[1] - 1),    # top-left
            (loc[0] - 1, loc[1]),        # top
            (loc[0] - 1, loc[1] + 1),    # top-right
            (loc[0], loc[1] + 1),        # right
            (loc[0] + 1, loc[1] + 1),    # bottom-right
            (loc[0] + 1, loc[1]),        # bottom
            (loc[0] + 1, loc[1] - 1),    # bottom-left
            (loc[0], loc[1] - 1),        # left
        ]
        valid_surroundings = []
        for coords in surroundings:
            if coords[0] in range(0, self.row_count) and coords[1] in range(0, self.col_count):
                valid_surroundings.append(coords)
        return valid_surroundings

    # =========================================================================
    # Display current game board state
    def display_board(self):
        print("\n  ", end='')
        for i in range(self.col_count):
            if i % 2 == 0:
                print(f"|   ", end='')
        print()
        horz_dash_count = self.col_count * 2 + 1
        print(f"+{'-' * horz_dash_count}+")
        for i,row in enumerate(self.game_board_UI):
            print("| ", end='')
            for col in row:
                if col == 0:
                    print("_", end=" ")
                else:
                    print(col, end=" ")
            print(f"| {i}")
        print(f"+{'-' * horz_dash_count}+\n")

    # =========================================================================
    # Clear screen
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # =========================================================================
    # Print mine locations
    def print_mine_locations(self):
        print("\nMine locations:", self.mine_locations)

    # =========================================================================
    # Print mine count
    def print_mine_count(self):
        print("\nMine count:", len(self.mine_locations))

    # =========================================================================
    # Handle user input
    def handle_input(self, user_input):

        # Check if user wants to quit game
        if user_input == 'q':
            exit()

        # Check for proper input coordinate format
        user_input_pattern = re.compile(r"^\d+,\d+$")
        if user_input_pattern.match(user_input):
            x = int(user_input.split(",")[0])
            y = int(user_input.split(",")[1])

            # Check if valid input is within bounds of gameboard
            if x in range(0, self.row_count) and y in range(0, self.col_count):

                # If user chooses mine location, expose whole board and quit game
                if (x,y) in self.mine_locations:
                    self.game_board_UI = [row[:] for row in self.game_board]
                    return -1

                # If user chooses location with number, expose it
                elif self.game_board[x][y] > 0:
                    self.game_board_UI[x][y] = self.game_board[x][y]

                # If user chooses a blank location, expose all adjacent locations that are blank or have a number
                elif self.game_board[x][y] == 0:
                    coords_to_check = self.get_surrounding_coords((x,y))
                    coords_to_convert = []
                    coords_to_convert.append((x,y))
                    while coords_to_check:
                        for ctc in coords_to_check:
                            x, y = ctc[0], ctc[1]
                            coords_to_convert.append(ctc)
                            coords_to_check.remove(ctc)
                            if self.game_board[x][y] == 0:
                                surrounding_coords = self.get_surrounding_coords(ctc)
                                for sc in surrounding_coords:
                                    if sc not in coords_to_check and sc not in coords_to_convert:
                                        coords_to_check.append(sc)
                    for ctc in coords_to_convert:
                        x, y = ctc[0], ctc[1]
                        self.game_board_UI[x][y] = self.game_board[x][y]
            
        # Check if player won
        correct_plays_count = 0
        for row in self.game_board_UI:
            for col in row:
                if col != "X":
                    correct_plays_count += 1
        
        if correct_plays_count == self.non_mine_count:
            return 1
        else:
            return 0
    
    # =========================================================================
    # Run game interface with player input
    def run_game(self):

        game_over = False

        while not game_over:
            self.clear_screen()
            self.print_mine_count()
            #self.print_mine_locations()
            self.display_board()

            user_input = input("Enter 'v,h' values or 'q' to quit: ")
            result = self.handle_input(user_input)

            if result != 0:
                self.clear_screen()
                self.print_mine_count()
                #self.print_mine_locations()
                self.display_board()
                game_over = True
                if result == -1:
                    print("Sorry, you lose. :(")
                elif result == 1:
                    print("Yay, you win! :)")
                    

# Run game
game = Minesweeper(R=5, C=5, M=3)
game.run_game()
