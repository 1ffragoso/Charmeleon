import sys
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from optimizer import Optimizer
from code_generator import CodeGenerator
from sast_analyzer import SASTAnalyzer
from ir_generator import IRGenerator # Import IRGenerator

def compile_charmeleon(source_code: str):
    # 1. Análise Léxica
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # 2. Análise Sintática e AST
    parser = Parser(tokens)
    ast = parser.parse()

    # 3. Análise Semântica
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # 4. Análise de Segurança Estática (SAST)
    sast_analyzer = SASTAnalyzer()
    vulnerabilities = sast_analyzer.analyze(ast)

    sast_output = "Resultados da Análise SAST:\n"
    if vulnerabilities:
        for vul in vulnerabilities:
            sast_output += f"- Tipo: {vul['type']}\n  Mensagem: {vul['message']}\n  Nó AST: {str(vul['node'])}\n"
    else:
        sast_output += "Nenhuma vulnerabilidade encontrada.\n"

    # 5. Geração de Código Intermediário (IR)
    ir_generator = IRGenerator()
    ir_code = ir_generator.generate(ast)

    # 6. Otimização de Código (DCE)
    optimizer = Optimizer(ir_code)
    optimized_ir_code = optimizer.eliminate_dead_code()

    # 7. Geração de Código Alvo (Python)
    code_generator = CodeGenerator(optimized_ir_code)
    python_code = code_generator.gen()

    return sast_output, python_code

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

    sast_report, generated_python_code = compile_charmeleon(charmeleon_code)

    # Print SAST report to stderr
    print("\n" + "="*30 + "\nResultados da Análise SAST\n" + "="*30, file=sys.stderr)
    print("\n" + sast_report, file=sys.stderr)

    # Print generated Python code to stdout
    print(generated_python_code)

    # Opcional: Salvar o código Python gerado em um arquivo
    output_file = input_file.replace(".charmeleon", ".py")
    if not output_file.endswith(".py"):
        output_file += ".py"

    # Se houver instruções globais, encapsula em uma função main automaticamente
    if not generated_python_code.strip().startswith("def "):
        wrapped_code = "def __global_main__():\n"
        for line in generated_python_code.splitlines():
            wrapped_code += "    " + line + "\n"
        wrapped_code += "\nif __name__ == '__main__':\n    __global_main__()\n"
        generated_python_code = wrapped_code

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(generated_python_code)
    print(f"\nCódigo Python salvo em: {output_file}", file=sys.stderr)
