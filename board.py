import tkinter as tk
from tkinter import messagebox
from enum import Enum

class AI(Enum):
    # AI 
    WIN = 10
    LOSE = -10
    TIE = 0
    ONGOING = 3

class Application:

    def __init__(self, root):

        self.root = root

        self.root.title("Tic Tac Toe")
        self.root.configure(background='black')

        self.player = 'X'
        self.ai = 'X' if self.player == 'O' else 'O'

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font='Helvetica 40 bold', bg='#15BDAC', height=2, width=4)
                self.buttons[i][j].config(command=lambda arg1=i, arg2=j: self.play(arg1,arg2))
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2) 

        self.reset()
        
    def reset(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
                self.board = [['' for _ in range(3)] for _ in range(3)]
        
    def play(self, i, j):
        # Player's turn
        self.buttons[i][j].config(text=self.player, state='disabled')
        self.board[i][j] = self.player
        # end early if game is over
        if self.check(): return

        # AI's turn
        next_i, next_j = self.minimax(self.board, 0, True, -1000, 1000)[1]
        self.buttons[next_i][next_j].config(text=self.ai, state='disabled')
        self.board[next_i][next_j] = self.ai
        self.check() 

    def minimax(self, board, depth, maxi, alpha, beta):
        status = self.end(board)    
        if status is not AI.ONGOING:
            return (status.value, )
        # maximize or minimize?
        if maxi:
            best_val = -1000
            best_move = (-1, -1)
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ''):
                        board[i][j] = self.ai
                        value = self.minimax(board, depth+1, False, alpha, beta)[0]
                        board[i][j] = ''
                        if value > best_val:
                            best_val = value
                            best_move = (i, j)
                        alpha = max(best_val, alpha)
                        if beta <= alpha:
                            return (best_val, best_move)
            return (best_val, best_move)
        else: 
            best_val = 1000
            best_move = (-1, -1)
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ''):
                        board[i][j] = self.player
                        value = self.minimax(board, depth+1, True, alpha, beta)[0]
                        board[i][j] = ''
                        if value < best_val:
                            best_val = value
                            best_move = (i, j)
                        beta = min(best_val, beta)
                        if beta <= alpha:
                            return (best_val, best_move)
            return (best_val, best_move)

    def end(self, board):
        # check 3 rows
        for i in range(3):
            sign1 = board[i][0]
            sign2 = board[i][1]
            sign3 = board[i][2]
            if sign1 == sign2 and sign2 == sign3 and sign1 != '':
                return AI.LOSE if sign1 == self.player else AI.WIN

        # check 3 columns
        for j in range(3):
            sign1 = board[0][j]
            sign2 = board[1][j]
            sign3 = board[2][j]
            if sign1 == sign2 and sign2 == sign3 and sign1 != '':
                return AI.LOSE if sign1 == self.player else AI.WIN

        # check diagonals
        sign1 = board[0][0]
        sign2 = board[1][1]
        sign3 = board[2][2]
        if sign1 == sign2 and sign2 == sign3 and sign1 != '':
            return AI.LOSE if sign1 == self.player else AI.WIN

        sign1 = board[0][2]
        sign2 = board[1][1]
        sign3 = board[2][0]
        if sign1 == sign2 and sign2 == sign3 and sign1 != '':
            return AI.LOSE if sign1 == self.player else AI.WIN

        # tie or ongoing?
        return AI.TIE if self.full(board) else AI.ONGOING

    def full(self, board):
        for i in range(3):
            for j in range(3):
                if (board[i][j] == ''):
                    return False
        return True

    def check(self):
        status = self.end(self.board)
        if status is AI.WIN:
            messagebox.showinfo("End", "You Lose!")
            self.reset() 
            return True
        elif status is AI.LOSE:
            messagebox.showinfo("End", "You win!")
            self.reset() 
            return True
        elif status is AI.TIE:
            messagebox.showinfo("End", " It's a Tie!")
            self.reset() 
            return True
        else: 
            return False
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
