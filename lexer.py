import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0

        self.token_specs = [
            ("SKIP",        r"\s+|//.*|/\*.*?\*/"),  # Espaços em branco e comentários
            ("KEYWORD",     r"\b(func|if|else|for|while|var|int|float|bool|string|true|false|return|print)\b"),  # Palavras-chave
            ("IDENTIFIER",  r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Identificadores
            ("NUMBER",      r"\d+(\.\d*)?"),  # Números (inteiros ou decimais)
            ("STRING",      r"\"(?:[^\\\"]|\\.)*\"|\'(?:[^\\\"]|\\.)*\'"),  # Atualizado para lidar com aspas escapadas e aspas simples
            ("OPERATOR",    r"\+\+|--|==|!=|<=|>=|&&|\|\||->|[+\-*/%<>]"),  # Incluído operador ->
            ("ASSIGN",      r"="),  # Atribuição
            ("DELIMITER",   r"[(){},;:]"),  # Delimitadores
        ]

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for token_type, regex in self.token_specs:
                pattern = re.compile(regex)
                m = pattern.match(self.code, self.position)
                if m:
                    value = m.group(0)
                    if token_type != "SKIP":
                        self.tokens.append({"type": token_type, "value": value})
                    self.position = m.end(0)
                    match = True
                    break
            if not match:
                raise Exception(f"Caractere inesperado: {self.code[self.position]}")
        return self.tokens

if __name__ == "__main__":
    code = """
func main() {
    var x = 10;
    if (x > 5) {
        print("Hello");
    }
}
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)



