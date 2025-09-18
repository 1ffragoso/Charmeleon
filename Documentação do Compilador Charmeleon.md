# Documentação do Compilador Charmeleon

## 1. Introdução

Este documento detalha o design, a implementação e as funcionalidades do compilador para a linguagem de programação Charmeleon. Desenvolvido com foco em simplicidade, intuitividade e velocidade, o Charmeleon é uma linguagem projetada para desenvolvimento web, combinando características de Python e C#. O compilador aqui descrito é uma ferramenta essencial que transforma o código-fonte escrito em Charmeleon em código Python executável, incorporando otimizações e análises de segurança estática (SAST) para garantir a eficiência e a robustez das aplicações geradas.

O processo de compilação do Charmeleon segue uma arquitetura modular, dividida em várias fases distintas: Análise Léxica, Análise Sintática (com construção da Árvore de Sintaxe Abstrata - AST), Análise Semântica, Geração de Código Intermediário (IR), Otimização de Código (com foco em Eliminação de Código Morto - DCE), Análise de Segurança Estática (SAST) e Geração de Código Alvo (transpilação para Python). Cada uma dessas fases contribui para a transformação progressiva do código-fonte, desde sua representação textual até um programa funcional em Python.

O objetivo principal deste compilador é fornecer uma base sólida para o desenvolvimento de aplicações web, aproveitando a sintaxe amigável do Charmeleon e a vasta ecossistema do Python. Além disso, a inclusão de funcionalidades de SAST visa identificar e mitigar potenciais vulnerabilidades de segurança desde as etapas iniciais do desenvolvimento, promovendo a criação de software mais seguro. A otimização de código, por sua vez, garante que o código gerado seja performático, removendo instruções desnecessárias e otimizando o fluxo de execução.

Este documento servirá como um guia abrangente para desenvolvedores, pesquisadores e entusiastas que desejam entender o funcionamento interno do compilador Charmeleon, suas capacidades e como ele pode ser utilizado para construir aplicações web eficientes e seguras.

**Autor:** Manus AI
**Data:** 21 de agosto de 2025





## 2. Análise e Detalhamento dos Requisitos do Projeto

A fase inicial do desenvolvimento do compilador Charmeleon envolveu uma análise aprofundada dos requisitos do projeto, definindo o escopo, as funcionalidades essenciais e as características desejadas para a linguagem e seu compilador. Esta etapa foi crucial para estabelecer uma base sólida para as fases subsequentes de design e implementação.

### 2.1. Definição da Linguagem Charmeleon

O primeiro e mais fundamental requisito foi a concepção da própria linguagem Charmeleon. Foi decidido que a linguagem deveria ser:

*   **Simples e Intuitiva:** Inspirada na facilidade de uso do Python, com uma sintaxe clara e de fácil aprendizado.
*   **Rápida:** Embora o compilador gere código Python, a intenção é que a linguagem Charmeleon em si permita a escrita de código que, após a transpilação e otimização, seja performático.
*   **Focada em Desenvolvimento Web:** Embora não implementado diretamente no compilador base, o design da linguagem deveria prever futuras extensões para facilitar a criação de aplicações web, como manipulação de requisições HTTP, integração com bancos de dados e renderização de templates.
*   **Delimitadores de Bloco:** Optou-se pelo uso de chaves `{}` para delimitar blocos de código, similar ao C#, proporcionando uma estrutura visual clara e consistente.
*   **Sem Recursos Avançados Iniciais:** Para manter a simplicidade e focar no núcleo do compilador, decidiu-se não incluir inicialmente recursos como classes (Programação Orientada a Objetos), módulos ou tratamento de exceções (`try-catch`). Esta decisão simplificou significativamente o design do analisador semântico e do gerador de código.

### 2.2. Funcionalidades do Compilador

Com base na definição da linguagem, os seguintes requisitos funcionais foram estabelecidos para o compilador:

*   **Análise Léxica:** Capacidade de ler o código-fonte Charmeleon e convertê-lo em uma sequência de tokens, identificando palavras-chave, identificadores, literais, operadores e delimitadores.
*   **Análise Sintática:** Construção de uma Árvore de Sintaxe Abstrata (AST) a partir da sequência de tokens, verificando a conformidade com a gramática da linguagem. A AST serve como uma representação estruturada do programa, facilitando as fases posteriores.
*   **Análise Semântica:** Verificação da correção semântica do programa, incluindo a checagem de tipos, a declaração e o escopo de variáveis, e a consistência no uso de identificadores. Esta fase também constrói e utiliza uma tabela de símbolos para gerenciar informações sobre as entidades do programa.
*   **Geração de Código Intermediário (IR):** Transformação da AST em uma representação de código intermediário, que é mais próxima do código de máquina, mas ainda independente da plataforma alvo. O IR facilita a aplicação de otimizações e a geração de código para diferentes alvos.
*   **Otimização de Código:** Implementação de técnicas de otimização para melhorar a eficiência do código gerado. O requisito inicial focou na **Eliminação de Código Morto (Dead Code Elimination - DCE)**, que remove instruções que não afetam o resultado final do programa, reduzindo o tamanho e o tempo de execução.
*   **Análise de Segurança Estática (SAST):** Inclusão de um componente de análise estática para identificar potenciais vulnerabilidades de segurança no código Charmeleon. O foco inicial foi na detecção de:
    *   **Exposição de Dados Sensíveis:** Identificação de `print` diretos de identificadores que podem conter informações sensíveis.
    *   **Injeção por Concatenação de Strings:** Detecção de padrões de concatenação de strings que podem levar a vulnerabilidades de injeção (e.g., SQL Injection, Command Injection) se não forem devidamente sanitizadas.
