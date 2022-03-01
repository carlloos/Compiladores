from dictPyr import *
from tkn import *
from validate import *
from auxfile import aux_dict


class State (ABC):

    def __init__(self, lexer):
        self.lexer = lexer

    @abstractmethod
    def processState(self, curr_char):
        pass


class StateZero(State):
    def processState(self, curr_char):
        if Blank(curr_char).validate():
            self.lexer.state = StateZero(self.lexer)

        elif LowerCase(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = StateOne(self.lexer)

        elif Digit(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = StateThree(self.lexer)

        elif Operator(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = StateSeven(self.lexer)

        elif curr_char == '\'':
            self.lexer.lexem += curr_char
            self.lexer.state = StateEight(self.lexer)

        elif curr_char == '\"':
            self.lexer.lexem += curr_char
            self.lexer.state = StateTen(self.lexer)

        elif UpperCase(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = StateEleven(self.lexer)

        elif curr_char == '#':
            self.lexer.lexem += curr_char
            self.lexer.state = StateThirteen(self.lexer)

        elif curr_char in ['+', '-', '*', '/', '%', '@', '^', '&', '|']:
            self.lexer.lexem += curr_char
            self.lexer.col += 1
            aux = aux_dict[curr_char]
            return Token(Tokens.tokenDict[aux], aux, self.lexer.lexem, self.lexer.row, self.lexer.col)

        elif curr_char in ['(', ')', '[', ']', ';', ',']:
            self.lexer.lexem += curr_char
            self.lexer.col += 1
            aux = aux_dict[curr_char]
            return Token(Tokens.tokenDict[aux], aux, self.lexer.lexem, self.lexer.row, self.lexer.col)

        else:
            Token(Tokens.tokenDict['ERR_UNK'], 'ERR_UNK', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateOne(State):  # ID State
    def processState(self, curr_char):

        if (Digit(curr_char).validate() or LowerCase(curr_char).validate() or UpperCase(curr_char).validate()
                or curr_char == '_'):
            self.lexer.lexem += curr_char

        elif Operator(curr_char).validate() or Blank(curr_char).validate() or not Alphanum(curr_char).validate():
            self.lexer.back()
            self.lexer.state = StateTwo(self.lexer)

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_IND'], 'ERR_IND', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateTwo(State):  # Final State for IDs
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['ID'], 'ID', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateThree(State):  # State that defines numeric CNST
    def processState(self, curr_char):
        if curr_char == '.':
            self.lexer.lexem += curr_char
            self.lexer.state = StateFour(self.lexer)
            self.lexer.col = +1

        elif Digit(curr_char).validate():
            self.lexer.lexem += curr_char

        elif not Alphanum(curr_char).validate():
            self.lexer.back()
            self.lexer.state = StateFive(self.lexer)

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_NUMER'], 'ERR_NUMER', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateFour(State):  # State for float decimal part
    def processState(self, curr_char):
        if Digit(curr_char).validate():
            self.lexer.lexem += curr_char

        elif Operator(curr_char).validate() or Blank(curr_char).validate() or not Alphanum(curr_char).validate():
            self.lexer.back()
            self.lexer.state = StateSix(self.lexer)

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_NUMER'], 'ERR_NUMER', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateFive(State):  # Final state for CNST_INT
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['CNST_INT'], 'CNST_INT', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateSix(State):  # Final State for CNST_FLOAT
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['CNST_FLOAT'], 'CNST_FLOAT', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateSeven(State):  # State that defines Relacional operations "<, <=, >, >=, !, ==, !=
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.back()
        curr_char = self.lexer.getNextChar()

        if curr_char == '>':
            curr_char = self.lexer.getNextChar()
            self.lexer.col += 1

            if curr_char == '=':
                self.lexer.lexem += curr_char
                return Token(Tokens.tokenDict['OPE_MAIORI'], 'OPE_MAIORI', self.lexer.lexem, self.lexer.row,
                             self.lexer.col)
            else:
                self.lexer.back()
                return Token(Tokens.tokenDict['OPE_MAIORQ'], 'OPE_MAIORQ', self.lexer.lexem, self.lexer.row,
                             self.lexer.col)

        elif curr_char == '<':

            curr_char = self.lexer.getNextChar()
            self.lexer.col += 1

            if curr_char == '=':
                self.lexer.lexem += curr_char
                return Token(Tokens.tokenDict['OPE_MENORI'], 'OPE_MENORI', self.lexer.lexem, self.lexer.row,
                             self.lexer.col)
            else:
                self.lexer.back()
                return Token(Tokens.tokenDict['OPE_MENORQ'], 'OPE_MENORQ', self.lexer.lexem, self.lexer.row,
                             self.lexer.col)

        elif curr_char == '!':
            curr_char = self.lexer.getNextChar()
            self.lexer.col += 1

            if curr_char == '=':
                self.lexer.lexem += curr_char

                return Token(Tokens.tokenDict['OPE_DIFE'], 'OPE_DIFE', self.lexer.lexem, self.lexer.row,
                            self.lexer.col)
            else:
                self.lexer.back()
                return Token(Tokens.tokenDict['OPE_NEGA'], 'OPE_NEGA', self.lexer.lexem, self.lexer.row, self.lexer.col)

        elif curr_char == '=':
            curr_char = self.lexer.getNextChar()
            self.lexer.col += 1

            if curr_char == '=':
                self.lexer.lexem += curr_char
                return Token(Tokens.tokenDict['OPE_IGUAL'], 'OPE_IGUAL', self.lexer.lexem, self.lexer.row,
                            self.lexer.col)

            else:
                self.lexer.back()
                return Token(Tokens.tokenDict['OPE_ATRI'], 'OPE_ATRI', self.lexer.lexem, self.lexer.row, self.lexer.col)

        else:
            Token(Tokens.tokenDict['ERR_UNK'], 'ERR_UNK', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateEight(State):
    def processState(self, curr_char):
        if (chr(32) <= curr_char <= chr(244)):
            self.lexer.lexem += curr_char
            curr_char = self.lexer.getNextChar()

            if curr_char == '\'':
                self.lexer.lexem += curr_char
                self.lexer.state = StateNine(self.lexer)

            else:
                while curr_char != '\'':
                    self.lexer.lexem += curr_char
                    curr_char = self.lexer.getNextChar()
                self.lexer.col += len(curr_char)
                Token(Tokens.tokenDict['ERR_CHR'], 'ERR_CHR', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateNine(State):  # Final State for CNST_CHAR
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['CNST_CHAR'], 'CNST_CHAR', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateTen(State):  # Final State for CNST_STRING
    def processState(self, curr_char):
        if chr(32) <= curr_char <= chr(244):
            self.lexer.lexem += curr_char


            if curr_char == '\"':
                self.lexer.col += 1
                return Token(Tokens.tokenDict['CNST_STR'], 'CNST_STR', self.lexer.lexem, self.lexer.row, self.lexer.col)

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_CHR'], 'ERR_CHR', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateEleven(State):  # State for process reserved words
    def processState(self, curr_char):
        if curr_char == '(' or not (LowerCase(curr_char).validate()) or Blank(curr_char).validate():
            if curr_char == 'N':
                self.lexer.lexem += curr_char
            else:
                self.lexer.back()
                self.lexer.state = StateTwelve(self.lexer)

        elif LowerCase(curr_char).validate():
            self.lexer.lexem += curr_char


class StateTwelve(State):  # Final state for reserved words
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        aux_category = aux_dict[self.lexer.lexem]
        if Tokens.tokenDict[aux_category] is not None:
            return Token(Tokens.tokenDict[aux_category], aux_category, self.lexer.lexem, self.lexer.row,
                     self.lexer.col)


        else:
            return Token(Tokens.tokenDict["ERR_PR"], "ERR_PR", self.lexer.lexem, self. lexer.row, self.lexer.col)
            self.lexer.back()
            self.lexer.col += 1



class StateThirteen(State):  # Estado comentários
    def processState(self, curr_char):
        self.lexer.newLine()
        self.lexer.content = self.lexer.txtline
        self.lexer.lexem = ''
        self.lexer.state = StateZero(self.lexer)


