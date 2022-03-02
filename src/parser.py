from lex import *
from validate import *
import sys


eps = "epsilon"


class Parser:
    def __init__(self):
        self.lex = Lexer(sys.argv[1])
        self.curr = self.lex.nextToken()
        self.lookahead = self.lex.lexem
        self.l1category = self.curr.category
        self.ident = "          "
        self.S()


    def printError(self, exceptmessage):
        print('Error: Expecting ' + exceptmessage)



    def updateToken(self):
        self.curr = self.lex.nextToken()
        self.lookahead = self.lex.lexem
        self.l1category = self.curr.category

    def printProd(self, a, b):
        print(self.ident + a + " = " + b)

    def S(self):
        if (self.l1category == "RESE_FUNCAO" or IsType(self.l1category).check() or IsConst(self.l1category).check()):
            if self.l1category == "RESE_FUNCAO":
                self.printProd("S", "FunDecla S")
                self.FunDecla()

            elif IsType(self.l1category).check() or IsConst(self.l1category).check():
                self.printProd("S,", "VarDecla S")
                print(self.curr.toString())
                self.VarDecla()

            else:
                self.printError('int, float, bool, char, str, func ou const')

            self.S()

        elif self.l1category == "DELI_EOF":
            self.printProd("S", eps)
            print(self.curr.toString())

        else:
            self.printError('int, float, bool, char, str, func, const, id ou eof')


    def FunDecla(self):

        if(self.l1category == "RESE_FUNCAO"):
            self.printProd("FunDecla", "'function' TipoFun FunNome '(' ParamsDecla ')' DelimiDecla")
            print(self.curr.toString())
            self.updateToken()

            self.TipoFun()
            self.FunNome()


            if(self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.ParamDecla()
                if(self.l1category == "DELI_CPAREN"):
                    print(self.curr.toString())
                    self.updateToken()
                    self.DelimiDecla()
                else:
                    print(self.lookahead)
                    self.printError(')')
            else:
                self.printError('(')
        else:
            print("erro FUNCAO")

    def TipoFun(self):
        if self.l1category == "RESE_VAZIO":
            self.printProd("TipoFun", "'void'")
            print(self.curr.toString())
            self.updateToken()

        elif IsType(self.l1category).check():
            self.printProd("TipoFun", "Tipo")
            self.Tipo()

        else:
            self.printError('int, float, char, bool ou str')

    def FunNome(self):
        if self.l1category == "RESE_CENTRAL":
            self.printProd("FunNome", "'Central'")
            print(self.curr.toString())
            self.updateToken()
        elif self.l1category == "ID":
            self.printProd("FunNome", "'id'")
            print(self.curr.toString())
            self.updateToken()
        else:
            self.printError('funcao central ou id')

    def Tipo(self):
        if self.l1category == "RESE_FLOAT":
            self.printProd("Tipo", "'Float'")
            print(self.curr.toString())

        elif self.l1category == "RESE_INT":
            self.printProd("Tipo", "'Int'")
            print(self.curr.toString())

        elif self.l1category == "RESE_CHAR":
            self.printProd("Tipo", "'Char'")
            print(self.curr.toString())

        elif self.l1category == "RESE_STR":
            self.printProd("Tipo", "'Str'")
            print(self.curr.toString())

        elif self.l1category == "RESE_BOOL":
            self.printProd("Tipo", "'Bool'")
            print(self.curr.toString())

        else:
            self.printError('int, float, char, bool ou str')

        self.updateToken()

    def ParamDecla(self):
        if IsType(self.l1category).check():
            self.printProd("ParamDecla", " Tipo 'id' Arr LParamDecla")
            print(self.curr.toString())
            self.updateToken()

            if self.l1category == "ID":
                print(self.curr.toString())
                self.updateToken()
                self.Array()
                self.LParamDecla()
            else:
                self.printError('id')
        else:
            self.printProd("ParamDecla", eps)

    def LParamDecla(self):
        if self.l1category == "DELI_COMMA":
            self.printProd("LParamDecla", "',' ParamDecla")
            print(self.curr.toString())
            self.updateToken()
            self.ParamDecla()
        else:
            self.printProd("LParamDecla", eps)

    def ParamCall(self):
        if IsEconcFirst(self.l1category).check():
            self.printProd("ParamCall", "ExpC LParamCall")
            self.ExpC()
            self.LParamCall()

        else:
            self.printProd("ParamCall", eps)

    def LParamCall(self):
        if self.l1category == "DELI_COMMA":
            self.printProd("LParamCall", "',' ParamCall")
            print(self.curr.toString())
            self.updateToken()
            self.ParamCall()
        else:
            self.printProd("LParamCall", eps)

    def IdOrFun(self):
        if self.l1category == "ID":
            self.printProd("IdOrFun", "'id' FuncCallArr")
            print(self.curr.toString())
            self.updateToken()
            self.FuncCallArr()

    def FuncCallArr(self):
        if self.l1category == "DELI_OPAREN":
            self.printProd("FuncCallArr", "'(' ParamCall ')'")
            print(self.curr.toString())
            self.updateToken()
            self.ParamCall()

            if self.l1category == "DELI_CPAREN":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(')')

        elif self.l1category == "DELI_OPBRA":
            self.printProd("FuncCallArr", "'[' ExpA ']'")
            print(self.curr.toString())
            self.updateToken()
            self.ExpA()

            if self.l1category == "DELI_ENBRA":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(']')

        else:
            self.printProd("FuncCallArr", eps)

    def FuncCallAtrib(self):
        if self.l1category == "DELI_OPAREN":
            self.printProd("FuncCallAtrib", "FuncCall")
            print(self.curr.toString()) # talvez falte next token
            self.FuncCall()
        elif self.l1category == "OPE_ATRI" or self.l1category == "DELI_OPBRA":
            self.printProd("FuncCallAtrib", "LAtrib")
            self.LAtrib()

    def FuncCall(self):
        if self.l1category == "DELI_OPAREN":
            self.printProd("FuncCall", "'(' ParamCall ')' ';'")
            print(self.curr.toString())
            self.updateToken()
            self.ParamCall()

            if self.l1category == "DELI_CPAREN":
                print(self.curr.toString())
                self.updateToken()
                if self.l1category == "DELI_SECOL":
                    print(self.curr.toString())
                    self.updateToken()
                else:
                    self.printError(';')
            else:
                self.printError(')')
        else:
            self.printError('(')



    def LAtrib(self):
        self.printProd("LAtrib", "IdArr Atr")
        self.IdArr()
        self.Atr()
        if self.l1category == "DELI_SECOL":
            print(self.curr.toString())
            self.updateToken()

        else:
            self.printError(';')


    def DelimiDecla(self):
        if self.l1category == "RESE_INITIATE":
            self.printProd("DelimiDecla", "'Initiate' Instru 'Halt'")
            print(self.curr.toString())
            self.updateToken()
            self.Instru()

            if self.l1category == "RESE_HALT":
                print(self.curr.toString())
                self.updateToken()

            else:
                self.printError('Halt')
        else:
            self.printError('Initiate')

    def Array(self):
        if self.l1category == "DELI_OPBRA":
            self.printProd("Array", "'[' ']'")
            print(self.curr.toString())
            self.updateToken()

            if self.l1category == "DELI_ENBRA":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(']')


        else:
            self.printProd("Arr", eps)

    def IdArr(self):
        if self.l1category == "DELI_OPBRA":
            self.printProd("IdArr", "ExpA")
            print(self.curr.toString())
            self.updateToken()
            self.ExpA()

            if self.l1category == "DELI_ENBRA":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(']')


        else:
            self.printProd("IdArr", eps)

    def Instru(self):
        if(IsType(self.l1category).check()):
            self.printProd("Instru", "VarDecla Instru")
            self.VarDecla()
            self.Instru()

        elif IsCMD(self.l1category).check():
            self.printProd("Instru", "Comando Instru")
            self.Comando()
            self.Instru()

        elif self.l1category == 'ID':
            self.printProd("Instru", "FuncCallAtrib Instru")

            print(self.curr.toString())
            self.updateToken()

            self.FuncCallAtrib()
            self.Instru()

        else:
            self.printProd("Instru",  eps)

    def Comando(self):

        if self.l1category == "RESE_ESCREVER":
            self.printProd("Comando", "'Escrever' '(' ParamCall ')' ';'")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.ParamCall()

                if (self.l1category == "DELI_CPAREN"):
                    print(self.curr.toString())
                    self.updateToken()
                    if (self.l1category == "DELI_SECOL"):
                        print(self.curr.toString())
                        self.updateToken()
                    else:
                        self.printError(';')

        elif self.l1category == "RESE_ESCREVERPL":
            self.printProd("Comando", "'Escreverpl' '(' ParamCall ')' ';'")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.ParamCall()

                if (self.l1category == "DELI_CPAREN"):
                    print(self.curr.toString())
                    self.updateToken()
                    if (self.l1category == "DELI_SECOL"):
                        print(self.curr.toString())
                        self.updateToken()
                    else:
                        self.printError(';')

        elif self.l1category == "RESE_LER":
            self.printProd("Comando", "'Ler' '(' Ler ')' ';'")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.Ler()

                if (self.l1category == "DELI_CPAREN"):
                    print(self.curr.toString())
                    self.updateToken()
                    if (self.l1category == "DELI_SECOL"):
                        print(self.curr.toString())
                        self.updateToken()
                    else:
                        self.printError(';')

                else:
                    self.printError(')')
            else:
                self.printError('(')

        elif self.l1category == "RESE_ENQUANTO":
            self.printProd("Comando", "'Enquanto' '(' ExpEB ')' DelimiDecla")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.ExpEB()

                if (self.l1category == "DELI_CPAREN"):
                    print(self.curr.toString())
                    self.updateToken()
                    self.DelimiDecla()

                else:
                    self.printError(')')
            else:
                self.printError('(')

        elif self.l1category == "RESE_SE":
            self.printProd("Comando", "'Se' '(' ExpEB ')' DelimiDecla Else")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.ExpEB()

                if (self.l1category == "DELI_CPAREN"):
                    print(self.curr.toString())
                    self.updateToken()
                    self.DelimiDecla()
                    self.Else()

                else:
                    self.printError(')')
            else:
                self.printError('(')

        elif self.l1category == "RESE_PARE":
            self.printProd("Comando", "'Pare';'")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_SECOL"):
                print(self.curr.toString())
                self.updateToken()


            else:
                self.printError(';')

        elif self.l1category == "RESE_RETORNA":
            self.printProd("Comando", "'Retorna' Return ';' Instru")
            print(self.curr.toString())
            self.updateToken()
            self.Return()

            if (self.l1category == "DELI_SECOL"):
                print(self.curr.toString())
                self.updateToken()
                self.Instru()
            else:
                self.printError(';')

        elif self.l1category == "RESE_LOOP":
            self.printProd("Comando", "'Loop' '(' Int ',' Int ',' Int ',' Incremen ')' DelimiDecla")
            print(self.curr.toString())
            self.updateToken()

            if (self.l1category == "DELI_OPAREN"):
                print(self.curr.toString())
                self.updateToken()
                self.Int()

                if (self.l1category == "DELI_COMMA"):
                    print(self.curr.toString())
                    self.updateToken()
                    self.Int()
                    if (self.l1category == "DELI_COMMA"):
                        print(self.curr.toString())
                        self.updateToken()
                        self.Int()
                        if (self.l1category == "DELI_COMMA"):
                            print(self.curr.toString())
                            self.updateToken()
                            self.Incr()

                            if (self.l1category == "DELI_CPAREN"):
                                print(self.curr.toString())
                                self.updateToken()
                                self.DelimiDecla()

                            else:
                                self.printError(')')

                    else:
                        self.printError(',')

                else:
                    self.printError(',')
            else:
                self.printError('(')

    def Return(self):
        if self.l1category == "RESE_RETORNA":
            self.printProd("Return", "'Retorna' Retorna ';'")
            print(self.curr.toString())
            self.updateToken()
            self.Retorna()
            if (self.l1category == "DELI_SECOL"):
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(';')

    def Retorna(self):
        if IsEconcFirst(self.l1category).check():
            self.printProd("Retorna", "ExpC")
            self.ExpC()
            if (self.l1category == "DELI_SECOL"):
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printProd("Retorna", eps)


    def Int(self):
        if self.l1category == "ID":
            self.printProd("Int", " 'id' ';'")
            print(self.curr.toString())
            self.updateToken()
        elif self.l1category == "RESE_INT":
            self.printProd("Int", "'Int' 'id' ';'")
            print(self.curr.toString())
            self.updateToken()

            if self.l1category == "ID":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError('id')

        elif self.l1category == "CNST_INT":
            self.printProd("Int", "'CNST_INT'")
            print(self.curr.toString())
            self.updateToken()

    def Incr(self):
        if self.l1category == "DELI_COMMA":
            self.printProd("Int", " ',' Int")
            print(self.curr.toString())
            self.updateToken()
            self.Int()

        else:
            self.printProd("Int", eps)
            self.updateToken()

    def Ler(self):
        self.printProd("Ler", " Id LLer")
        self.Id()
        self.LLer()

    def Id(self):
        self.printProd("Id", " 'id' ArrId")
        print(self.curr.toString())
        self.updateToken()
        self.IdArr()

    def LLer(self):
        if self.l1category == "DELI_COMMA":
            self.printProd("LLer", " ',' Ler")
            print(self.curr.toString())
            self.updateToken()
            self.Ler()

        else:
            self.printProd("LLer", eps)

    def Else(self):
        if self.l1category == "RESE_SENAO":
            print(self.curr.toString())
            self.updateToken()
            self.DelimiDecla()

        else:
            self.printProd("Else", eps)

    def ExpA(self):
        self.printProd("ExpA", "Tiparit LExpA")
        self.Tiparit()
        self.LExpA()

    def LExpA(self):
        if self.l1category == "OPE_ADI" or self.l1category == "OPE_SUB":
            self.printProd("LExpA", "OpArit Tiparit LExpA")
            self.OpeAri()
            self.Tiparit()
            self.LExpA()
        else:
            self.printProd("LExpA", eps)

    def Tiparit(self):
        self.printProd("Tiparit", "Parit LTiparit")
        self.Parit()
        self.LTiparit()

    def LTiparit(self):
        if self.l1category == "OPE_MULTI" or self.l1category == "OPE_DIV":
            self.printProd("LTiparit", "OpeMulti Parit LTiparit")
            self.OpeMulti()
            self.Parit()
            self.LTiparit()
        else:
            self.printProd("LTiparit", eps)

    def Parit(self):
        self.printProd("Parit", "Farit LParit")
        self.Farit()
        self.LParit()

    def LParit(self):
        if self.l1category == "OPE_REST" or self.l1category == "OPE_POTEN":
            self.printProd("LParit", "OpePoten Parit")
            self.OpePoten()
            self.Parit()
        else:
            self.printProd("LParit", eps)

    def Farit(self):
        if self.l1category == "OPE_ADI" or self.l1category == "OPE_SUB":
            self.printProd("Farit", "OpeAri LFarit")
            self.OpeAri()
            self.LFarit()
        else:
            self.printProd("Farit", "LFarit")
            self.LFarit()

    def LFarit(self):

        if self.l1category == "ID":
            self.printProd("LFarit", "IdOrFun")
            self.IdOrFun()

        elif IsConst(self.l1category).check():
            self.printProd("LFarit", "Cte")
            self.Cte()

        elif self.l1category == "DELI_OPAREN":
            self.printProd("LFarit", "'(' ExpC ')'")
            print(self.curr.toString())
            self.updateToken()
            self.ExpC()

            if self.l1category == "DELI_CPAREN":
                print(self.curr.toString())
                self.updateToken()

            else:
                self.printError(')')

    def ExpC(self):
        self.printProd("ExpC", "ExpEB LExpC")
        self.ExpEB()
        self.LExpC()

    def LExpC(self):
        if self.l1category == "OPE_CONCAT":
            self.printProd("LexpC", "'OPE_CONCAT' ExpEB LexpC")
            print(self.curr.toString())
            self.updateToken()
            self.ExpEB()
            self.LExpC()
        else:
            self.printProd("LexpC", eps)

    def ExpEB(self):
        self.printProd("ExpEB", "ExpOuB LExpEB")
        self.ExpOuB()
        self.LExpEB()

    def LExpEB(self):
        if self.l1category == "OPE_DISJUN":
            self.printProd("LExpEB", "'OPE_DISJUN' ExpOuB LExpEB")
            print(self.curr.toString())
            self.updateToken()
            self.ExpOuB()
            self.LExpEB()
        else:
            self.printProd("EboolX", eps)

    def ExpOuB(self):
        self.printProd("ExpOuB", "ExpNB LExpOuB")
        self.ExpNB()
        self.LExpOuB()

    def LExpOuB(self):
        if self.l1category == "OPE_CONJUN":
            self.printProd("LExpOuB", "'OPE_CONJUN' ExpNB LExpOuB")
            print(self.curr.toString())
            self.updateToken()
            self.ExpNB()
            self.LExpOuB()
        else:
            self.printProd("ExpOuB", eps)

    def ExpNB(self):
        if self.l1category == "OPE_NEGA":
            self.printProd("ExpNB", "'OPE_NEGA' Tiprelac")
            print(self.curr.toString())
            self.updateToken()
            self.Tiprelac()
        else:
            self.printProd("ExpNB", "Tiprelac")
            self.Tiprelac()


    def Tiprelac(self):
        self.printProd("Tiprelac", "ExpA LTiprelac")
        self.ExpA()
        self.LTiprelac()

    def LTiprelac(self):
        if IsRela(self.l1category).check():
            self.printProd("LTiprelac", "OpeRela ExpA LTiprelac")
            self.OpeRela()
            self.ExpA()
            self.LTiprelac()
        else:
            self.printProd("LTiprelac", eps)



    def OpeRela(self):

        if self.l1category == "OPE_MAIORQ":
            self.printProd("OpeRela", "'OPE_MAIORQ'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "OPE_MENORQ":
            self.printProd("OpeRela", "'OPE_MENORQ'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "OPE_MAIORI":
            self.printProd("OpeRela", "'OPE_MAIORI'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "OPE_MENORI":
            self.printProd("OpeRela", "'OPE_MENORI'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "OPE_IGUAL":
            self.printProd("OpeRela", "'OPE_IGUAL'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "OPE_DIFE":
            self.printProd("OpeRela", "'OPE_DIFE'")
            print(self.curr.toString())
            self.updateToken()

        else:
            self.printError('relacional operator')


    def OpePoten(self):
        if self.l1category == "OPE_REST":
            self.printProd("OpePoten", "'OPE_REST'")
            print(self.curr.toString())

        elif self.l1category == "OPE_POTEN":
            self.printProd("OpePoten", "'OPE_POTEN'")
            print(self.curr.toString())

        self.updateToken()


    def OpeAri(self):
        if self.l1category == "OPE_ADI":
            self.printProd("OpeAri", "'OPE_ADI'")
            print(self.curr.toString())

        elif self.l1category == "OPE_SUB":
            self.printProd("OpeAri", "'OPE_SUB'")
            print(self.curr.toString())

        self.updateToken()

    def OpeMulti(self):
        if self.l1category == "OPE_MULTI":
            self.printProd("OpeMulti", "'OPE_MULTI'")
            print(self.curr.toString())

        elif self.l1category == "OPE_DIV":
            self.printProd("OpeMulti", "'OPE_DIV'")
            print(self.curr.toString())

        self.updateToken()


    def Cte(self):

        if self.l1category == "CNST_INT":
            self.printProd("Cte", "'CNST_INT'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "CNST_FLOAT":
            self.printProd("Cte", "'CNST_FLOAT'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "CNST_CHAR":
            self.printProd("Cte", "'CNST_CHAR'")
            print(self.curr.toString())
            self.updateToken()


        elif self.l1category == "CNST_STR":
            self.printProd("Cte", "'CNST_STR'")
            print(self.curr.toString())
            self.updateToken()

        elif self.l1category == "CNST_BOOL" or self.l1category == "RESE_VERDADE" or self.l1category == "RESE_FALSO":
            self.printProd("Cte", "'CNST_BOOL'")
            print(self.curr.toString())
            self.updateToken()

        else:
            self.printError('literal constant')


    def Atr(self):
        if self.l1category == "OPE_ATRI":
            self.printProd("Atr", " '=' ExpCArr")
            print(self.curr.toString())
            self.updateToken()

            self.EconcOuListArr()

        else:
            self.printProd("Atr", eps)

    def EconcOuListArr(self):
        if IsEconcFirst(self.l1category):
            self.printProd("ExpCArr", "ExpC")
            self.ExpC()

        elif self.l1category == "DELI_OPBRA":
            self.printProd("ExpCArr", "ArrS")
            print(self.curr.toString())
            self.updateToken()

            self.ArrS()

            if self.lookahead == "DELI_ENBRA":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(']')
        else:
            self.printError('[')

    def ArrS(self):
        self.printProd("ArrS", "ExpC LArrS")
        self.ExpC()
        self.LArrS()

    def LArrS(self):
        if self.l1category == "DELI_COMMA":
            self.printProd("LArrS = ", "',' ArrS")
            print(self.curr.toString())
            self.updateToken()

            self.ArrS()

        else:
            self.printProd("LArrS", eps)

    def ListId(self):
        self.printProd("ListId", "AtribOuId ListIdX")
        self.AtrId()
        self.ListIdX()

    def ListIdX(self):
        if self.l1category == "DELI_COMMA":
            self.printProd("ListIdX = ", "',' ListId")
            print(self.curr.toString())
            self.updateToken()

            self.ListId()

        else:
            self.printProd("ListIdX", eps)

    def AtrId(self):
        if self.l1category == "ID":
            self.printProd("AtrId = ", "'id' IdArr Atr")
            print(self.curr.toString())
            self.updateToken()

            self.IdArr()
            self.Atr()

        else:
            self.printError('id')

    def VarDecla(self):
        if IsType(self.l1category):
            self.printProd("VarDecla", "Tipo ListId ';'")
            self.Tipo()
            self.ListId()

            if self.l1category == "DELI_SECOL":
                print(self.curr.toString())
                self.updateToken()
            else:
                self.printError(';')

        else:
            self.printError('int, float, bool, char ou str')


Parser()