*   **Geração de Código Alvo:** Transpilação do código intermediário (otimizado) para código Python executável. Esta fase é responsável por mapear as construções da linguagem Charmeleon para as equivalentes em Python, permitindo que os programas Charmeleon sejam executados no ambiente Python.
*   **Testes Abrangentes:** Desenvolvimento de um conjunto de testes de ponta a ponta para validar a correção de cada fase do compilador e a funcionalidade geral da transpilação. Isso inclui testes para estruturas de controle (condicionais, loops), declarações de variáveis, atribuições e a detecção de vulnerabilidades pelo SAST.

### 2.3. Ferramentas e Tecnologias

Para a implementação do compilador, foi definida a utilização da linguagem Python, aproveitando sua flexibilidade e o rico ecossistema de bibliotecas para desenvolvimento de ferramentas de processamento de texto e análise de dados. A escolha do Python como linguagem de implementação e como alvo de transpilação simplifica o processo de desenvolvimento e depuração.

Esta fase de detalhamento dos requisitos serviu como um mapa para todo o projeto, garantindo que todas as partes interessadas tivessem uma compreensão clara dos objetivos e das funcionalidades a serem entregues. A iteração contínua com o solicitante foi fundamental para refinar esses requisitos e tomar decisões cruciais, como a escolha dos delimitadores de bloco e a exclusão inicial de recursos avançados.



## 3. Idealização e Design da Linguagem de Programação

A concepção da linguagem Charmeleon foi um passo fundamental no desenvolvimento deste compilador. A idealização buscou criar uma linguagem que fosse ao mesmo tempo poderosa para o desenvolvimento web e acessível para programadores, combinando as melhores práticas de linguagens estabelecidas como Python e C#. O nome "Charmeleon" foi escolhido para refletir essa dualidade: a simplicidade e adaptabilidade (como um camaleão) e a capacidade de ser "charmosa" em sua sintaxe e uso, além de evocar a ideia de transformação (de código Charmeleon para Python).

### 3.1. Filosofia e Propósito

A filosofia central do Charmeleon é a de oferecer uma experiência de codificação que priorize a clareza e a produtividade. Embora o foco seja o desenvolvimento web, a linguagem foi projetada com uma base genérica que permite sua expansão para outras áreas no futuro. A rapidez, tanto na escrita do código quanto na execução do programa compilado, é um pilar dessa filosofia. A intenção é que os desenvolvedores possam expressar suas ideias de forma concisa, e que o compilador se encarregue de gerar um código eficiente.

### 3.2. Sintaxe e Estrutura

As decisões sintáticas foram tomadas com base na familiaridade e na legibilidade:

*   **Delimitadores de Bloco: Chaves `{}`.** Diferentemente do Python, que utiliza indentação para definir blocos de código, o Charmeleon adota as chaves `{}` para essa finalidade, similar ao C#, Java e JavaScript. Essa escolha proporciona uma delimitação visual explícita dos blocos de código, o que pode ser preferível para desenvolvedores acostumados com linguagens da família C. Exemplos incluem blocos de funções, condicionais (`if-else`) e laços de repetição (`for`, `while`).

    ```charmeleon
    func minhaFuncao() {
        var x = 10;
        if (x > 5) {
            print("X é maior que 5");
        } else {
            print("X é menor ou igual a 5");
        }
    }
    ```

*   **Declaração de Variáveis: `var` e Tipagem Opcional.** A declaração de variáveis utiliza a palavra-chave `var`, seguida pelo nome da variável. A tipagem é opcional, permitindo inferência de tipo, mas também pode ser explicitamente declarada após dois pontos (`:`), similar ao TypeScript ou Kotlin. Isso oferece flexibilidade ao desenvolvedor, permitindo um estilo mais dinâmico ou mais estático conforme a necessidade.

    ```charmeleon
    var idade = 30;             // Inferência de tipo (int)
    var nome: string = "Alice"; // Tipagem explícita
    var preco: float = 99.99;
    ```

*   **Funções: `func` e Retorno Explícito.** Funções são declaradas com a palavra-chave `func`, seguida pelo nome, lista de parâmetros entre parênteses e, opcionalmente, o tipo de retorno após `->`. O corpo da função é delimitado por chaves.

    ```charmeleon
    func somar(a: int, b: int) -> int {
        return a + b;
    }

    func saudacao() {
        print("Olá, Charmeleon!");
    }
    ```

*   **Estruturas de Controle:**
    *   **Condicionais (`if-else`):** Seguem a sintaxe tradicional com a condição entre parênteses e blocos de código entre chaves.
    *   **Laços de Repetição (`for`, `while`):** O laço `for` é similar ao C-style `for` (`for (inicialização; condição; atualização)`), enquanto o `while` segue a sintaxe padrão.

    ```charmeleon
    for (var i = 0; i < 10; i = i + 1) {
        print(i);
    }

    var contador = 5;
    while (contador > 0) {
        print(contador);
        contador = contador - 1;
    }
    ```

