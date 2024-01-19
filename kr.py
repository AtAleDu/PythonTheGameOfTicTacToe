from tkinter import *
import random

current_player = 'X'
game_mode = '2'


class MiniGrid:
    def __init__(self, master, big_row, big_col, game_callback):
        self.master = master
        self.big_row = big_row
        self.big_col = big_col
        self.game_callback = game_callback
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.create_grid()

    def create_grid(self):
        for row in range(3):
            for col in range(3):
                button = Button(self.master, text=' ', width=2, height=1,
                                font=('Verdana', 10, 'bold'), background='lavender',
                                command=lambda r=row, c=col: self.game_callback(self, r, c))
                button.grid(row=row, column=col, sticky='nsew')
                self.buttons[row][col] = button

    def new_game(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = ' '
                self.buttons[row][col]['background'] = 'lavender'
        self.winner = None

    def make_move(self, row, col, symbol):
        if self.buttons[row][col]['text'] == ' ' and not self.winner:
            self.buttons[row][col]['text'] = symbol
            if self.check_win(symbol):
                self.winner = symbol
                self.highlight_winner()
            return True
        return False

    def check_win(self, symbol):
        for row in range(3):
            if all(self.buttons[row][col]['text'] == symbol for col in range(3)):
                return True
        for col in range(3):
            if all(self.buttons[row][col]['text'] == symbol for row in range(3)):
                return True
        if all(self.buttons[i][i]['text'] == symbol for i in range(3)):
            return True
        if all(self.buttons[i][2-i]['text'] == symbol for i in range(3)):
            return True
        return False

    def highlight_winner(self):
        color = 'light green' if self.winner == 'X' else 'light blue'
        for row in self.buttons:
            for button in row:
                button['background'] = color
                button['state'] = DISABLED  # Делаем кнопку неактивной

    def highlight_grid(self, highlight):
        color = 'yellow' if highlight else 'lavender'
        for row in self.buttons:
            for button in row:
                button['background'] = color


def switch_player():
    global current_player
    current_player = 'O' if current_player == 'X' else 'X'


def set_game_mode_to_player_vs_player():
    global game_mode
    game_mode = '2'
    new_game()


def set_game_mode_to_player_vs_computer():
    global game_mode
    game_mode = '1'
    new_game()


def new_game():
    global game_run, current_mini_grid, winner
    game_run = True
    current_mini_grid = None
    winner = None
    for big_row in big_field:
        for mini_grid in big_row:
            mini_grid.new_game()
    highlight_current_mini_grid()


def highlight_current_mini_grid():
    for big_row in big_field:
        for mini_grid in big_row:
            mini_grid.highlight_grid(mini_grid == current_mini_grid)


def check_big_field_win():
    for row in range(3):
        if big_field[row][0].winner == big_field[row][1].winner == big_field[row][2].winner and big_field[row][0].winner:
            return big_field[row][0].winner
        if big_field[0][row].winner == big_field[1][row].winner == big_field[2][row].winner and big_field[0][row].winner:
            return big_field[0][row].winner
    if big_field[0][0].winner == big_field[1][1].winner == big_field[2][2].winner and big_field[0][0].winner:
        return big_field[0][0].winner
    if big_field[2][0].winner == big_field[1][1].winner == big_field[0][2].winner and big_field[2][0].winner:
        return big_field[2][0].winner
    return None


def show_winner_message(symbol):
    winner_message = Toplevel(root)
    winner_message.title('Победитель!')
    label = Label(winner_message, text=f'Победил игрок {symbol}!', font=('Verdana', 14))
    label.pack(padx=20, pady=20)
    ok_button = Button(winner_message, text='OK', command=winner_message.destroy)
    ok_button.pack(pady=10)


def click(mini_grid, row, col):
    global current_mini_grid, game_run, current_player
    if game_run:
        if current_mini_grid is None or current_mini_grid == mini_grid:
            if mini_grid.make_move(row, col, current_player):
                if check_big_field_win():
                    game_run = False
                    show_winner_message(current_player)
                else:
                    switch_player()
                    current_mini_grid = None if big_field[row][col].winner else big_field[row][col]
                    highlight_current_mini_grid()
                if game_mode == '1' and current_player == 'O':
                    root.after(100, computer_turn)


def computer_turn():
    computer_move()
    switch_player()
    highlight_current_mini_grid()



def computer_move():
    global current_mini_grid, game_run, current_player
    if game_run and current_mini_grid and not current_mini_grid.winner:
        empty_cells = [(r, c) for r in range(3) for c in range(3) if current_mini_grid.buttons[r][c]['text'] == ' ']
        if empty_cells:
            row, col = random.choice(empty_cells)
            current_mini_grid.make_move(row, col, 'O')
            if check_big_field_win():
                game_run = False
                show_winner_message('O')
            else:
                current_mini_grid = None if big_field[row][col].winner else big_field[row][col]



root = Tk()
root.title('Крестики-нолики Беркли')
root.geometry("270x325")

big_field = [[None for _ in range(3)] for _ in range(3)]
current_mini_grid = None
game_run = True
winner = None

for big_row in range(3):
    frame_row = []
    for big_col in range(3):
        frame = Frame(root, borderwidth=1, relief="raised")
        frame.grid(row=big_row, column=big_col, padx=2, pady=2, sticky='nsew')
        mini_grid = MiniGrid(frame, big_row, big_col, click)
        frame_row.append(mini_grid)
    big_field[big_row] = frame_row

player_vs_player_button = Button(root, text='Игрок против Игрока', command=set_game_mode_to_player_vs_player)
player_vs_player_button.grid(row=3, column=0, columnspan=3, sticky='nsew')

player_vs_computer_button = Button(root, text='Игрок против Компьютера', command=set_game_mode_to_player_vs_computer)
player_vs_computer_button.grid(row=4, column=0, columnspan=3, sticky='nsew')

root.mainloop()
