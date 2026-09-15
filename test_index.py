import unittest

from index import CASOS, OBJETIVO, bfs, dfs, sucessores, validar_estado


class TestPuzzle(unittest.TestCase):
    def conferir_caminho(self, estado, resultado):
        self.assertIsNotNone(resultado.no)
        for acao in resultado.acoes:
            estado = dict(sucessores(estado))[acao]
        self.assertEqual(estado, OBJETIVO)
        self.assertEqual(len(resultado.acoes), resultado.no.profundidade)

    def test_casos_e_caminhos(self):
        for estado, distancia in zip(CASOS, (1, 3, 4)):
            with self.subTest(estado=estado):
                largura = bfs(estado)
                self.assertEqual(largura.no.profundidade, distancia)
                self.conferir_caminho(estado, largura)
                self.conferir_caminho(estado, dfs(estado))
                self.assertIsNone(dfs(estado, distancia - 1).no)
                self.conferir_caminho(estado, dfs(estado, distancia))

    def test_objetivo_e_limite_zero(self):
        for resultado in (bfs(OBJETIVO), dfs(OBJETIVO, 0)):
            self.assertEqual(resultado.acoes, [])
            self.assertEqual(resultado.expandidos, 0)
            self.assertEqual(resultado.pico_fronteira, 1)
        self.assertIsNone(dfs(CASOS[0], 0).no)

    def test_sem_solucao(self):
        resultado = bfs((1, 2, 3, 4, 5, 6, 8, 7, 0))
        self.assertIsNone(resultado.no)
        self.assertIn('esgotado', resultado.status)
        self.assertEqual(resultado.expandidos, 181440)

    def test_entradas_invalidas(self):
        for estado in ((0,) * 9, tuple(range(8)), tuple(range(1, 10))):
            with self.assertRaises(ValueError):
                validar_estado(estado)
        with self.assertRaises(ValueError):
            dfs(OBJETIVO, -1)


if __name__ == '__main__':
    unittest.main()
