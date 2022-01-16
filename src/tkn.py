
class Token():
    def __init__(self, num, category, lexem, row, col):
        self.category = category
        self.num = num
        self.lexem = lexem
        self.row = row
        self.col = col

    def toString(self):
        printmessage = "              [{:>4}, {:>4}] ({:>4}, {:>20}) (" +self.lexem+")"
        return (printmessage.format(self.row - 1, self.col, self.num, self.category))