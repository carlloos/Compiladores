
class Token():
    def __init__(self, category, lexem, row, col):
        self.category = category
        self.lexem = lexem
        self.row = row
        self.col = col

    def to_str(self):
        return f"[{self.row - 1},{self.col}] ({self.category}) {{{self.lexem}}}"