import random
matches = []

class c4match:
    def __init__(self, player1, player2, channel):
        self.player1 = player1
        self.player2 = player2
        self.channel = channel

        self.title = ""
        self.turn = player1
        self.status = "Ongoing"
        self.board = ""
        self.b = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

    def getTitle(self):
        i = random.randint(1, 10)
        if i <= 7:
            s = "Connect Four!"
        if i == 8:
            s = "Battle of the Mentally Disabled"
        if i == 9:
            s = "Battle of Autism"
        if i == 10:
            s = "Battle for Mio Honda"
        return s

    def displayBoard(self):
        s = ":one: :two: :three: :four: :five: :six: :seven: \n"
        for rows in self.b:
            for x in rows:
                if x == 0:
                    s = s + ":white_circle:"
                if x == 1:
                    s = s + ":red_circle:"
                if x == 2:
                    s = s + ":blue_circle:"
                if x == 3:
                    s = s + ":green_circle:"
                s = s + " "
            s = s + "\n"
        return s

    def play(player1, player2, channel):
        match = c4match(player1, player2, channel)
        match.title = match.getTitle()
        matches.append(match)

        match.board = match.displayBoard()
        return match
    
    def isAvailable(self, player, c):
        b = True
        if self.turn != player:
            b = False
        if self.b[0][c] != 0:
            b = False
        if c > 6 or c < 0:
            b = False
        return b

    def checkBoard(self, n):
        board = self.b
        r = 0
        c = 0
        while r < len(board):
            while c < len(board[r]):
                if board[r][c] == n or 3 == board[r][c]:
                    if c < 4:
                        x = c + 1
                        while x < c + 4:
                            if n != board[r][x] and 3 != board[r][x]:
                                break
                            x = x + 1
                        if x == c + 4:
                            self.status = "Concluded"

                            x = c
                            while x < c + 4:
                                board[r][x] = 3
                                x = x + 1

                    if r < 3:
                        y = r + 1
                        while y < r + 4:
                            if n != board[y][c] and 3 != board[y][c]:
                                break
                            y = y + 1
                        if y == r + 4:
                            self.status = "Concluded"

                            y = r
                            while y < r + 4:
                                board[y][c] = 3
                                y = y + 1
                
                    if r < 3 and c < 4:
                        x = c + 1
                        y = r + 1
                        while y < r + 4:
                            if n != board[y][x] and 3 != board[y][x]:
                                break
                            y = y + 1
                            x = x + 1
                        if y == r + 4:
                            self.status = "Concluded"

                            x = c
                            y = r
                            while y < r + 4:
                                board[y][x] = 3
                                y = y + 1
                                x = x + 1
                
                    if r < 3 and c > 2:
                        x = c - 1
                        y = r + 1
                        while y < r + 4:
                            if n != board[y][x] and 3 != board[y][x]:
                                break
                            y = y + 1
                            x = x - 1
                        if y == r + 4:
                            self.status = "Concluded"

                            x = c
                            y = r
                            while y < r + 4:
                                board[y][x] = 3
                                y = y + 1
                                x = x - 1

                c = c + 1
            c = 0
            r = r + 1

        for x in board:
            for y in x:
                if y == 0:
                    return self
        
        self.status = "Stalemate"
        return self

    def turn(self, player, c):
        c = c - 1
        if self.isAvailable(player, c) == True:
            i = 5
            while i >= 0:
                if self.b[i][c] == 0:
                    break
                i = i - 1
            if self.turn == self.player1:
                self.b[i][c] = 1
                self.turn = self.player2
            else:
                self.b[i][c] = 2
                self.turn = self.player1

            self = c4match.checkBoard(self, self.b[i][c])
            self.board = self.displayBoard()
            return self
        
        else:
            return None

def checkPlayers(player1, player2):

    for x in matches:
        if x.player1 == player1 or x.player2 == player1:
            return player1
        if x.player1 == player2 or x.player2 == player2:
            return player2

    return None

def getMatch(player):
    for x in matches:
        if x.player1 == player or x.player2 == player:
            return x
    return None
    
def clearMatch(match):
    matches.remove(match)