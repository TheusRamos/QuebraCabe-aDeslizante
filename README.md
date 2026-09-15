# Quebra-Cabeça Deslizante — BFS e DFS

Aplicação de terminal em Python 3.10 ou superior, sem dependências externas.
O objetivo é `1 2 3 / 4 5 6 / 7 8 0`. As ações movimentam o espaço vazio.

## Execução

```console
python index.py
```

Digite três linhas com três números cada, usando todos os números de 0 a 8:

```text
1 2 3
4 0 6
7 5 8
```

Executar os casos do enunciado ou alterar o limite do DFS:

```console
python index.py --casos
python index.py --limite 10
python -m unittest -v
```

## Modelagem e métricas

Cada nó armazena o tabuleiro como tupla, o nó pai, a ação e a profundidade
(custo, pois todo movimento custa 1). O caminho é reconstruído pelos pais.
A BFS usa uma fila FIFO e marca estados ao inseri-los. A DFS usa uma pilha
LIFO e limite padrão de 20. Ambas exploram as ações na ordem CIMA, BAIXO,
ESQUERDA, DIREITA, quando válidas.

Na DFS, o controle de visitados registra a menor profundidade encontrada.
Um estado pode ser reaberto se um caminho mais curto deixar mais movimentos
disponíveis até o limite. Usar apenas um conjunto global de visitados poderia
descartar uma solução válida dentro do limite.

- **Nós expandidos:** nós cujos sucessores são gerados; exclui o objetivo,
  nós cortados pelo limite e entradas obsoletas da pilha. Reexpansões da DFS
  contam novamente; esta métrica não é o número de estados distintos.
- **Pico da fronteira:** máximo de nós simultaneamente na fila ou pilha,
  incluindo a raiz. Não representa toda a memória do processo: o mapa de
  visitados e os nós retidos pelas referências aos pais também ocupam memória.
- **Tempo:** medido com `perf_counter`, incluindo a busca e a criação dos nós,
  excluindo entrada, impressão e reconstrução da lista de ações.
- **Falha:** informa corte pelo limite ou esgotamento da busca; passos e ações
  aparecem como N/A. Atingir o limite não prova que o tabuleiro é insolúvel.

## Relatório técnico

Resultados de uma execução local com limite 20; tempos variam entre execuções.

| Caso | Algoritmo | Passos | Nós expandidos | Pico da fronteira | Tempo (ms) |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | BFS | 1 | 2 | 3 | 0,571 |
| 1 | DFS | 1 | 20100 | 19 | 774,634 |
| 2 | BFS | 3 | 16 | 14 | 0,419 |
| 2 | DFS | 13 | 4382 | 19 | 93,794 |
| 3 | BFS | 4 | 28 | 18 | 0,383 |
| 3 | DFS | 20 | 14028 | 18 | 280,101 |

As matrizes fornecidas nos casos 2 e 3 exigem no mínimo **3 e 4 movimentos**,
respectivamente, apesar das faixas de dificuldade indicadas no enunciado.
Os caminhos mínimos são `[DIREITA, BAIXO, DIREITA]` e
`[DIREITA, BAIXO, DIREITA, BAIXO]`.

### 1. Garantia de otimalidade

O DFS encontrou a mesma quantidade de passos somente no caso 1. A BFS
explora os estados por profundidade crescente e garante o menor número de
movimentos, já que todos têm o mesmo custo. O DFS segue primeiro um ramo
conforme a ordem das ações e aceita a primeira solução encontrada: não há
garantia de otimalidade. Mesmo no caso 1, ele explora muitos nós antes de
retornar ao ramo que contém a solução de um passo.

### 2. Consumo de memória

Nos casos testados, o pico da fila da BFS aumentou de 3 para 14 e 18 nós
com distâncias de 1, 3 e 4 movimentos. Ela precisa guardar os próximos níveis
de busca; o crescimento pode ser exponencial na profundidade, em termos
do fator de ramificação. Os casos são pequenos e não demonstram, sozinhos,
o comportamento em profundidades grandes. O pico não cresce obrigatoriamente
de forma estrita entre quaisquer dois tabuleiros. A pilha da DFS foi pequena,
mas seu mapa de visitados também deve ser considerado no consumo total.

### 3. DFS sem limite de profundidade

Sem controle de ciclos, o DFS pode repetir movimentos indefinidamente.
Com visitados, o grafo finito do 8-Puzzle eventualmente se esgota, mas a busca
pode percorrer caminhos muito longos, gastar bastante tempo e memória e
encontrar soluções extensas. Uma implementação recursiva também pode exceder
o limite da pilha de chamadas. Esta aplicação usa pilha explícita, controle de
estados e limite de profundidade; o limite restringe a exploração, mas pode
impedir a descoberta de soluções que exijam mais movimentos.