*   **Operadores:** Suporte a operadores aritméticos (`+`, `-`, `*`, `/`, `%`), relacionais (`==`, `!=`, `<`, `>`, `<=`, `>=`) e lógicos (`&&`, `||`).

*   **Comentários:** Suporte a comentários de linha única (`//`) e de múltiplas linhas (`/* ... */`).

### 3.3. Recursos Atualmente Excluídos (para Simplicidade Inicial)

Para manter o escopo do projeto gerenciável e focar na construção de um compilador funcional, algumas funcionalidades comuns em linguagens modernas foram intencionalmente excluídas nesta fase inicial de design:

*   **Programação Orientada a Objetos (Classes, Herança, Polimorfismo):** Não há suporte nativo para classes ou conceitos de POO. A linguagem é procedural por natureza nesta versão.
*   **Módulos e Importação:** Não há um sistema formal de módulos ou pacotes para organizar e reutilizar código entre arquivos. O compilador assume um único arquivo de entrada.
*   **Tratamento de Exceções (`try-catch`):** Mecanismos para tratamento de erros e exceções não foram implementados.
*   **Tipos de Dados Complexos:** A linguagem suporta tipos básicos como `int`, `float`, `bool` e `string`. Não há tipos de dados mais complexos como arrays, listas, dicionários ou estruturas definidas pelo usuário.

Essas exclusões simplificaram significativamente a complexidade do analisador léxico, sintático e semântico, permitindo que o foco fosse na construção de um pipeline de compilação robusto para as funcionalidades essenciais. Futuras versões da linguagem e do compilador podem incorporar esses recursos para aumentar sua expressividade e poder.



## 4. Análise Léxica

A primeira fase do processo de compilação do Charmeleon é a Análise Léxica, realizada pelo componente `Lexer`. O objetivo principal desta fase é ler o código-fonte da linguagem Charmeleon, caractere por caractere, e agrupá-los em unidades significativas chamadas **tokens**. Cada token representa uma construção atômica da linguagem, como palavras-chave, identificadores, operadores, literais (números e strings) e delimitadores.

### 4.1. Funcionamento do Lexer

O `Lexer` opera através de um conjunto de regras de expressões regulares (`token_specs`) que definem os padrões para cada tipo de token. Ele percorre o código-fonte, tentando encontrar a maior correspondência possível para um dos padrões definidos. Uma vez que um padrão é reconhecido, o lexer extrai o lexema (a sequência de caracteres que forma o token) e o classifica com um tipo de token correspondente. Espaços em branco e comentários são ignorados nesta fase, pois não contribuem para a estrutura sintática ou semântica do programa.

**Componente:** `lexer.py`

### 4.2. Especificação dos Tokens

A tabela a seguir detalha os tipos de tokens reconhecidos pelo lexer do Charmeleon, juntamente com suas descrições e exemplos:

| Tipo de Token | Descrição                                                                 | Expressão Regular (Regex)                                  | Exemplos                                                                 |
|---------------|---------------------------------------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------------------|
| `SKIP`        | Espaços em branco e comentários (ignorados)                               | `\s+|//.*|/\*.*?\*/`                                       | ` ` (espaço), `\t` (tab), `\n` (nova linha), `// comentário`, `/* multi-linha */` |
| `KEYWORD`     | Palavras reservadas da linguagem                                          | `\b(func|if|else|for|while|var|int|float|bool|string|true|false|return|print)\b` | `func`, `if`, `else`, `var`, `print`, `return`                           |
| `IDENTIFIER`  | Nomes de variáveis, funções, etc.                                         | `[a-zA-Z_][a-zA-Z0-9_]*`                                   | `x`, `main`, `myVariable`, `_counter`                                    |
| `NUMBER`      | Literais numéricos (inteiros ou ponto flutuante)                          | `\d+(\.\d*)?`                                             | `10`, `3.14`, `0`, `123.45`                                              |
| `STRING`      | Literais de string (entre aspas duplas ou simples, com escape)            | `\"(?:[^\\\"]|\\.)*\"|\'(?:[^\\\"]|\\.)*\'`         | `"Hello World"`, `'single quote'`, `"com \"aspas\""`                 |
| `ASSIGN`      | Operador de atribuição                                                    | `=`                                                        | `=`                                                                      |
| `OPERATOR`    | Operadores aritméticos, relacionais, lógicos e de tipo                   | `\+\+|--|==|!=|<=|>=|&&|\|\||->|[+\-*/%<>]`             | `+`, `-`, `*`, `/`, `==`, `!=`, `>`, `<`, `->`                           |
| `DELIMITER`   | Delimitadores de sintaxe                                                  | `[(){},;:]`                                                | `(`, `)`, `{`, `}`, `,`, `;`, `:`                                        |

### 4.3. Estrutura de Saída

O `Lexer` produz uma lista de dicionários, onde cada dicionário representa um token e contém as chaves `"type"` (o tipo de token, como `"KEYWORD"`, `"IDENTIFIER"`, etc.) e `"value"` (o lexema real, ou seja, a string correspondente ao token no código-fonte). Por exemplo, a linha de código `var x = 10;` seria tokenizada como:

```json
[
  {"type": "KEYWORD", "value": "var"},
  {"type": "IDENTIFIER", "value": "x"},
  {"type": "ASSIGN", "value": "="},
  {"type": "NUMBER", "value": "10"},
  {"type": "DELIMITER", "value": ";"}
]
```

