import random

SIZE = 5

EMPTY = '.'
SHIP = 'X'
HIT = '*'
MISS = 'O'

class Board:
    def __init__(self):
        self.board = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.ships = []

    def place_ship(self, ship_size, x, y, direction):
        """Place a ship on the board."""
        if direction == 'H': 
            for i in range(ship_size):
                self.board[y][x + i] = SHIP
        elif direction == 'V': 
            for i in range(ship_size):
                self.board[y + i][x] = SHIP
        self.ships.append((ship_size, x, y, direction))

    def print_board(self, show_ships=False):
        """Display the board."""
        print("  " + " ".join([str(i) for i in range(SIZE)]))
        for y in range(SIZE):
            row = str(y) + " "
            for x in range(SIZE):
                if show_ships and self.board[y][x] == SHIP:
                    row += SHIP + " "
                else:
                    row += self.board[y][x] + " "
            print(row)

    def is_game_over(self):
        """Check if there are any ships left on the board."""
        for row in self.board:
            if SHIP in row:
                return False
        return True

    def make_move(self, x, y):
        """Make a move, checking if it hits a ship."""
        if self.board[y][x] == SHIP:
            self.board[y][x] = HIT
            return True
        elif self.board[y][x] == EMPTY:
            self.board[y][x] = MISS
            return False
        return None

class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.computer_visible_board = Board()

    def place_computer_ships(self):
        """Place computer's ships randomly."""
        ships = [3, 2, 2, 1, 1]  
        for ship_size in ships:
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)
                if direction == 'H' and x + ship_size <= SIZE:
                    placed = True
                    for i in range(ship_size):
                        if self.computer_board.board[y][x + i] == SHIP:
                            placed = False
                            break
                    if placed:
                        self.computer_board.place_ship(ship_size, x, y, direction)
                elif direction == 'V' and y + ship_size <= SIZE:
                    placed = True
                    for i in range(ship_size):
                        if self.computer_board.board[y + i][x] == SHIP:
                            placed = False
                            break
                    if placed:
                        self.computer_board.place_ship(ship_size, x, y, direction)

    def place_player_ships(self):
        """Player places their ships manually."""
        ships = [3, 2, 2, 1, 1]
        for ship_size in ships:
            placed = False
            while not placed:
                print(f"Placing a ship of size {ship_size}")
                self.player_board.print_board(show_ships=True)
                x, y, direction = self.get_player_input()
                if self.is_valid_move(x, y, direction, ship_size, self.player_board):
                    self.player_board.place_ship(ship_size, x, y, direction)
                    placed = True
                else:
                    print("Invalid move, try again.")

    def get_player_input(self):
        """Get input from the player."""
        x = int(input("Enter X coordinate: "))
        y = int(input("Enter Y coordinate: "))
        direction = input("Enter direction (H - horizontal, V - vertical): ").upper()
        return x, y, direction

    def is_valid_move(self, x, y, direction, ship_size, board):
        """Check if a ship can be placed at this location."""
        if direction == 'H':
            if x + ship_size > SIZE:
                return False
            for i in range(ship_size):
                if board.board[y][x + i] == SHIP:
                    return False
        elif direction == 'V':
            if y + ship_size > SIZE:
                return False
            for i in range(ship_size):
                if board.board[y + i][x] == SHIP:
                    return False
        return True

    def player_turn(self):
        """Player's turn."""
        print("Player's turn")
        self.computer_visible_board.print_board(show_ships=False)
        x, y = self.get_player_input_for_attack()
        hit = self.computer_board.make_move(x, y)
        if hit:
            print("Hit!")
        else:
            print("Miss!")

    def computer_turn(self):
        """Computer's turn."""
        print("Computer's turn")
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        print(f"Computer attacks {x}, {y}")
        hit = self.player_board.make_move(x, y)
        if hit:
            print("Computer hit!")
        else:
            print("Computer missed.")

    def get_player_input_for_attack(self):
        """Get attack coordinates from the player."""
        x = int(input("Enter X coordinate to attack: "))
        y = int(input("Enter Y coordinate to attack: "))
        return x, y

    def play(self):
        """Start the game."""
        self.place_computer_ships()
        self.place_player_ships()

        while True:
            self.player_turn()
            if self.computer_board.is_game_over():
                print("You won!")
                break
            self.computer_turn()
            if self.player_board.is_game_over():
                print("You lost!")
                break

if __name__ == "__main__":
    game = Game()
    game.play()
