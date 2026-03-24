from enum import Enum

class TokenType(Enum):
    PRINT = 0
    INTDEC = 1
    FLOATDEC = 2
    INTLIT = 3
    FLOATLIT = 4
    VARREF = 5
    ASSIGN = 6
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    EXPONENT = '^'
    LPAREN = 12
    RPAREN = 13
    EOF = 14
    EOTS = 15



class Token:

    def __init__(
        self, 
        tokentype: TokenType, 
        lexeme: str,
        *,  
        name: str | None = None,
        value: int | None = None,
        numtype: str | None = None,
    ):

        self.tokentype = tokentype
        self.lexeme = lexeme
        self.name = name
        self.value = value
        self.numtype = numtype

    def __str__(self):
        namepart = f"; name: {self.name}" if self.name is not None else ""
        valpart = f";  val: {str(self.value)}" if self.value is not None else ""

        return f"[Token type: {self.tokentype}; lexeme: {self.lexeme}{namepart}{valpart}]"

    def __repr__(self):
        return self.__str__()
    