Esta sequência de tokens é então passada para a próxima fase do compilador: a Análise Sintática. A robustez do lexer é crucial, pois quaisquer erros ou falhas na tokenização podem propagar-se e causar problemas nas fases subsequentes do processo de compilação. O lexer do Charmeleon foi projetado para ser resiliente a variações de espaços e comentários, e para corretamente identificar literais de string complexos, incluindo aqueles com aspas escapadas ou mistas.



## 5. Análise Sintática e Árvore de Sintaxe Abstrata (AST)

Após a Análise Léxica, a sequência de tokens gerada é passada para o **Analisador Sintático** (ou **Parser**). O objetivo desta fase é verificar se a sequência de tokens segue as regras gramaticais da linguagem Charmeleon e, em caso afirmativo, construir uma representação hierárquica do código-fonte chamada **Árvore de Sintaxe Abstrata (AST)**. A AST é uma estrutura de dados em árvore que representa a estrutura sintática do programa, omitindo detalhes irrelevantes como delimitadores e espaços em branco, e focando nas relações entre as construções do código.

### 5.1. Funcionamento do Parser

O parser do Charmeleon é um analisador sintático descendente recursivo. Ele percorre a lista de tokens e tenta aplicar as regras de produção da gramática da linguagem. Cada regra de produção corresponde a uma função no parser que tenta reconhecer uma construção específica da linguagem (como uma declaração de função, uma expressão, um laço de repetição, etc.). Se a sequência de tokens corresponde à regra, um nó da AST é criado para representar essa construção, e o parser continua a analisar os tokens restantes. Se a sequência não corresponde a nenhuma regra válida, um erro de sintaxe é lançado.

**Componente:** `parser.py`

### 5.2. Estrutura da AST

A AST é composta por nós (`ASTNode`), onde cada nó representa uma parte do código. Cada `ASTNode` possui:

*   **`type`:** O tipo do nó, que descreve a construção da linguagem que ele representa (e.g., `"FunctionDeclaration"`, `"IfStatement"`, `"BinaryExpression"`).
*   **`value`:** Um valor associado ao nó, como o nome de uma variável, o valor de um literal numérico, ou o operador em uma expressão binária.
*   **`children`:** Uma lista de nós filhos, que representam as sub-construções do nó atual. Por exemplo, um nó `"IfStatement"` teria como filhos a condição, o bloco `true` e, opcionalmente, o bloco `false`.
*   **`metadata`:** Um dicionário para armazenar informações adicionais que serão úteis em fases posteriores, como o tipo de uma variável ou o tipo de retorno de uma função.

**Exemplo de AST:**

Para o seguinte código Charmeleon:

```charmeleon
func main() {
    var x = 10;
    if (x > 5) {
        print("maior");
    }
}
```

O parser geraria uma AST com a seguinte estrutura (simplificada):

```
- Program
  - FunctionDeclaration (main)
    - ParameterList
    - Block
      - VariableDeclaration (x)
        - NumberLiteral (10)
      - IfStatement
        - BinaryExpression (>)
          - Identifier (x)
          - NumberLiteral (5)
        - Block
          - PrintStatement
            - StringLiteral ("maior")
        - None (bloco else)
```

### 5.3. Gramática da Linguagem (Simplificada)

A seguir, uma visão geral da gramática que o parser implementa:

*   `program ::= (function_declaration)*`
*   `function_declaration ::= 'func' IDENTIFIER '(' parameter_list ')' ('->' type)? '{' block '}'`
*   `block ::= (statement)*`
*   `statement ::= variable_declaration | assignment_statement | if_statement | for_statement | while_statement | return_statement | print_statement`
*   `variable_declaration ::= 'var' IDENTIFIER (':' type)? '=' expression ';'`
*   `assignment_statement ::= IDENTIFIER '=' expression ';'`
*   `if_statement ::= 'if' '(' expression ')' '{' block '}' ('else' ('{' block '}' | if_statement))?`
*   `for_statement ::= 'for' '(' (variable_declaration_no_semicolon | assignment_statement_no_semicolon)? ';' expression? ';' (assignment_statement_no_semicolon)? ')' '{' block '}'`
*   `while_statement ::= 'while' '(' expression ')' '{' block '}'`
*   `expression ::= comparison`
*   `comparison ::= arithmetic (('==' | '!=' | '<' | '>' | '<=' | '>=') arithmetic)*`
*   `arithmetic ::= term (('+' | '-') term)*`
*   `term ::= factor (('*' | '/') factor)*`
*   `factor ::= NUMBER | STRING | IDENTIFIER | '(' expression ')'`

A AST gerada nesta fase é a entrada para a Análise Semântica, que verificará a correção lógica do programa e enriquecerá a AST com informações de tipo e informações de tipo e tipo.



## 6. Análise Semântica

A Análise Semântica complementa a análise sintática verificando propriedades que não podem ser checadas apenas pela gramática. Nesta fase, o compilador Charmeleon constrói e consulta uma ou mais tabelas de símbolos para validar declarações, usos e tipos básicos das entidades do programa. O escopo é gerenciado de forma hierárquica: a declaração de uma função cria um novo escopo; laços como `for` e `while` também introduzem escopos locais no gerador de IR para fins de resolução de identificadores durante a geração de código intermediário. Isso garante que variáveis declaradas dentro de um bloco não “vazem” para escopos externos, refletindo práticas comuns de linguagens com blocos delimitados por chaves.

