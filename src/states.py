from dictPyr import *
from tkn import *
from validate import *


class State (ABC):
    aux_dict = {'Initiate': "RESE_INITIATE", 'Halt': "RESE_HALT", 'Central': "RESE_CENTRAL", 'Funcao': "RESE_FUNCAO",
                'Retorna': "RESE_RETORNA", 'Int': "RESE_INT",'Str': "RESE_STR", 'Float': "RESE_FLOAT",
                'Char': "RESE_CHAR", 'Bool': "RESE_BOOL", "Array": "RESE_ARRAY", "Vazio": "RESE_VAZIO",
                'Verdade': "RESE_VERDADE", 'Falso': "RESE_FALSO", 'Se': "RESE_SE", 'SeNao': "RESE_SENAO",
                'Loop': "RESE_LOOP", "Enquanto": "RESE_ENQUANTO", "Nulo": "RESE_NULO", "Pare": "RESE_PARE",
                "Ler": "RESE_LER", "Escrever": "RESE_ESCREVER", "Escreverpl": "RESE_ESCREVERPL", "&": "OPE_CONJUN",
                "|": "OPE_DISJUN", "+": "OPE_ADI", "-": "OPE_SUB", "*": "OPE_MULTI",  "/": "OPE_DIV",
                "%": "OPE_REST", "=": "OPE_ATRI", "==": "OPE_IGUAL", "!=": "OPE_DIFE", "^": "OPE_POTEN",
                "<": "OPE_MENORQ", ">": "OPE_MAIORQ", "<=": "OPE_MENORI", ">=": "OPE_MAIORI", "!": "OPE_NEGA",
                "@": "OPE_CONCAT", '(': "DELI_OPAREN", ')': "DELI_CPAREN", ']': "DELI_ENBRA", '[': "DELI_OPBRA",
                ',': "DELI_COMMA", ';': "DELI_SECOL"}

    def __init__(self, lexer):
        self.lexer = lexer

    @abstractmethod
    def processState(self, curr_char):
        pass


