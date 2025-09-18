# Manual do Usuário: Compilador Charmeleon

## 1. Introdução

Bem-vindo ao manual do usuário do Compilador Charmeleon! Este documento foi criado para ajudá-lo a utilizar o compilador Charmeleon para transformar seu código-fonte Charmeleon em código Python executável. O Charmeleon é uma linguagem de programação simples, intuitiva e rápida, focada em desenvolvimento web, que combina a facilidade do Python com a estrutura do C#.

Este compilador não apenas transpila seu código, mas também realiza otimizações para melhorar a eficiência e executa uma Análise de Segurança Estática (SAST) para identificar potenciais vulnerabilidades em seu código.

## 2. Pré-requisitos

Para utilizar o compilador Charmeleon, você precisará ter o seguinte instalado em seu sistema:

*   **Python 3.11 ou superior:** O compilador Charmeleon é desenvolvido em Python e gera código Python. Certifique-se de ter a versão correta instalada.

## 3. Estrutura do Projeto

O projeto do compilador Charmeleon é organizado nos seguintes arquivos:

*   `main.py`: O script principal que orquestra o processo de compilação.
*   `lexer.py`: Implementa o analisador léxico, responsável por tokenizar o código-fonte.
*   `parser.py`: Implementa o analisador sintático, que constrói a Árvore de Sintaxe Abstrata (AST).
*   `semantic_analyzer.py`: Realiza a análise semântica e a checagem de tipos.
*   `ir_generator.py`: Gera o Código Intermediário (IR) a partir da AST.
*   `optimizer.py`: Implementa a otimização de Eliminação de Código Morto (DCE) no IR.
*   `sast_analyzer.py`: Realiza a Análise de Segurança Estática (SAST).
*   `code_generator.py`: Transpila o IR otimizado para código Python.
*   `test_compiler.py`: Contém a suíte de testes de ponta a ponta para o compilador.
*   `documentation.md`: Documentação detalhada sobre o design e a implementação do compilador.
*   `project_proposal.md`: Proposta inicial do projeto.
*   `user_manual.md`: Este manual.

Todos esses arquivos devem estar no mesmo diretório para que o compilador funcione corretamente.

## 4. Como Usar o Compilador Charmeleon

Para compilar um arquivo `.charmeleon`, siga os passos abaixo:

1.  **Navegue até o Diretório do Compilador:** Abra seu terminal ou prompt de comando e navegue até o diretório onde você salvou os arquivos do compilador Charmeleon.

    ```bash
    cd /caminho/para/seu/diretorio/charmeleon_compiler
    ```

2.  **Crie seu Código Charmeleon:** Escreva seu código na linguagem Charmeleon e salve-o em um arquivo com a extensão `.charmeleon` (por exemplo, `meu_programa.charmeleon`).

    **Exemplo de `meu_programa.charmeleon`:**
    ```charmeleon
    func main() {
        var x = 10;
        if (x > 5) {
            print("X é maior que 5");
        } else {
            print("X é menor ou igual a 5");
        }
        var user_input = "admin";
        var query = "SELECT * FROM users WHERE name = \'" + user_input + "\'";
        print(query);
    }
    ```

3.  **Execute o Compilador:** Utilize o script `main.py` para compilar seu arquivo Charmeleon. Passe o caminho para o seu arquivo `.charmeleon` como argumento.

    ```bash
    python3.11 main.py meu_programa.charmeleon
    ```

## 5. Saída do Compilador

Ao executar o compilador, você verá duas seções principais na saída:

### 5.1. Resultados da Análise SAST (Saída de Erro Padrão - `stderr`)

Esta seção exibirá o relatório da Análise de Segurança Estática. Se nenhuma vulnerabilidade for encontrada, a mensagem "Nenhuma vulnerabilidade encontrada." será exibida. Caso contrário, ele listará as vulnerabilidades detectadas, incluindo o tipo, uma mensagem descritiva e o nó da AST onde a vulnerabilidade foi identificada.

**Exemplo de Saída SAST:**

```
==============================
Resultados da Análise SAST
==============================

- Tipo: PotentialInjection
  Mensagem: Potencial vulnerabilidade de injeção detectada em concatenação de string.
  Nó AST: ASTNode(type='BinaryExpression' value='+' children=[ASTNode(type='BinaryExpression' value='+' children=[ASTNode(type='StringLiteral' value='"SELECT * FROM users WHERE name = \'"'), ASTNode(type='Identifier' value='user_input')], metadata={}), ASTNode(type='StringLiteral' value='\''"')] metadata={})
```

### 5.2. Código Python Gerado (Saída Padrão - `stdout`)

Esta seção exibirá o código Python transpilado a partir do seu código Charmeleon. Este é o código que você pode executar diretamente com um interpretador Python.

**Exemplo de Código Python Gerado (para o `meu_programa.charmeleon` acima):**

```python
def main():
    x = 10
    if x > 5:
        print("X é maior que 5")
    else:
        print("X é menor ou igual a 5")
    user_input = "admin"
    query = "SELECT * FROM users WHERE name = \'" + user_input + "\''"
    print(query)

```

Além de imprimir na tela, o compilador também salvará o código Python gerado em um novo arquivo com a mesma base de nome do seu arquivo Charmeleon, mas com a extensão `.py` (por exemplo, `meu_programa.py`).

## 6. Executando o Código Python Gerado

Após a compilação, você pode executar o arquivo `.py` gerado diretamente com o interpretador Python:

```bash
python3.11 meu_programa.py
```

## 7. Testando o Compilador

Para verificar a funcionalidade do compilador e garantir que todas as fases estão operando corretamente, você pode executar a suíte de testes de ponta a ponta. Certifique-se de estar no diretório `charmeleon_compiler` e execute:

```bash
python3.11 -m unittest test_compiler.py
```

Se todos os testes passarem, você verá uma mensagem "OK". Caso contrário, as falhas serão detalhadas.

## 8. Suporte e Contato

Se você tiver dúvidas, encontrar problemas ou precisar de assistência, por favor, consulte a documentação detalhada (`documentation.md`) ou entre em contato com o desenvolvedor. Estamos aqui para ajudar a tornar sua experiência com o Charmeleon a melhor possível!

--- 

**Autor:** Manus AI
**Data:** 28 de agosto de 2025


