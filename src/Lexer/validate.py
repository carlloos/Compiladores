from abc import ABC, abstractmethod


class Validation(ABC):
    def __init__(self, string):
        self.string = string

    @abstractmethod
    def validate(self):
        pass


class UpperCase(Validation):

    def validate(self):
        return self.string.isupper()


class LowerCase(Validation):
    def validate(self):
        return self.string.islower()


class Digit(Validation):
    def validate(self):
        return self.string.isdigit()


class Operator(Validation):
    def validate(self):
        return self.string in ['>', '<', '=', '!']


class Blank(Validation):
    def validate(self):
        return self.string.isspace()


class Letter(Validation):
    def validate(self):
        return self.string.isalpha()


class Alphanum(Validation):
    def validate(self):
        return self.string.isalpha() or self.string.isdigit()


class Check(ABC):
    def __init__(self, category):
        self.category = category

    @abstractmethod
    def check(self):
        pass


class IsType(Check):
    def check(self):
        if self.category in ["RESE_INT", "RESE_VAZIO", "RESE_FLOAT", "RESE_STR", "RESE_BOOL", "RESE_CHAR"]:
            return True
        return False


class IsConst(Check):
    def check(self):
        if self.category in ["CNST_INT", "CNST_FLOAT", "CNST_STR", "CNST_BOOL", "CNST_CHAR", "RESE_VERDADE",
                             "RESE_FALSO"]:
            return True

        return False


class IsEconcFirst(Check):
    def check(self):
        if self.category in ["ID", "OPE_ADI", "OPE_SUB", "DELI_OPAREN"] or IsConst(self.category).check():
            return True
        return False


class IsCMD(Check):
    def check(self):
        if self.category in ["RESE_SE", "RESE_ENQUANTO", "RESE_LOOP", "RESE_PARE", "RESE_RETORNA", "RESE_ESCREVER",
                             "RESE_ESCREVERPL", "RESE_LER"]:
            return True
        return False


class IsRela(Check):
    def check(self):
        if self.category in ["OPE_MAIORQ", "OPE_MAIORI", "OPE_MENORI", "OPE_MENORQ", "OPE_IGUAL", "OPE_DIFE"]:
            return True
        else:
            return False
