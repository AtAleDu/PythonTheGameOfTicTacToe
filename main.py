from tkinter import *
import random

root = Tk()
root.title('Крестики-нолики')
game_run = True
field = []
cross_count = 0

def new_game():
    global game_run
    game_run = True
    global cross_count
    cross_count = 0
    for row in range(3):
        for col in range(3):
            field[row][col]['text'] = ' '
            field[row][col]['background'] = 'lavender'

def check_win(smb):
    for n in range(3):
        check_line(field[n][0], field[n][1], field[n][2], smb)
        check_line(field[0][n], field[1][n], field[2][n], smb)
    check_line(field[0][0], field[1][1], field[2][2], smb)
    check_line(field[2][0], field[1][1], field[0][2], smb)

def check_line(a1, a2, a3, smb):
    if a1['text'] == smb and a2['text'] == smb and a3['text'] == smb:
        a1['background'] = a2['background'] = a3['background'] = 'pink'
        show_winner_message(smb)
        global game_run
        game_run = False

def show_winner_message(winner):
    winner_message = Toplevel(root)
    winner_message.title('Победитель!')
    label = Label(winner_message, text=f'Победил игрок {winner}!', font=('Verdana', 14))
    label.pack(padx=20, pady=20)
    ok_button = Button(winner_message, text='OK', command=winner_message.destroy)
    ok_button.pack(pady=10)

def can_win(a1, a2, a3, smb):
    res = False
    if a1['text'] == smb and a2['text'] == smb and a3['text'] == ' ':
        a3['text'] = 'O'
        res = True
    if a1['text'] == smb and a2['text'] == ' ' and a3['text'] == smb:
        a2['text'] = 'O'
        res = True
    if a1['text'] == ' ' and a2['text'] == smb and a3['text'] == smb:
        a1['text'] = 'O'
        res = True
    return res

def check_tie():
    for row in range(3):
        for col in range(3):
            if field[row][col]['text'] == ' ':
                return False  # Есть свободная клетка, игра не закончена
    return True  # Все клетки заполнены, ничья

def click(row, col):
    global cross_count
    if game_run and field[row][col]['text'] == ' ':
        field[row][col]['text'] = 'X'
        cross_count += 1
        check_win('X')
        if game_run and cross_count < 5:
            computer_move()
        if cross_count == 5 and not game_run and check_tie():
            show_tie_message()

def computer_move():
    for n in range(3):
        if can_win(field[n][0], field[n][1], field[n][2], 'O'):
            check_win('O')  # Добавлен вызов проверки на победу для 'O'
            return
        if can_win(field[0][n], field[1][n], field[2][n], 'O'):
            check_win('O')  # Добавлен вызов проверки на победу для 'O'
            return
    if can_win(field[0][0], field[1][1], field[2][2], 'O'):
        check_win('O')  # Добавлен вызов проверки на победу для 'O'
        return
    if can_win(field[2][0], field[1][1], field[0][2], 'O'):
        check_win('O')  # Добавлен вызов проверки на победу для 'O'
        return
    for n in range(3):
        if can_win(field[n][0], field[n][1], field[n][2], 'X'):
            return
        if can_win(field[0][n], field[1][n], field[2][n], 'X'):
            return
    if can_win(field[0][0], field[1][1], field[2][2], 'X'):
        return
    if can_win(field[2][0], field[1][1], field[0][2], 'X'):
        return
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if field[row][col]['text'] == ' ':
            field[row][col]['text'] = 'O'
            check_win('O')  # Добавлен вызов проверки на победу для 'O'
            break

def show_tie_message():
    tie_message = Toplevel(root)
    tie_message.title('Ничья!')
    label = Label(tie_message, text='Игра завершилась вничью!', font=('Verdana', 14))
    label.pack(padx=20, pady=20)
    ok_button = Button(tie_message, text='OK', command=tie_message.destroy)
    ok_button.pack(pady=10)

for row in range(3):
    line = []
    for col in range(3):
        button = Button(root, text=' ', width=4, height=2,
                        font=('Verdana', 20, 'bold'),
                        background='lavender',
                        command=lambda row=row, col=col: click(row, col))
        button.grid(row=row, column=col, sticky='nsew')
        line.append(button)
    field.append(line)

new_button = Button(root, text='Новая игра', command=new_game)
new_button.grid(row=3, column=0, columnspan=3, sticky='nsew')

root.mainloop()
