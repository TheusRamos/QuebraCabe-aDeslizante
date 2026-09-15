"""8-Puzzle: BFS e DFS limitada, sem heurísticas."""
import argparse
from collections import deque
from dataclasses import dataclass
from time import perf_counter

OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)
CASOS = ((1, 2, 3, 4, 5, 0, 7, 8, 6),
         (1, 2, 3, 0, 4, 6, 7, 5, 8),
         (0, 1, 3, 4, 2, 5, 7, 8, 6))

@dataclass(slots=True)
class No:
    estado: tuple[int, ...]
    pai: 'No | None' = None
    acao: str | None = None
    profundidade: int = 0

@dataclass(slots=True)
class Resultado:
    status: str
    no: No | None
    expandidos: int
    pico_fronteira: int
    tempo_ms: float

    @property
    def acoes(self):
        caminho, atual = [], self.no
        while atual is not None and atual.pai is not None:
            caminho.append(atual.acao)
            atual = atual.pai
        return list(reversed(caminho))

def validar_estado(estado):
    estado = tuple(estado)
    if len(estado) != 9 or any(type(n) is not int for n in estado) or set(estado) != set(range(9)):
        raise ValueError('O tabuleiro deve conter os números de 0 a 8, sem repetição.')
    return estado

def sucessores(estado):
    """Ações do vazio em ordem fixa: CIMA, BAIXO, ESQUERDA, DIREITA."""
    vazio = estado.index(0)
    linha, coluna = divmod(vazio, 3)
    for acao, dl, dc in (('CIMA', -1, 0), ('BAIXO', 1, 0),
                         ('ESQUERDA', 0, -1), ('DIREITA', 0, 1)):
        nl, nc = linha + dl, coluna + dc
        if 0 <= nl < 3 and 0 <= nc < 3:
            destino = nl * 3 + nc
            novo = list(estado)
            novo[vazio], novo[destino] = novo[destino], novo[vazio]
            yield acao, tuple(novo)

def buscar(estado, algoritmo, limite=20):
    if algoritmo not in ('BFS', 'DFS'):
        raise ValueError('Algoritmo deve ser BFS ou DFS.')
    if type(limite) is not int or limite < 0:
        raise ValueError('O limite deve ser um inteiro não negativo.')
    estado = validar_estado(estado)
    inicio = perf_counter()
    fronteira = deque([No(estado)])
    # DFS reabre estados alcançados por caminhos mais curtos, preservando
    # a possibilidade de encontrar soluções dentro do limite restante.
    melhor_profundidade = {estado: 0}
    expandidos, pico = 0, 1
    houve_corte = False

    def resultado(status, no=None):
        return Resultado(status, no, expandidos, pico,
                         (perf_counter() - inicio) * 1000)

    while fronteira:
        no = fronteira.popleft() if algoritmo == 'BFS' else fronteira.pop()
        if no.profundidade != melhor_profundidade[no.estado]:
            continue
        if no.estado == OBJETIVO:
            return resultado('Objetivo alcançado', no)
        if algoritmo == 'DFS' and no.profundidade == limite:
            houve_corte = True
            continue
        expandidos += 1
        vizinhos = list(sucessores(no.estado))
        if algoritmo == 'DFS':
            vizinhos.reverse()  # CIMA deve sair primeiro da pilha.
        for acao, novo in vizinhos:
            profundidade = no.profundidade + 1
            anterior = melhor_profundidade.get(novo)
            if anterior is not None and (algoritmo == 'BFS' or anterior <= profundidade):
                continue
            melhor_profundidade[novo] = profundidade
            fronteira.append(No(novo, no, acao, profundidade))
        pico = max(pico, len(fronteira))
    if houve_corte:
        return resultado(f'Limite de profundidade ({limite}) atingido sem solução')
    return resultado('Espaço de busca esgotado sem solução')

def bfs(estado):
    return buscar(estado, 'BFS')

def dfs(estado, limite=20):
    return buscar(estado, 'DFS', limite)

def comparar(estado, limite):
    print('Estado inicial:')
    for i in range(0, 9, 3):
        print(*estado[i:i + 3])
    for algoritmo in ('BFS', 'DFS'):
        r = buscar(estado, algoritmo, limite)
        print(f'\n{algoritmo}: {r.status}')
        passos = r.no.profundidade if r.no is not None else 'N/A'
        acoes = r.acoes if r.no is not None else 'N/A'
        print(f'Número de passos: {passos}')
        print(f'Sequência de ações: {acoes}')
        print(f'Nós expandidos: {r.expandidos}')
        print(f'Pico de nós na fronteira: {r.pico_fronteira}')
        print(f'Tempo: {r.tempo_ms:.3f} ms')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limite', type=int, default=20, help='Profundidade máxima do DFS (padrão: 20)')
    parser.add_argument('--casos', action='store_true', help='Executar os três casos do enunciado')
    args = parser.parse_args()
    if args.limite < 0:
        parser.error('O limite deve ser não negativo.')
    if args.casos:
        for numero, estado in enumerate(CASOS, 1):
            print(f'\n=== Caso {numero} ===')
            comparar(estado, args.limite)
        return
    print('Digite a matriz, uma linha por vez (use 0 para o espaço vazio):')
    try:
        linhas = [list(map(int, input().split())) for _ in range(3)]
        if any(len(linha) != 3 for linha in linhas):
            raise ValueError('Cada linha deve conter exatamente três números.')
        estado = validar_estado(n for linha in linhas for n in linha)
    except (ValueError, EOFError) as erro:
        parser.error(f'Entrada inválida: {erro}')
    comparar(estado, args.limite)

if __name__ == '__main__':
    main()
