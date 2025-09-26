import sys
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from optimizer import Optimizer
from code_generator import CodeGenerator
from sast_analyzer import SASTAnalyzer
from ir_generator import IRGenerator


def compile_charmeleon(source_code: str):
    outputs = {}

    # 1. Análise Léxica
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    outputs["tokens"] = tokens

    # 2. Análise Sintática e AST
    parser = Parser(tokens)
    ast = parser.parse()
    outputs["ast"] = ast

    # 3. Análise Semântica
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # 4. Análise de Segurança Estática (SAST)
    sast_analyzer = SASTAnalyzer()
    vulnerabilities = sast_analyzer.analyze(ast)
    outputs["sast"] = vulnerabilities

    # 5. Geração de Código Intermediário (IR)
    ir_generator = IRGenerator()
    ir_code = ir_generator.generate(ast)
    outputs["ir_code"] = ir_code

    # 6. Otimização de Código (DCE)
    optimizer = Optimizer(ir_code)
    optimized_ir_code = optimizer.eliminate_dead_code()
    outputs["optimized_ir"] = optimized_ir_code

    # 7. Geração de Código Alvo (Python)
    code_generator = CodeGenerator(optimized_ir_code)
    python_code = code_generator.gen()
    outputs["python_code"] = python_code

    return outputs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3.11 main.py <caminho_do_arquivo_charmeleon>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            charmeleon_code = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    results = compile_charmeleon(charmeleon_code)

    # 1. Tokens
    print("\n" + "="*30 + "\nTOKENS\n" + "="*30)
    print(results["tokens"])

    # 2. AST
    print("\n" + "="*30 + "\nAST (Simplificado)\n" + "="*30)
    def print_ast(node, indent=0):
        if node is None:
            return
        print("  " * indent + f"- {node.type}", end="")
        if node.value is not None:
            print(f" ({node.value})", end="")
        if hasattr(node, "metadata") and node.metadata:
            print(f" {node.metadata}", end="")
        print()
        for child in node.children:
            print_ast(child, indent + 1)
    print_ast(results["ast"])

    # 3. Vulnerabilidades
    print("\n" + "="*30 + "\nSAST (Vulnerabilidades)\n" + "="*30)
    if results["sast"]:
        for vul in results["sast"]:
            print(f"- Tipo: {vul['type']} | Mensagem: {vul['message']} | Nó AST: {vul['node']}")
    else:
        print("Nenhuma vulnerabilidade encontrada.")

    # 4. IR
    print("\n" + "="*30 + "\nCÓDIGO INTERMEDIÁRIO (IR)\n" + "="*30)
    for line in results["ir_code"]:
        print(line)

    # 5. IR Otimizado
    print("\n" + "="*30 + "\nIR OTIMIZADO\n" + "="*30)
    for line in results["optimized_ir"]:
        print(line)

    # 6. Código Python Gerado
    print("\n" + "="*30 + "\nCÓDIGO PYTHON GERADO\n" + "="*30)
    print(results["python_code"])

    # Opcional: Salvar código Python em arquivo
    output_file = input_file.replace(".charmeleon", ".py")
    if not output_file.endswith(".py"):
        output_file += ".py"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(results["python_code"])

    print(f"\nCódigo Python salvo em: {output_file}", file=sys.stderr)
