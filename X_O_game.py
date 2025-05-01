import turtle

# Set up the screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("X O Game")
screen.bgcolor("white")
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# Global Constants
LINE_COLOR = "black"
X_COLOR = "red"
O_COLOR = "blue"
FONT_SIZE = 50
GRID_SIZE = 200

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.score = 0

class Board:
    def __init__(self):
        self.board = [str(i+1) for i in range(9)]  # Initialize the board with numbers 1 to 9
    
    def draw_grid(self):
        pen.penup()
        pen.goto(-GRID_SIZE, GRID_SIZE)
        pen.pendown()
        pen.pensize(5)
        pen.color(LINE_COLOR)
        
        # رسم المربعات الصغيرة (شبكة 3x3)
        for row in range(3):
            for col in range(3):
                pen.penup()
                pen.goto(-GRID_SIZE + col * GRID_SIZE, GRID_SIZE - row * GRID_SIZE)
                pen.pendown()
                for _ in range(4):  # رسم مربع لكل خلية
                    pen.forward(GRID_SIZE)
                    pen.right(90)
    
    def display_board(self):
        pen.clear()
        self.draw_grid()

        positions = []
        for row in range(3):
            for col in range(3):
                x = -GRID_SIZE + col * GRID_SIZE + GRID_SIZE // 2
                y = GRID_SIZE - row * GRID_SIZE - GRID_SIZE // 2- FONT_SIZE //3
                positions.append((x, y))

        
        # رسم الأرقام والرموز في أماكنها
        for i, cell in enumerate(self.board):
            pen.penup()
            pen.goto(positions[i])
            pen.pendown()
            if cell == 'X':
                pen.color(X_COLOR)
            elif cell == 'O':
                pen.color(O_COLOR)
            else:
                pen.color("black")
            pen.write(cell, align="center", font=("Arial", FONT_SIZE, "normal"))

        # display score
        pen.penup()
        pen.goto(0, 250)
        pen.color("black")
        pen.write(f"{game.players[0].name}: {game.players[0].score}    {game.players[1].name}: {game.players[1].score}",
                  align="center", font=("Arial", 20, "bold"))        
    
    def update_board(self, cell_choice, symbol):
        if self.board[cell_choice - 1] not in ["X", "O"]:
            self.board[cell_choice - 1] = symbol
            return True
        else:
            return False
    
    def reset_board(self):
        self.board = [str(i+1) for i in range(9)]

class Game:
    def __init__(self):
        self.board = Board()
        self.players = []
        self.current_player_index = 0

    def main_menu(self):
        pen.clear()
        pen.penup()
        pen.goto(0, 100)
        pen.pendown()
        pen.write("Welcome to X O Game", align="center", font=("Arial", 30, "bold"))
        pen.penup()
        pen.goto(0, 0)
        pen.pendown()
        pen.write("1. Start Game", align="center", font=("Arial", 24, "normal"))
        pen.penup()
        pen.goto(0, -50)
        pen.pendown()
        pen.write("2. Quit Game", align="center", font=("Arial", 24, "normal"))
        
        choice = screen.textinput("Menu", "Enter your choice (1 or 2):")
        if choice == "1":
            self.start_game()
        elif choice == "2":
            self.quit_game()
        else:
            self.main_menu()

    def setup_players(self):
        # Set up player 1
        player1_name = screen.textinput("Player 1", "Enter Player 1's name:")
        player1_symbol = screen.textinput("Player 1", "Choose X or O:").upper()
        while player1_symbol not in ["X", "O"]:
            player1_symbol = screen.textinput("Player 1", "Invalid input. Choose X or O:").upper()
        
        player2_symbol = "O" if player1_symbol == "X" else "X"
        player2_name = screen.textinput("Player 2", f"Enter Player 2's name:")
        
        self.players.append(Player(player1_name, player1_symbol))
        self.players.append(Player(player2_name, player2_symbol))

    def start_game(self):
        self.setup_players()
        self.board.display_board()
        self.play_game()

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                self.end_game(f"{self.players[self.current_player_index].name} wins!")
                break
            elif self.check_draw():
                self.end_game("It's a draw!")
                break
            self.switch_player()

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        while True:
            try:
                cell_choice = int(screen.textinput(f"{current_player.name}'s Turn", f"Choose a cell (1-9):"))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, current_player.symbol):
                    self.board.display_board()
                    break
                else:
                    screen.textinput("Invalid", "Invalid choice. Press OK to try again.")
            except ValueError:
                screen.textinput("Invalid", "Invalid input. Press OK to try again.")

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in win_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]:
                return True
        return False

    def check_draw(self):
        return all(cell in ["X", "O"] for cell in self.board.board)

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def end_game(self, message):
        screen.textinput("Game Over", message)
        if message.endswith("wins!"):
            self.players[self.current_player_index].score += 1
        while True:
            choice = screen.textinput("Post Game Menu",
                "Choose:\n1. Play Again\n2. New Game\n3. Quit Game")
            if choice == "1":
                self.board.reset_board()
                self.board.display_board()
                self.play_game()
                break
            elif choice == "2":
                self.players = []
                self.board.reset_board()
                self.current_player_index = 0
                self.main_menu()
                break
            elif choice == "3":
                self.quit_game()
                break

    def quit_game(self):
        pen.clear()
        pen.penup()
        pen.goto(0, 0)
        pen.pendown()
        pen.write("Thanks for playing!", align="center", font=("Arial", 24, "normal"))
        screen.bye()

game = Game()
game.main_menu()
turtle.mainloop()
