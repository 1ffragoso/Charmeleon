class SASTAnalyzer:
    def __init__(self):
        self.vulnerabilities = []

    def analyze(self, ast):
        self.vulnerabilities = []
        self.visit(ast)
        return self.vulnerabilities

    def visit(self, node):
        if node is None:
            return
        method_name = f"visit_{node.type}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_PrintStatement(self, node):
        # Simplified example: Check for direct printing of identifiers (potential for sensitive data exposure)
        # In a real SAST, this would be much more complex, involving data flow analysis
        if node.children and node.children[0].type == "Identifier":
            self.vulnerabilities.append({
                "type": "SensitiveDataExposure",
                "message": f"Potencial exposição de dados sensíveis: Variável '{node.children[0].value}' sendo impressa diretamente.",
                "node": node
            })
        self.generic_visit(node)

    def visit_BinaryExpression(self, node):
        # Simplified example: Check for string concatenation that might lead to injection (e.g., SQL injection)
        # This assumes string literals are used directly in concatenation, which is a common pattern for vulnerabilities.
        if node.value == "+":
            left_child = node.children[0]
            right_child = node.children[1]

            if (left_child.type == "StringLiteral" and right_child.type == "Identifier") or \
               (left_child.type == "Identifier" and right_child.type == "StringLiteral"):
                self.vulnerabilities.append({
                    "type": "PotentialInjection",
                    "message": "Potencial vulnerabilidade de injeção: Concatenação de string com identificador. Considere sanitização de entrada.",
                    "node": node
                })
        self.generic_visit(node)


if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser

    code_vulnerable = """
func main() {
    var username = "admin";
    var password = "password123";
    print(username);
    var query = "SELECT * FROM users WHERE username = '" + username + "'";
    print(query);
}
"""

    lexer = Lexer(code_vulnerable)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    sast_analyzer = SASTAnalyzer()
    vulnerabilities = sast_analyzer.analyze(ast)

    print("\nResultados da Análise SAST:")
    if vulnerabilities:
        for vul in vulnerabilities:
            print(f"- Tipo: {vul['type']}\n  Mensagem: {vul['message']}\n  Nó AST: {vul['node']}\n")
    else:
        print("Nenhuma vulnerabilidade encontrada.")

    code_clean = """
func safe_main() {
    var name = "John";
    print("Hello, " + name);
}
"""
    lexer_clean = Lexer(code_clean)
    tokens_clean = lexer_clean.tokenize()
    parser_clean = Parser(tokens_clean)
    ast_clean = parser_clean.parse()

    sast_analyzer_clean = SASTAnalyzer()
    vulnerabilities_clean = sast_analyzer_clean.analyze(ast_clean)

    print("\nResultados da Análise SAST (Código Limpo):")
    if vulnerabilities_clean:
        for vul in vulnerabilities_clean:
            print(f"- Tipo: {vul['type']}\n  Mensagem: {vul['message']}\n  Nó AST: {vul['node']}\n")
    else:
        print("Nenhuma vulnerabilidade encontrada.")


