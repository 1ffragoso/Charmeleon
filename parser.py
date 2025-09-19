class ASTNode:
    def __init__(self, type, value=None, children=None, metadata=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"ASTNode(type=\'{self.type}\' value={self.value!r} children={self.children} metadata={self.metadata})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def advance(self):
        self.current_token_index += 1
        self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type, token_value=None):
        if self.current_token and self.current_token["type"] == token_type and \
           (token_value is None or self.current_token["value"] == token_value):
            self.advance()
        else:
            raise Exception(f"Erro de sintaxe: Esperado {token_type} (valor: {token_value}), mas encontrou {self.current_token}")

    def parse(self):
        return self.program()

    def program(self):
        nodes = []
        while self.current_token:
            if self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "func":
                nodes.append(self.function_declaration())
            else:
                # Agora permite instruções no topo do programa
                nodes.append(self.statement())
        return ASTNode("Program", children=nodes)

    def function_declaration(self):
        self.eat("KEYWORD", "func")
        name = self.current_token["value"]
        self.eat("IDENTIFIER")
        self.eat("DELIMITER", "(")
        params = self.parameter_list()
        self.eat("DELIMITER", ")")
        return_type = None
        if self.current_token and self.current_token["value"] == "->":
            self.eat("OPERATOR", "->")
            return_type = self.current_token["value"]
            self.eat("KEYWORD") # int, float, bool, string
        self.eat("DELIMITER", "{")
        body = self.block()
        self.eat("DELIMITER", "}")
        return ASTNode("FunctionDeclaration", value=name, children=[params, body], metadata={"return_type": return_type})

    def parameter_list(self):
        params = []
        while self.current_token and self.current_token["type"] != "DELIMITER" and self.current_token["value"] != ")":
            name = self.current_token["value"]
            self.eat("IDENTIFIER")
            self.eat("DELIMITER", ":")
            param_type = self.current_token["value"]
            self.eat("KEYWORD") # int, float, bool, string
            params.append(ASTNode("Parameter", value=name, metadata={"type": param_type}))
            if self.current_token and self.current_token["value"] == ",":
                self.eat("DELIMITER", ",")
        return ASTNode("ParameterList", children=params)

    def block(self):
        statements = []
        while self.current_token and not (self.current_token["type"] == "DELIMITER" and self.current_token["value"] == "}"):
            statements.append(self.statement())
        return ASTNode("Block", children=statements)

    def statement(self):
        if self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "var":
            return self.variable_declaration()
        elif self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "if":
            return self.if_statement()
        elif self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "for":
            return self.for_statement()
        elif self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "while":
            return self.while_statement()
        elif self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "return":
            return self.return_statement()
        elif self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "print":
            return self.print_statement()
        elif self.current_token["type"] == "IDENTIFIER":
            return self.assignment_statement()
        else:
            raise Exception(f"Declaração de instrução inesperada: {self.current_token}")

    def variable_declaration(self):
        self.eat("KEYWORD", "var")
        name = self.current_token["value"]
        self.eat("IDENTIFIER")
        var_type = None
        if self.current_token and self.current_token["value"] == ":":
            self.eat("DELIMITER", ":")
            var_type = self.current_token["value"]
            self.eat("KEYWORD") # int, float, bool, string
        self.eat("ASSIGN", "=")
        expression = self.expression()
        self.eat("DELIMITER", ";")
        return ASTNode("VariableDeclaration", value=name, children=[expression], metadata={"type": var_type})

    def assignment_statement(self):
        name = self.current_token["value"]
        self.eat("IDENTIFIER")
        self.eat("ASSIGN", "=")
        expression = self.expression()
        self.eat("DELIMITER", ";")
        return ASTNode("AssignmentStatement", value=name, children=[expression])

    def if_statement(self):
        self.eat("KEYWORD", "if")
        self.eat("DELIMITER", "(")
        condition = self.expression()
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", "{")
        true_block = self.block()
        self.eat("DELIMITER", "}")
        false_block = None
        if self.current_token and self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "else":
            self.eat("KEYWORD", "else")
            if self.current_token and self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "if":
                false_block = self.if_statement() # else if
            else:
                self.eat("DELIMITER", "{")
                false_block = self.block()
                self.eat("DELIMITER", "}")
        return ASTNode("IfStatement", children=[condition, true_block, false_block])

    def for_statement(self):
        self.eat("KEYWORD", "for")
        self.eat("DELIMITER", "(")
        # For init: can be a var declaration or an assignment, but without trailing semicolon
        init = None
        if self.current_token and self.current_token["type"] == "KEYWORD" and self.current_token["value"] == "var":
            init = self._variable_declaration_no_semicolon()
        elif self.current_token and self.current_token["type"] == "IDENTIFIER":
            init = self._assignment_statement_no_semicolon()
        self.eat("DELIMITER", ";")

        condition = self.expression()
        self.eat("DELIMITER", ";")

        # For update: can be an assignment, but without trailing semicolon
        update = None
        if self.current_token and self.current_token["type"] == "IDENTIFIER":
            update = self._assignment_statement_no_semicolon()
        
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", "{")
        body = self.block()
        self.eat("DELIMITER", "}")
        return ASTNode("ForStatement", children=[init, condition, update, body])

    def _variable_declaration_no_semicolon(self):
        self.eat("KEYWORD", "var")
        name = self.current_token["value"]
        self.eat("IDENTIFIER")
        var_type = None
        if self.current_token and self.current_token["value"] == ":":
            self.eat("DELIMITER", ":")
            var_type = self.current_token["value"]
            self.eat("KEYWORD") # int, float, bool, string
        self.eat("ASSIGN", "=")
        expression = self.expression()
        return ASTNode("VariableDeclaration", value=name, children=[expression], metadata={"type": var_type})

    def _assignment_statement_no_semicolon(self):
        name = self.current_token["value"]
        self.eat("IDENTIFIER")
        self.eat("ASSIGN", "=")
        expression = self.expression()
        return ASTNode("AssignmentStatement", value=name, children=[expression])

    def while_statement(self):
        self.eat("KEYWORD", "while")
        self.eat("DELIMITER", "(")
        condition = self.expression()
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", "{")
        body = self.block()
        self.eat("DELIMITER", "}")
        return ASTNode("WhileStatement", children=[condition, body])

    def return_statement(self):
        self.eat("KEYWORD", "return")
        expression = self.expression()
        self.eat("DELIMITER", ";")
        return ASTNode("ReturnStatement", children=[expression])

    def print_statement(self):
        self.eat("KEYWORD", "print")
        self.eat("DELIMITER", "(")
        expression = self.expression()
        self.eat("DELIMITER", ")")
        self.eat("DELIMITER", ";")
        return ASTNode("PrintStatement", children=[expression])

    def expression(self):
        return self.comparison()

    def comparison(self):
        node = self.arithmetic()
        while self.current_token and self.current_token["type"] == "OPERATOR" and self.current_token["value"] in ["==", "!=", "<=", ">=", "<", ">"]:
            op = self.current_token["value"]
            self.eat("OPERATOR")
            right = self.arithmetic()
            node = ASTNode("BinaryExpression", value=op, children=[node, right])
        return node

    def arithmetic(self):
        node = self.term()
        while self.current_token and self.current_token["type"] == "OPERATOR" and self.current_token["value"] in ["+", "-"]:
            op = self.current_token["value"]
            self.eat("OPERATOR")
            right = self.term()
            node = ASTNode("BinaryExpression", value=op, children=[node, right])
        return node

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token["type"] == "OPERATOR" and self.current_token["value"] in ["*", "/"]:
            op = self.current_token["value"]
            self.eat("OPERATOR")
            right = self.factor()
            node = ASTNode("BinaryExpression", value=op, children=[node, right])
        return node

    def factor(self):
        token = self.current_token
        if token["type"] == "NUMBER":
            self.eat("NUMBER")
            return ASTNode("NumberLiteral", value=token["value"])
        elif token["type"] == "STRING":
            self.eat("STRING")
            return ASTNode("StringLiteral", value=token["value"])
        elif token["type"] == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return ASTNode("Identifier", value=token["value"])
        elif token["type"] == "DELIMITER" and token["value"] == "(":
            self.eat("DELIMITER", "(")
            node = self.expression()
            self.eat("DELIMITER", ")")
            return node
        else:
            raise Exception(f"Fator inesperado: {token}")


if __name__ == "__main__":
    from lexer import Lexer

    code = """
func main() {
    var x = 10;
    if (x > 5) {
        print("Hello");
    }
    for (var i = 0; i < 10; i = i + 1) {
        print(i);
    }
    while (x > 0) {
        x = x - 1;
    }
}
func somar(a: int, b: int) -> int {
    return a + b;
}
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    # You can add a simple AST pretty printer here to visualize the tree
    def print_ast(node, indent=0):
        if node is None: # Handle None nodes
            return
        print("  " * indent + f"- {node.type}", end="")
        if node.value is not None:
            print(f" ({node.value})", end="")
        if hasattr(node, "metadata") and node.metadata:
            print(f" {node.metadata}", end="")
        print()
        for child in node.children:
            print_ast(child, indent + 1)

    print("\nPretty Printed AST:")
    print_ast(ast)
