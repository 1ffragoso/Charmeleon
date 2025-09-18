class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def add_symbol(self, name, type, kind=None):
        if name in self.symbols:
            raise Exception(f"Erro semântico: Símbolo '{name}' já declarado neste escopo.")
        self.symbols[name] = {"type": type, "kind": kind}

    def get_symbol(self, name):
        symbol = self.symbols.get(name)
        if symbol is None and self.parent:
            return self.parent.get_symbol(name)
        return symbol

class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = None

    def enter_scope(self):
        new_scope = SymbolTable()
        new_scope.parent = self.current_scope
        self.current_scope = new_scope

    def exit_scope(self):
        self.current_scope = self.current_scope.parent

    def analyze(self, ast):
        self.enter_scope() # Global scope
        self.visit(ast)
        self.exit_scope()

    def visit(self, node):
        method_name = f"visit_{node.type}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            if child:
                self.visit(child)

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_FunctionDeclaration(self, node):
        func_name = node.value
        return_type = node.metadata.get("return_type")
        # Add function to current scope (global)
        self.current_scope.add_symbol(func_name, "function", kind={"return_type": return_type})

        self.enter_scope() # Function scope
        # Add parameters to function scope
        for param in node.children[0].children:
            self.current_scope.add_symbol(param.value, param.metadata["type"], kind="parameter")
        
        self.visit(node.children[1]) # Visit function body (Block)
        self.exit_scope()

    def visit_VariableDeclaration(self, node):
        var_name = node.value
        var_type = node.metadata.get("type")
        # Infer type if not explicitly declared
        if var_type is None:
            expr_type = self.visit(node.children[0]) # Get type of expression
            var_type = expr_type
        
        self.current_scope.add_symbol(var_name, var_type, kind="variable")
        # Type checking for assignment
        expr_type = self.visit(node.children[0])
        if var_type and expr_type and var_type != expr_type:
            raise Exception(f"Erro semântico: Atribuição de tipo incompatível para '{var_name}'. Esperado {var_type}, mas obteve {expr_type}.")

    def visit_AssignmentStatement(self, node):
        var_name = node.value
        symbol = self.current_scope.get_symbol(var_name)
        if not symbol:
            raise Exception(f"Erro semântico: Variável '{var_name}' não declarada.")
        
        expr_type = self.visit(node.children[0])
        if symbol["type"] and expr_type and symbol["type"] != expr_type:
            raise Exception(f"Erro semântico: Atribuição de tipo incompatível para '{var_name}'. Esperado {symbol['type']}, mas obteve {expr_type}.")

    def visit_IfStatement(self, node):
        condition_type = self.visit(node.children[0])
        if condition_type != "bool":
            raise Exception(f"Erro semântico: Condição 'if' deve ser do tipo booleano, mas obteve {condition_type}.")
        self.enter_scope()
        self.visit(node.children[1]) # True block
        self.exit_scope()
        if node.children[2]: # Else block or else if
            self.enter_scope()
            self.visit(node.children[2])
            self.exit_scope()

    def visit_ForStatement(self, node):
        self.enter_scope()
        if node.children[0]: # init
            self.visit(node.children[0])
        condition_type = self.visit(node.children[1])
        if condition_type != "bool":
            raise Exception(f"Erro semântico: Condição 'for' deve ser do tipo booleano, mas obteve {condition_type}.")
        if node.children[2]: # update
            self.visit(node.children[2])
        self.visit(node.children[3]) # body
        self.exit_scope()

    def visit_WhileStatement(self, node):
        condition_type = self.visit(node.children[0])
        if condition_type != "bool":
            raise Exception(f"Erro semântico: Condição 'while' deve ser do tipo booleano, mas obteve {condition_type}.")
        self.enter_scope()
        self.visit(node.children[1]) # body
        self.exit_scope()

    def visit_ReturnStatement(self, node):
        # For simplicity, assume return type matches function declaration for now
        # In a real compiler, you'd check against the current function's declared return type
        return self.visit(node.children[0])

    def visit_PrintStatement(self, node):
        # Print can take any type, so just visit the expression
        self.visit(node.children[0])

    def visit_BinaryExpression(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        op = node.value

        if op in ["+", "-", "*", "/"]:
            if left_type == "int" and right_type == "int":
                return "int"
            elif left_type == "float" and right_type == "float":
                return "float"
            elif (left_type == "int" and right_type == "float") or (left_type == "float" and right_type == "int"):
                return "float" # Promote to float
            elif op == "+" and left_type == "string" and right_type == "string":
                return "string"
            else:
                raise Exception(f"Erro semântico: Operação aritmética inválida entre {left_type} e {right_type}.")
        elif op in ["==", "!=", "<", ">", "<=", ">="]:
            if left_type == right_type:
                return "bool"
            else:
                raise Exception(f"Erro semântico: Comparação inválida entre {left_type} e {right_type}.")
        elif op in ["&&", "||"]:
            if left_type == "bool" and right_type == "bool":
                return "bool"
            else:
                raise Exception(f"Erro semântico: Operação lógica inválida entre {left_type} e {right_type}. Esperado booleanos.")
        return None # Should not reach here

    def visit_NumberLiteral(self, node):
        if "." in node.value:
            return "float"
        return "int"

    def visit_StringLiteral(self, node):
        return "string"

    def visit_Identifier(self, node):
        symbol = self.current_scope.get_symbol(node.value)
        if not symbol:
            raise Exception(f"Erro semântico: Variável '{node.value}' não declarada.")
        return symbol["type"]


if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser

    code = """
func main() {
    var x = 10;
    var y: float = 20.5;
    var z = x + y;
    if (z > 30.0) {
        print("Maior que 30");
    }
}

func calculate(a: int, b: int) -> int {
    return a * b;
}
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(ast)
        print("Análise semântica concluída com sucesso!")
    except Exception as e:
        print(f"Erro durante a análise semântica: {e}")

    # Teste com erro de tipo
    code_error = """
func test_error() {
    var a = 10;
    var b: bool = a;
}
"""
    lexer_error = Lexer(code_error)
    tokens_error = lexer_error.tokenize()
    parser_error = Parser(tokens_error)
    ast_error = parser_error.parse()
    analyzer_error = SemanticAnalyzer()
    try:
        analyzer_error.analyze(ast_error)
        print("Análise semântica de erro concluída com sucesso (mas deveria falhar)!")
    except Exception as e:
        print(f"Erro esperado durante a análise semântica: {e}")

    # Teste com variável não declarada
    code_undeclared = """
func test_undeclared() {
    var a = 10;
    b = 20;
}
"""
    lexer_undeclared = Lexer(code_undeclared)
    tokens_undeclared = lexer_undeclared.tokenize()
    parser_undeclared = Parser(tokens_undeclared)
    ast_undeclared = parser_undeclared.parse()
    analyzer_undeclared = SemanticAnalyzer()
    try:
        analyzer_undeclared.analyze(ast_undeclared)
        print("Análise semântica de variável não declarada concluída com sucesso (mas deveria falhar)!")
    except Exception as e:
        print(f"Erro esperado durante a análise semântica: {e}")


