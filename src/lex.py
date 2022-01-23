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
        self.state = StateZero(self)
        self.lexem = ""
        while True:

            if self.isEOF():
                if self.newLine():
                    self.content = list(self.txtline)
                else:
                    return Token(Tokens.tokenDict["DELI_EOF"], "DELI_EOF", "EOF", self.row, self.col)

            curr_char = self.getNextChar()
            check = None

            check = self.state.processState(curr_char)
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
        aux = ''
        is_on = True
        if tmp != '':
            for i in tmp:
                if Blank(i).validate() and is_on:
                    pass
                elif not is_on:
                    aux = aux + i
                elif not (Blank(i).validate()) and Alphanum(i).validate():
                    is_on = False
                    aux = aux + i


            self.txtline = aux.replace('\n', '')
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