class StateZero(State):
    def processState(self, curr_char):
        if Blank(curr_char).validate():
            self.lexer.state = 0

        elif LowerCase(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = 1

        elif Digit(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = 3

        elif Operator(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = 7

        elif curr_char == '\'':
            self.lexer.lexem += curr_char
            self.lexer.state = 8

        elif UpperCase(curr_char).validate():
            self.lexer.lexem += curr_char
            self.lexer.state = 11

        elif curr_char == '#':
            self.lexer.lexem += curr_char
            self.lexer.state = 13

        elif curr_char in ['+', '-', '*', '/', '%', '*', '@']:  # UNARINEG
            self.lexer.lexem += curr_char
            self.lexer.col += 1
            aux = self.aux_dict[curr_char]
            return Token(Tokens.tokenDict[aux], aux, self.lexer.lexem, self.lexer.row, self.lexer.col)

        elif curr_char in ['(', ')', '[', ']', ';', ',']:
            self.lexer.lexem += curr_char
            self.lexer.col += 1
            aux = self.aux_dict[curr_char]
            return Token(Tokens.tokenDict[aux], aux, self.lexer.lexem, self.lexer.row, self.lexer.col)

        else:
            Token(Tokens.tokenDict['ERR_UNK'], 'ERR_UNK',self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateOne(State):
    def processState(self, curr_char):
        if Operator(curr_char).validate() or Blank(curr_char).validate() or not Alphanum(curr_char).validate():
            self.lexer.back()
            self.lexer.state = 2

        elif Digit(curr_char).validate() or LowerCase(curr_char).validate() or UpperCase(curr_char).validate():
            self.lexer.lexem += curr_char

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_IND'], 'ERR_IND', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateTwo(State):
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['ID'], 'ID', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateThree(State):
    def processState(self, curr_char):
        if curr_char == '.':
            self.lexer.lexem += curr_char
            self.lexer.state = 4
            self.lexer.col = +1
        elif not Alphanum(curr_char).validate():
            self.lexer.back()
            self.lexer.state = 5
        elif Digit(curr_char).validate():
            self.lexer.lexem += curr_char
        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_NUMER'], 'ERR_NUMER', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateFour(State):
    def processState(self, curr_char):
        if Digit(curr_char).validate():
            self.lexer.lexem += curr_char

        elif Operator(curr_char).validate() or Blank(curr_char).validate() or not Alphanum(curr_char).validate():
            self.lexer.back()
            self.lexer.state = 6

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_NUMER'], 'ERR_NUMER',self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateFive(State):
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['CNST_INT'], 'CNST_INT', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateSix(State):
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['CNST_FLOAT'], 'CNST_FLOAT', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateSeven(State):
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
                return Token(Tokens.tokenDict['OPE_MENORI'], 'OPE_MENORI',self.lexer.lexem, self.lexer.row,
                             self.lexer.col)
            else:
                self.lexer.back()
                return Token(Tokens.tokenDict['OPE_MENORQ'], 'OPE_MENORQ',self.lexer.lexem, self.lexer.row,
                             self.lexer.col)

        elif curr_char == '!' or curr_char == '=':
            curr_char = self.lexer.getNextChar()
            self.lexer.col += 1

            if curr_char == '=':
                self.lexer.lexem += curr_char
                if self.lexer.lexem == '==':
                    return Token(Tokens.tokenDict['OPE_IGUAL'], 'OPE_IGUAL', self.lexer.lexem, self.lexer.row,
                                 self.lexer.col)
                else:
                    return Token(Tokens.tokenDict['OPE_DIFE'], 'OPE_DIFE', self.lexer.lexem, self.lexer.row,
                                 self.lexer.col)
            else:
                self.lexer.back()
                return Token(Tokens.tokenDict['OPE_ATRI'], 'OPE_ATRI', self.lexer.lexem, self.lexer.row, self.lexer.col)

        else:
            Token(Tokens.tokenDict['ERR_UNK'], 'ERR_UNK',self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateEight(State):
    def processState(self, curr_char):
        if chr(32) <= curr_char and curr_char <= chr(200):
            self.lexer.lexem += curr_char
            curr_char = self.lexer.getNextChar()

            if curr_char == '\'':
                self.lexer.lexem += curr_char
                self.lexer.state = 9

            else:
                self.lexer.back()
                self.lexer.state = 10

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_CHR'], 'ERR_CHR', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateNine(State):
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        return Token(Tokens.tokenDict['CNST_CHAR'], 'CNST_CHAR', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateTen(State):
    def processState(self, curr_char):
        if chr(32) <= curr_char <= chr(244):
            self.lexer.lexem += curr_char
            #print(self.lexer.lexem)

            if curr_char == '\'':
                self.lexer.col += 1
                return Token(Tokens.tokenDict['CNST_STR'], 'CNST_STR', self.lexer.lexem, self.lexer.row, self.lexer.col)

        else:
            self.lexer.col += 1
            Token(Tokens.tokenDict['ERR_CHR'], 'ERR_CHR', self.lexer.lexem, self.lexer.row, self.lexer.col)


class StateEleven(State):
    def processState(self, curr_char):
        if not (LowerCase(curr_char).validate()) or Blank(curr_char).validate():
            self.lexer.back()
            self.lexer.state = 12

        elif LowerCase(curr_char).validate():
            self.lexer.lexem += curr_char


class StateTwelve(State):
    def processState(self, curr_char):
        self.lexer.back()
        self.lexer.col += 1
        aux_category = self.aux_dict[self.lexer.lexem]
        if Tokens.tokenDict[aux_category] is not None:
            return Token(Tokens.tokenDict[aux_category], aux_category, self.lexer.lexem, self.lexer.row,
                         self.lexer.col)
        else:
            return Token(Tokens.tokenDict["ERR_PR"], "ERR_PR",self.lexer.lexem, self. lexer.row, self.lexer.col)
            self.lexer.back()
            self.lexer.col += 1



class StateThirteen(State):
    def processState(self, curr_char):
        self.lexer.newLine()
        self.lexer.content = self.lexer.txtline
        self.lexer.lexem = ''
        self.lexer.state = 0
