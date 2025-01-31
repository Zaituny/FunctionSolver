import ply.lex as lex


class ExpressionLexer:
    """
        A lexer for tokenizing mathematical expressions. This lexer is built using the PLY (Python Lex-Yacc) library.
        It can handle numbers, basic arithmetic operators, parentheses, and functions like log and sqrt.
    """
    tokens = (
        'NUMBER',   # Represents numeric literals (e.g., 123, 45.67)
        'PLUS',     # Represents the addition operator '+'
        'MINUS',    # Represents the subtraction operator '-'
        'TIMES',    # Represents the multiplication operator '*'
        'DIVIDE',   # Represents the division operator '/'
        'POWER',    # Represents the power operator '^'
        'LPAREN',   # Represents the left parenthesis '('
        'RPAREN',   # Represents the right parenthesis ')'
        'LOG',      # Represents the log function
        'SQRT',     # Represents the square root function
        'VARIABLE'  # Represents variables (e.g., x, y, z)
    )

    t_PLUS = r'\+'    # Regular expression for the PLUS token
    t_MINUS = r'-'    # Regular expression for the MINUS token
    t_TIMES = r'\*'   # Regular expression for the TIMES token
    t_DIVIDE = r'/'   # Regular expression for the DIVIDE token
    t_POWER = r'\^'   # Regular expression for the POWER token
    t_LPAREN = r'\('  # Regular expression for the LPAREN token
    t_RPAREN = r'\)'  # Regular expression for the RPAREN token
    t_LOG = r'log'    # Regular expression for the LOG token
    t_SQRT = r'sqrt'  # Regular expression for the SQRT token
    t_ignore = ' \t'  # Ignore whitespace characters

    def __init__(self):
        """
            Initializes the lexer. This sets up the lexer and initializes an empty list to store errors.
        """
        self.errors = []  # List to store any errors encountered during tokenization
        self.lexer = self.build()  # Build the lexer

    def t_VARIABLE(self, t):
        r'[a-zA-Z][a-zA-Z0-9]*'  # Regular expression for variable names
        if len(t.value) > 1:  # If the variable name has more than one character
            if t.value == 'log':
                t.type = 'LOG'  # If the variable is 'log', treat it as a LOG token
            elif t.value == 'sqrt':
                t.type = 'SQRT'  # If the variable is 'sqrt', treat it as a SQRT token
            else:
                self.errors.append(f"Invalid variable '{t.value}'")  # Add an error for invalid variable names
        elif len(t.value) == 1 and t.value != 'x':
            self.errors.append(f"Invalid variable '{t.value}'")  # restrict the variables to 'x'
        return t

    def t_NUMBER(self, t):
        r'\d*\.?\d+' # Regular expression for numbers (e.g., 123, 45.67)
        return t

    def t_error(self, t):
        self.errors.append(f"Invalid character '{t.value[0]}'") # Add the error to the errors list
        t.lexer.skip(1) # Skip the invalid character

    def build(self, **kwargs):
        self.errors = []  # Reset the errors list
        self.lexer = lex.lex(module=self, **kwargs)  # Build the lexer using the current module
        return self.lexer

    def tokenize(self, data):
        self.errors = []  # Reset the errors list
        self.lexer.input(data)  # Provide the input data to the lexer
        tokens = []  # List to store the token types
        while True:
            tok = self.lexer.token()  # Get the next token
            if not tok:
                break  # If no more tokens, exit the loop
            tokens.append(tok.type)  # Add the token type to the list
        return tokens, self.errors # Return the list of tokens and any errors
