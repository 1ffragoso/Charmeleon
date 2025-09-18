# Charmeleon: Uma Linguagem de Programação para Desenvolvimento Web

## 1. Introdução

Charmeleon é uma linguagem de programação projetada para ser simples, intuitiva e rápida, combinando a facilidade de uso do Python com a performance e robustez do C#. Seu foco principal é o desenvolvimento web, visando oferecer uma experiência de codificação eficiente e agradável para a construção de aplicações web modernas.

## 2. Motivação e Objetivos

A crescente demanda por aplicações web de alta performance e a necessidade de ferramentas que agilizem o processo de desenvolvimento impulsionaram a criação do Charmeleon. Nosso objetivo é preencher a lacuna entre linguagens de script de alto nível, que muitas vezes sacrificam desempenho, e linguagens de baixo nível, que podem ser complexas e demoradas para prototipagem e desenvolvimento rápido. Charmeleon busca oferecer:

*   **Simplicidade e Intuitividade:** Sintaxe clara e concisa, fácil de aprender e usar, mesmo para desenvolvedores iniciantes.
*   **Rapidez e Eficiência:** Compilação para código otimizado, garantindo alta performance em ambientes de produção.
*   **Foco em Web:** Recursos e bibliotecas nativas para facilitar o desenvolvimento de back-ends, APIs e serviços web.
*   **Produtividade:** Ferramentas e um ecossistema que permitam aos desenvolvedores construir e implantar aplicações rapidamente.

## 3. Domínio de Aplicação

Charmeleon é ideal para:

*   Desenvolvimento de APIs RESTful e microsserviços.
*   Construção de back-ends para aplicações web e mobile.
*   Processamento de dados em tempo real para aplicações web.
*   Automação de tarefas relacionadas à web.

## 4. Sintaxe e Semântica (BNF/EBNF - Esboço Inicial)

A sintaxe do Charmeleon será inspirada em Python para legibilidade e em C# para tipagem e estruturas. Utilizaremos uma abordagem de tipagem estática, mas com inferência de tipo para reduzir a verbosidade. Blocos de código serão definidos por chaves `{}`.

### 4.1. Tipos de Dados Básicos

Charmeleon suportará os seguintes tipos de dados primitivos:

*   `int`: Inteiros de 32 bits.
*   `float`: Números de ponto flutuante de 64 bits.
*   `bool`: Valores booleanos (`true`, `false`).
*   `string`: Sequências de caracteres Unicode.

### 4.2. Variáveis

Declaração de variáveis será feita com a palavra-chave `var` (para inferência de tipo) ou com o tipo explícito, seguido do nome da variável e, opcionalmente, uma atribuição inicial.

Exemplos:

```charmeleon
var nome = "Mundo";
int idade = 30;
bool ativo = true;
```

### 4.3. Estruturas de Controle

#### 4.3.1. Condicionais (`if`, `else if`, `else`)

```charmeleon
if (idade > 18) {
    print("Maior de idade");
} else if (idade == 18) {
    print("Exatamente 18");
} else {
    print("Menor de idade");
}
```

#### 4.3.2. Laços (`for`, `while`)

```charmeleon
for (var i = 0; i < 5; i++) {
    print(i);
}

while (ativo) {
    // fazer algo
    ativo = false;
}
```

### 4.4. Funções

Funções serão declaradas com a palavra-chave `func`, seguida do nome da função, parâmetros e tipo de retorno. As chaves `{}` definirão o corpo da função.

```charmeleon
func saudacao(nome: string) -> string {
    return "Olá, " + nome + "!";
}

func somar(a: int, b: int) -> int {
    return a + b;
}
```

## 5. Próximos Passos

Com base neste esboço inicial, refinaremos a sintaxe e semântica, e definiremos formalmente a gramática usando BNF/EBNF. Também discutiremos a escolha da máquina virtual ou formato de saída para a geração de código alvo.

