from ply.yacc import yacc
from src.function_solver.core.expression_lexer import ExpressionLexer


class ExpressionParser:
    """
        A parser for mathematical expressions. This parser is built using the PLY (Python Lex-Yacc) library.
        It works in conjunction with the `ExpressionLexer` to validate and parse mathematical expressions.
        The parser handles arithmetic operations, functions (log, sqrt), and variables.
    """
    def __init__(self):
        """
            Initializes the parser. This sets up the lexer, defines the tokens, and initializes an empty list to store errors.
        """
        self.lexer_obj = ExpressionLexer()  # Create an instance of the ExpressionLexer
        self.tokens = self.lexer_obj.tokens
        self.errors = []
        self.parser = self.build()

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'POWER'),
        ('right', 'UMINUS'),
    )

    def p_expression(self, p):
        '''
        expression : term
                  | expression PLUS term
                  | expression MINUS term
        '''
        pass

    def p_term(self, p):
        '''
        term : factor
             | term TIMES factor
             | term DIVIDE factor
        '''
        pass

    def p_factor(self, p):
        '''
        factor : power
               | LOG LPAREN expression RPAREN
               | SQRT LPAREN expression RPAREN
        '''
        pass

    def p_power(self, p):
        '''
        power : atom
              | atom POWER power
        '''
        pass

    def p_atom(self, p):
        '''
        atom : NUMBER
             | VARIABLE
             | LPAREN expression RPAREN
             | MINUS atom %prec UMINUS
        '''
        pass

    def p_error(self, p):
        if p:
            self.errors.append(f"Syntax error at '{p.value}'")
        else:
            self.errors.append("Syntax error at end of expression")

    def build(self, **kwargs):
        self.lexer = self.lexer_obj.build()
        parser = yacc(module=self, **kwargs)
        return parser

    def validate(self, expression):
        self.errors = []

        # First, validate tokens using the lexer object's method
        tokens, lexer_errors = self.lexer_obj.tokenize(expression)
        self.errors.extend(lexer_errors)

        if not lexer_errors:
            # Then validate syntax
            try:
                self.parser.parse(expression)
            except Exception as e:
                self.errors.append(str(e))

        return {
            'is_valid': len(self.errors) == 0,
            'errors': self.errors,
        }