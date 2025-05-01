import tkinter as tk
from tkinter import messagebox

class XOGame:
    def __init__(self, master):
        self.master = master
        self.master.title("X O Game")
        self.master.geometry("400x400")  # تكبير النافذة
        self.reset_game()

        self.welcome_frame = tk.Frame(self.master)
        self.welcome_frame.pack()
        self.label = tk.Label(self.welcome_frame, text="Welcome to the X O Game")
        self.label.pack()

        self.start_button = tk.Button(self.welcome_frame, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.quit_button = tk.Button(self.welcome_frame, text="Quit Game", command=self.master.quit)
        self.quit_button.pack()

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = None
        self.symbols = {}
        self.buttons = []

    def start_game(self):
        self.welcome_frame.pack_forget()
        self.player_setup()

    def player_setup(self):
        self.setup_frame = tk.Frame(self.master)
        self.setup_frame.pack()

        self.label1 = tk.Label(self.setup_frame, text="Enter Player 1 name:")
        self.label1.pack()
        self.player1_entry = tk.Entry(self.setup_frame)
        self.player1_entry.pack()

        self.symbol1_var = tk.StringVar(value='X')
        self.symbol1_label = tk.Label(self.setup_frame, text="Choose your symbol:")
        self.symbol1_label.pack()
        self.x_radio = tk.Radiobutton(self.setup_frame, text='X', variable=self.symbol1_var, value='X')
        self.x_radio.pack()
        self.o_radio = tk.Radiobutton(self.setup_frame, text='O', variable=self.symbol1_var, value='O')
        self.o_radio.pack()

        self.submit_button = tk.Button(self.setup_frame, text="Next", command=self.setup_player2)
        self.submit_button.pack()

    def setup_player2(self):
        player1_name = self.player1_entry.get()
        symbol1 = self.symbol1_var.get()

        if not player1_name:
            messagebox.showerror("Error", "Please enter Player 1 name.")
            return

        self.symbols['player1'] = symbol1
        self.symbols['player2'] = 'O' if symbol1 == 'X' else 'X'

        self.setup_frame.pack_forget()

        self.label2 = tk.Label(self.master, text="Enter Player 2 name:")
        self.label2.pack()
        self.player2_entry = tk.Entry(self.master)
        self.player2_entry.pack()

        self.submit2_button = tk.Button(self.master, text="Start Playing", command=self.create_board)
        self.submit2_button.pack()

    def create_board(self):
        player2_name = self.player2_entry.get()
        if not player2_name:
            messagebox.showerror("Error", "Please enter Player 2 name.")
            return

        self.symbols['player2'] = 'O' if self.symbols['player1'] == 'X' else 'X'
        self.current_player = 'player1'

        # حذف جميع العناصر السابقة من النافذة الرئيسية
        for widget in self.master.winfo_children():
            widget.pack_forget()

        # إنشاء إطار جديد للوحة اللعبة
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        # إنشاء الأزرار باستخدام grid داخل إطار منفصل
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.board_frame, text=' ', width=10, height=4,  # زيادة حجم الأزرار
                                   command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def make_move(self, row, col):
        index = row * 3 + col
        if self.board[index] == ' ':
            self.board[index] = self.symbols[self.current_player]
            self.update_button_color(row, col)  # تغيير لون الزر بناءً على الرمز
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Winner", f"The winner is: {winner}")
                self.reset_board()
            elif ' ' not in self.board:
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'player2' if self.current_player == 'player1' else 'player1'

    def update_button_color(self, row, col):
        symbol = self.board[row * 3 + col]
        color = "red" if symbol == 'X' else "blue"
        self.buttons[row][col].config(text=symbol, fg=color)  # تغيير لون النص حسب الرمز

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.symbols['player1'] if self.board[combo[0]] == self.symbols['player1'] else self.symbols['player2']
        return None

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        for row in self.buttons:
            for button in row:
                button.config(text=' ', fg="black")  # إعادة تعيين الألوان إلى الأسود

if __name__ == "__main__":
    root = tk.Tk()
    game = XOGame(root)
    root.mainloop()
