

# Função será detectada pelo pytest se começar com "test_" e estiver em um arquivo "test_*.py".
# O assert verifica se a condição é verdadeira; se não for, levanta AssertionError e o teste falha.
# Qualquer exceção não tratada faz o teste falhar, mas usamos assert por padrão.
def test_failing():
    assert (2, 1) == (1, 2)