A verificação semântica atual contempla:

- Presença de declarações de variáveis antes do uso, por escopo.
- Registro de tipo básico das variáveis (`int`, `float`, `bool`, `string`) quando disponível; quando não há anotação, o tipo é marcado como desconhecido a nível do analisador, mas ainda assim o identificador é válido para uso. O pipeline atual não impõe coerção de tipos em tempo de compilação, mantendo o comportamento semelhante a linguagens de tipagem dinâmica durante a geração de Python.
- Validação estrutural de funções: nome, parâmetros (com tipos opcionais) e corpo.

Esse desenho minimiza falsos positivos e facilita futuras extensões, como inferência de tipos, verificação de conversões e checagens de fluxo de dados.


## 7. Geração de Código Intermediário (IR)

A representação intermediária (IR) é um conjunto linear de instruções de três endereços que descrevem o programa de forma mais próxima a uma máquina abstrata, porém independente de plataforma. O IR do Charmeleon utiliza instruções simples, fáceis de analisar e transformar, permitindo otimizações e posterior geração de código alvo com relativa facilidade. O formato adotado inclui rótulos e saltos explícitos, que viabilizam a representação de estruturas de controle como condicionais e laços.

Conjunto de instruções IR atualmente suportado:

- `FUNC <nome>:` e `END_FUNC <nome>`: Delimitam o início e o fim da função. Cada função é gerada como um bloco contíguo de IR.
- `LABEL:`: Rótulos nomeados (`L1:`, `L2:` …) para alvos de salto.
- `ASSIGN <alvo>, <expr>`: Atribuição simples. O lado direito é normalmente um temporário, literal ou identificador.
- `BIN_OP <t>, <esq>, <op>, <dir>`: Operação binária que coloca o resultado no temporário `<t>`. Exemplos: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`.
- `IF_FALSE <cond> GOTO <label>`: Salto condicional caso a condição avalie como falsa.
- `GOTO <label>`: Salto incondicional.
- `PRINT <expr>`: Emissão de saída padrão, mantida até o código alvo.
- `RETURN <expr>`: Retorno da função.

Padrões estruturais:

- If/Else: Traduzido como `IF_FALSE cond GOTO L_else; …; GOTO L_end; L_else: …; L_end:`.
- While: Representado como `L_start: IF_FALSE cond GOTO L_end; corpo; GOTO L_start; L_end:`.
- For (estilo C): Expandido em init; `L_start:`; `IF_FALSE cond GOTO L_end;` corpo; update; `GOTO L_start; L_end:`.

Essa forma facilita tanto a otimização (por exemplo, eliminação de código morto) quanto a reestruturação para Python na etapa final.



## 8. Otimização de Código: Eliminação de Código Morto (DCE)

A fase de otimização de código é crucial para melhorar a eficiência e o desempenho do programa gerado. No compilador Charmeleon, a otimização implementada é a **Eliminação de Código Morto (Dead Code Elimination - DCE)**. O código morto refere-se a instruções que produzem resultados que nunca são usados posteriormente no programa, ou a blocos de código que nunca podem ser alcançados durante a execução. A remoção dessas instruções ou blocos resulta em um código final menor e mais rápido, sem alterar a funcionalidade do programa.

### 8.1. Funcionamento do Otimizador

O otimizador (`optimizer.py`) opera sobre o Código Intermediário (IR) gerado. A abordagem utilizada para DCE é baseada na análise de *liveness* (vivacidade) de variáveis. Uma variável é considerada "viva" em um determinado ponto do programa se seu valor pode ser usado em algum ponto futuro da execução. Se uma variável não está viva após uma atribuição, essa atribuição pode ser considerada código morto e removida.

O processo de DCE no compilador Charmeleon envolve as seguintes etapas:

1.  **Análise de Definições e Usos (Def-Use Chains):** Para cada instrução no IR, o otimizador identifica quais variáveis são *definidas* (recebem um novo valor) e quais são *usadas* (seu valor é lido). Isso cria cadeias de dependência entre as instruções.
2.  **Análise de Liveness Reversa:** O otimizador percorre o código IR de trás para frente, mantendo um conjunto de variáveis "vivas" em cada ponto. Quando uma instrução é processada:
    *   As variáveis *usadas* por essa instrução são adicionadas ao conjunto de variáveis vivas.
    *   As variáveis *definidas* por essa instrução são removidas do conjunto de variáveis vivas (pois a definição anterior dessa variável não é mais relevante).
3.  **Marcação de Código Morto:** Se uma instrução de atribuição (`ASSIGN` ou `BIN_OP` seguida de `ASSIGN`) define uma variável que não está viva imediatamente após essa definição, essa instrução é marcada como código morto. No entanto, o otimizador é conservador e não remove atribuições a variáveis que não são temporárias (ou seja, variáveis declaradas pelo usuário), a menos que a análise de liveness comprove que a atribuição é realmente inútil e não afeta o fluxo de controle ou saída do programa. Isso é importante para preservar o comportamento esperado de programas que podem ter efeitos colaterais não explícitos na análise de liveness simples ou que dependem de variáveis para depuração.
4.  **Reconstrução do IR:** Após a marcação, o otimizador constrói uma nova lista de instruções IR, excluindo as instruções marcadas como código morto.

**Componente:** `optimizer.py`

### 8.2. Exemplo de Eliminação de Código Morto

Considere o seguinte código Charmeleon:

```charmeleon
func main() {
    var x = 10;
    var y = 20; // Variável 'y' é definida, mas nunca usada
    print(x);
}
```

O IR gerado inicialmente pode ser algo como:

```
FUNC main:
ASSIGN x, 10
ASSIGN y, 20
PRINT x
END_FUNC main
```

Após a aplicação da Eliminação de Código Morto, a instrução `ASSIGN y, 20` seria identificada como código morto, pois o valor atribuído a `y` nunca é lido ou utilizado posteriormente. O IR otimizado seria:

```
FUNC main:
ASSIGN x, 10
PRINT x
END_FUNC main
```

Esta otimização contribui diretamente para a geração de código Python mais limpo e eficiente, reduzindo o tamanho do programa e, consequentemente, seu tempo de execução. A abordagem conservadora garante que a otimização não introduza efeitos colaterais indesejados ou altere a semântica do programa original.



## 9. Análise de Segurança Estática (SAST)

A segurança é um aspecto crítico no desenvolvimento de software. No compilador Charmeleon, a fase de Análise de Segurança Estática (SAST) foi integrada para identificar potenciais vulnerabilidades de segurança diretamente no código-fonte da linguagem Charmeleon, antes mesmo da execução. Esta abordagem permite que os desenvolvedores corrijam falhas de segurança precocemente no ciclo de desenvolvimento, reduzindo custos e riscos associados a vulnerabilidades em produção.

### 9.1. Funcionamento do SAST Analyzer

O `SASTAnalyzer` opera sobre a Árvore de Sintaxe Abstrata (AST) gerada pelo parser. Ao invés de executar o código, ele analisa a estrutura e o fluxo do programa para detectar padrões que são comumente associados a vulnerabilidades de segurança. A análise é baseada em regras predefinidas que buscam construções específicas na AST.

**Componente:** `sast_analyzer.py`

### 9.2. Vulnerabilidades Detectadas

Nesta versão inicial, o SAST do compilador Charmeleon foca em duas categorias principais de vulnerabilidades:

#### 9.2.1. Exposição de Dados Sensíveis

**Descrição:** Esta regra detecta o uso direto da função `print` com identificadores que podem conter dados sensíveis. Embora `print` seja uma função legítima para depuração, a impressão de variáveis como `username`, `password`, `token`, `secret`, etc., diretamente para a saída padrão pode expor informações confidenciais em ambientes de produção ou logs, tornando-as acessíveis a atacantes ou usuários não autorizados.

**Padrão de Detecção:** O analisador busca por nós `PrintStatement` na AST cujos filhos sejam `Identifier` e cujo nome do identificador corresponda a uma lista predefinida de palavras-chave sensíveis (e.g., `"username"`, `"password"`, `"token"`, `"secret"`).

**Exemplo de Código Vulnerável (Charmeleon):**

```charmeleon
func main() {
    var username = "admin";
    var password = "my_secret_password";
    print(username); // Potencial exposição de dados sensíveis
    print(password); // Potencial exposição de dados sensíveis
}
```

#### 9.2.2. Injeção por Concatenação de Strings

**Descrição:** Esta regra visa identificar padrões de construção de strings que podem levar a vulnerabilidades de injeção (como SQL Injection, Command Injection, ou Cross-Site Scripting - XSS) se a string resultante for usada em um contexto inseguro (e.g., uma consulta de banco de dados, um comando de sistema operacional, ou conteúdo HTML). A concatenação de literais de string com variáveis de entrada do usuário sem sanitização adequada é um vetor comum para esses ataques.

**Padrão de Detecção:** O analisador procura por `BinaryExpression` (operações de concatenação `+`) onde um dos operandos é um `StringLiteral` (parte fixa da consulta/comando) e o outro é um `Identifier` (representando uma entrada do usuário ou variável que pode conter dados controlados por um atacante). A regra é acionada quando uma string é construída dinamicamente a partir de uma parte literal e uma variável, especialmente em contextos que sugerem uma consulta ou comando.

**Exemplo de Código Vulnerável (Charmeleon):**

```charmeleon
func main() {
    var user_input = "admin
    var query = "SELECT * FROM users WHERE name = '" + user_input + "'"; // Potencial injeção de SQL
    print(query);
}
```

### 9.3. Relatório de Vulnerabilidades

Quando uma vulnerabilidade é detectada, o `SASTAnalyzer` gera um relatório que inclui:

*   **Tipo:** A categoria da vulnerabilidade (e.g., `"PotentialSensitiveDataExposure"`, `"PotentialInjection"`).
*   **Mensagem:** Uma descrição concisa da vulnerabilidade e sua causa.
*   **Nó AST:** Uma referência ao nó específico na AST onde a vulnerabilidade foi identificada, auxiliando na localização do problema no código-fonte original.

O resultado da análise SAST é impresso no `stderr` do compilador, permitindo que os desenvolvedores visualizem os avisos de segurança sem interferir na saída do código Python gerado. Esta funcionalidade é um passo importante para promover a escrita de código mais seguro na linguagem Charmeleon.



## 10. Geração de Código Alvo (Transpilação para Python)

A fase final do processo de compilação do Charmeleon é a **Geração de Código Alvo**, onde o Código Intermediário (IR) otimizado é transformado em código Python executável. Este processo é conhecido como transpilação, pois o código-fonte de uma linguagem (Charmeleon) é convertido para o código-fonte de outra linguagem (Python), mantendo o mesmo nível de abstração.

### 10.1. Funcionamento do Code Generator

O `CodeGenerator` (`code_generator.py`) recebe a lista de instruções IR (já otimizadas pela fase de DCE) e as traduz para a sintaxe Python correspondente. O desafio principal nesta fase é mapear as construções de baixo nível do IR (como `IF_FALSE` e `GOTO`) para as estruturas de controle de alto nível do Python (como `if/else` e `while` loops), mantendo a semântica original do programa.

O gerador de código percorre as instruções IR e, para cada tipo de instrução, emite a linha de código Python equivalente. Para lidar com as estruturas de controle, o gerador de código emprega uma lógica que tenta identificar padrões de IR que correspondem a `if/else` e `while` loops. Por exemplo, uma sequência de `BIN_OP` (para a condição), `IF_FALSE` (para o salto condicional) e `GOTO` (para o salto incondicional) pode ser reconhecida e convertida em um `if` ou `while` em Python.

**Componente:** `code_generator.py`

### 10.2. Mapeamento de IR para Python

A seguir, alguns exemplos de como as instruções IR são mapeadas para o código Python:

| Instrução IR                               | Código Python Gerado (Exemplo)                                 |
|---------------------------------------------|----------------------------------------------------------------| 
| `FUNC main:`                                | `def main():`                                                  |
| `END_FUNC main`                             | (fecha o bloco da função)                                      |
| `ASSIGN x, 10`                              | `x = 10`                                                       |
| `BIN_OP t1, x, +, 5`                        | `t1 = x + 5`                                                   |
| `PRINT x`                                   | `print(x)`                                                     |
| `RETURN result`                             | `return result`                                                |
| `IF_FALSE t1 GOTO L2`                       | `if not t1:` (ou `if x > 5:` se a condição for dobrada)        |
| `GOTO L1`                                   | (mapeado para `while` ou `else` em estruturas de controle)     |
| `LABEL L1:`                                 | (mapeado para o início de um bloco de código ou loop)          |

**Tratamento de Strings:**

Um ponto importante na geração de código é o tratamento correto de literais de string, especialmente aqueles que contêm aspas. O `CodeGenerator` garante que as aspas dentro de strings sejam escapadas corretamente no código Python gerado, para evitar erros de sintaxe e preservar o conteúdo original da string. Por exemplo, uma string Charmeleon como `"Hello \"World\""` será corretamente transpilada para `"Hello \"World\""` em Python.

**Reconhecimento de Estruturas de Controle:**

O `CodeGenerator` analisa o fluxo de controle implícito nas instruções `IF_FALSE` e `GOTO` para reconstruir as estruturas `if/else` e `while` do Python. Isso envolve:

*   **Condicionais (`if/else`):** Uma instrução `IF_FALSE` seguida por um bloco de código e um `GOTO` para um rótulo de fim, e um rótulo `else` opcional, é traduzida para um `if` com um `else` correspondente.
*   **Laços (`while`):** Um padrão de `LABEL` (início do loop), `BIN_OP` (condição), `IF_FALSE` (saída do loop), um bloco de código (corpo do loop) e um `GOTO` de volta para o `LABEL` inicial é reconhecido e transpilado para um `while` loop em Python.

### 10.3. Desafios e Abordagens

A transpilação de IR de baixo nível para estruturas de alto nível em Python é um desafio complexo. A abordagem adotada tenta ser o mais estrutural possível, mas em alguns casos, especialmente com `GOTO`s arbitrários, pode ser necessário gerar código Python que simule um "program counter" ou use `break`/`continue` de forma mais explícita, embora a preferência seja por `if/else` e `while` diretos. A iteração contínua e os testes de ponta a ponta são essenciais para garantir a correção e a robustez dessa fase.

O resultado final desta fase é um arquivo `.py` que pode ser executado diretamente pelo interpretador Python, efetivamente compilando o programa Charmeleon para um formato amplamente utilizável.



## 11. Desenvolvimento de Testes Abrangentes

Para garantir a correção e a robustez do compilador Charmeleon, uma suíte de testes abrangente foi desenvolvida. Estes testes são de ponta a ponta, o que significa que eles exercitam todo o pipeline do compilador, desde a leitura do código-fonte Charmeleon até a geração do código Python final. O objetivo é verificar se cada fase do compilador funciona conforme o esperado e se o código Python gerado é semanticamente equivalente ao código Charmeleon original.

### 11.1. Estrutura dos Testes

Os testes são implementados usando o módulo `unittest` do Python, o que permite uma estrutura organizada para os casos de teste. Cada caso de teste consiste em:

1.  **Código-fonte Charmeleon:** Uma string contendo um trecho de código na linguagem Charmeleon, projetado para testar uma funcionalidade específica (e.g., uma declaração `if-else`, um laço `for`, uma detecção de vulnerabilidade SAST).
2.  **Execução do Compilador:** O código-fonte Charmeleon é salvo em um arquivo temporário e passado como entrada para o `ir_generator.py` (que atua como o ponto de entrada principal do compilador). A saída padrão (`stdout`) e a saída de erro padrão (`stderr`) do compilador são capturadas.
3.  **Verificação de Saída:** Asserções são usadas para verificar se o código Python gerado (capturado de `stdout`) contém as estruturas esperadas e se as mensagens de SAST (capturadas de `stderr`) são emitidas corretamente quando aplicável.

**Componente:** `test_compiler.py`

### 11.2. Casos de Teste Implementados

A suíte de testes atual inclui os seguintes cenários:

*   **`test_if_else_statement`:** Verifica a correta transpilação de declarações `if-else` para suas equivalentes em Python, incluindo a condição e os blocos `true` e `false`.
*   **`test_for_loop`:** Assegura que os laços `for` (estilo C) sejam corretamente convertidos em estruturas `while` em Python, com inicialização, condição e atualização adequadas.
*   **`test_while_loop`:** Valida a transpilação de laços `while` para suas contrapartes em Python, incluindo a condição e o corpo do laço.
*   **`test_sast_injection_vulnerability`:** Confirma que o `SASTAnalyzer` detecta corretamente a vulnerabilidade de injeção por concatenação de strings. Este teste verifica a presença da mensagem `"PotentialInjection"` na saída de erro padrão do compilador.
*   **`test_dead_code_elimination`:** Verifica se a otimização de Eliminação de Código Morto (DCE) funciona conforme o esperado, garantindo que instruções de código morto (como atribuições a variáveis não utilizadas) sejam removidas do IR otimizado (e, consequentemente, não apareçam no código Python gerado).

### 11.3. Importância dos Testes

Os testes de ponta a ponta são cruciais por várias razões:

*   **Validação Integrada:** Eles verificam a interação correta entre todas as fases do compilador, garantindo que as saídas de uma fase sejam entradas válidas para a próxima.
*   **Detecção de Regressões:** Ao serem executados regularmente, os testes ajudam a identificar rapidamente quaisquer regressões (bugs introduzidos por novas alterações) no compilador.
*   **Garantia de Qualidade:** Fornecem uma garantia de que o compilador está produzindo código Python funcional e seguro, que se comporta como o esperado pelo código Charmeleon original.
*   **Suporte ao Desenvolvimento:** Permitem que os desenvolvedores façam alterações e refatorações com confiança, sabendo que a suíte de testes alertará sobre quaisquer problemas introduzidos.

O sucesso de todos os testes indica um alto nível de confiança na correção e na funcionalidade do compilador Charmeleon, tanto em termos de transpilação quanto de detecção de segurança e otimização.



## 12. Conclusão

O desenvolvimento do compilador Charmeleon representou um esforço significativo na criação de uma ferramenta robusta e multifacetada para a transpilação de código-fonte. Desde a idealização de uma linguagem simples e intuitiva, inspirada em Python e C#, até a implementação de um pipeline de compilação completo, cada fase foi cuidadosamente projetada para garantir a correção, a eficiência e a segurança do código gerado.

As principais conquistas deste projeto incluem:

*   **Design da Linguagem Charmeleon:** Uma linguagem com sintaxe clara, uso de chaves para blocos de código e tipagem opcional, focada em simplicidade e adaptabilidade para desenvolvimento web.
*   **Pipeline de Compilação Completo:** A implementação bem-sucedida de todas as fases essenciais de um compilador: Análise Léxica, Análise Sintática (com AST), Análise Semântica, Geração de Código Intermediário (IR), Otimização de Código (DCE), Análise de Segurança Estática (SAST) e Geração de Código Alvo (transpilação para Python).
*   **Otimização Eficaz:** A inclusão da Eliminação de Código Morto (DCE) que contribui para a geração de código Python mais limpo e performático, removendo instruções desnecessárias.
*   **Análise de Segurança Estática (SAST):** A capacidade de identificar proativamente vulnerabilidades comuns, como exposição de dados sensíveis e injeção por concatenação de strings, promovendo a escrita de código mais seguro desde as etapas iniciais.
*   **Transpilação para Python:** A habilidade de converter o código Charmeleon em código Python executável, aproveitando a vasta ecossistema e a portabilidade do Python.
*   **Testes Abrangentes:** A suíte de testes de ponta a ponta, que valida a funcionalidade de cada componente e a integração do compilador como um todo, garantindo a qualidade e a confiabilidade do sistema.

Embora o compilador Charmeleon já seja uma ferramenta funcional e eficaz, há diversas oportunidades para futuras melhorias e expansões. Estas podem incluir a adição de recursos mais avançados à linguagem (como classes, módulos, tratamento de exceções), a implementação de otimizações adicionais, a expansão das regras de SAST para cobrir um espectro mais amplo de vulnerabilidades, e a possibilidade de gerar código para outras plataformas ou linguagens (e.g., JavaScript para execução direta no navegador).

Em suma, o compilador Charmeleon demonstra a viabilidade de criar linguagens de programação customizadas com foco em domínios específicos, ao mesmo tempo em que incorpora práticas de segurança e otimização. Este projeto serve como uma base sólida para futuras inovações no campo de linguagens e compiladores, e esperamos que ele seja uma ferramenta valiosa para a comunidade de desenvolvimento.

