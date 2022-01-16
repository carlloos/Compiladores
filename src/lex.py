import traceback
from states import *


class Lexer:

    def __init__(self, file):
        try:
            self.txtline = " "
            self.row = 1
            self.col = 1
            self.pos = 1
            self.reader = open(file, 'rb')
            self.newLine()
            self.lexem = ''
            self.content = list(self.txtline)
            self.state = None

        except IOError as e:
            traceback.print_exc()

    def getNextChar(self):
        self.pos += 1
        return self.content[self.pos - 1]

    def nextToken(self):
        self.state = 0
        self.lexem = ""
        while True:

            if self.isEOF():
                if self.newLine():
                    self.content = list(self.txtline)
                else:
                    return Token(Tokens.tokenDict["DELI_EOF"], "DELI_EOF", "EOF", self.row, self.col)

            curr_char = self.getNextChar()
            curr_state = None
            check = None

            if self.state == 0:
                curr_state = StateZero(self)

            elif self.state == 1:
                curr_state = StateOne(self)

            elif self.state == 2:
                curr_state = StateTwo(self)

            elif self.state == 3:
                curr_state = StateThree(self)

            elif self.state == 4:
                curr_state = StateFour(self)

            elif self.state == 5:
                curr_state = StateFive(self)

            elif self.state == 6:
                curr_state = StateSix(self)

            elif self.state == 7:
                curr_state = StateSeven(self)

            elif self.state == 8:
                curr_state = StateEight(self)

            elif self.state == 9:
                curr_state = StateNine(self)

            elif self.state == 10:
                curr_state = StateTen(self)

            elif self.state == 11:
                curr_state = StateEleven(self)

            elif self.state == 12:
                curr_state = StateTwelve(self)

            elif self.state == 13:
                curr_state = StateThirteen(self)

            check = curr_state.processState(curr_char)
            if check:
                return check

    def back(self):
        self.pos -= 1

    def newLine(self):

        tmp = ''

        try:
            tmp = self.reader.readline().decode("utf-8")

        except IOError as e:
            traceback.print_exc()

        if tmp != '':
            self.txtline = tmp
            printmessage = "{:>4}  " + self.txtline
            print(printmessage.format(int(self.row)))

            self.txtline += " "
            self.row += 1
            self.pos = 0
            self.col = 0

            return True

        return False

    def isEOF(self):
        return self.pos == len(self.content)
