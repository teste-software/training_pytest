import pytest

'''
Fixtures -> funções auxiliares que podem ser executadas antes de cada teste
para preparar o ambiente de teste, como criar objetos, configurar conexões, 
colocar o ambiente em um estado específico, etc. Elas são úteis para evitar
repetição de código e manter os testes limpos e organizados.
Assim, como depois do teste para limpar o ambiente, fechar conexões, etc.
'''


# Recurso simples, apenas um fixture para retornar um dado
# pytest.fixture é um decorador que marca uma função como fixture
# O nome da função fixture pode ser usado como argumento em testes
# O pytest executa a fixture antes do teste que a utiliza
# e passa o valor retornado como argumento para o teste.
@pytest.fixture
def some_date():
    return 42

# As funções de fixture geralmente configuram ou recuperam alguns dados 
# com os quais o teste pode trabalhar;
def test_some_date(some_date):
    assert some_date == 42
    
# pytest trata as exceções levantadas dentro de uma fixture como "Error"
# diferenmente de um teste que falha, que é tratado como "Failed"
# Se uma fixture falhar, o teste que a utiliza também falhará, poŕem 
# será analisado como "Error" ajudando da depuração
@pytest.fixture
def some_date_error():
    raise ValueError("This is an error in the fixture")

def test_some_date_error(some_date_error):
    assert some_date_error is False  # Este teste falhará com "Error" porque a fixture falhou
    

'''
Vamos trabalhar com montagem e desmontagem, primeiro adicionar dados no cards:

$ cards count
$ cards add first item
$ cards add second item
$ cards count
'''

from pathlib import Path
from tempfile import TemporaryDirectory
from cards import CardsDB, Card

def test_empty():
    # aqui criamos um diretório temporário que será removido após o teste,
    # mas podemos usar o fixture para fazer essa configuração
    # pois o objetivo é testar o CardsDB com um banco de dados vazio
    # não a inicialização do banco de dados em si
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir) 
        db = CardsDB(db_path)
        
        count = db.count()
        assert count == 0
        
        db.close() # fechamos a conexão com o banco de dados
        # porém se o teste falhar, o diretório temporário  não será removido
        
# Agora vamos criar uma fixture que cria um banco de dados temporário
# E resolver o problemas citados anteriores
@pytest.fixture
def cards_db():
    # 'with' garante que o diretório temporário seja removido após o uso, pois está 
    # usando o contexto
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = CardsDB(db_path)
        '''
        Funções de fixação são executadas antes dos testes que as utilizam. 
        Se houver um yield na função, ela para ali, passa o controle para 
        os testes e continua na linha seguinte após a conclusão dos testes. 
        O código acima do yield é "setup" e o código depois do yield é "teardown". 
        O código depois do yield , o teardown, tem a garantia de ser executado
        independentemente do que aconteça durante os testes.
        '''
        yield db
        db.close()  # Isso será executado após o teste, garantindo que o banco de dados seja fechado
        # e o diretório temporário seja removido, mesmo que tenha erro
        
def test_empty_with_fixture(cards_db):
    count = cards_db.count()
    assert count == 0
    
def test_count_two(cards_db):
    cards_db.add_card(Card('first'))
    cards_db.add_card(Card('second'))
    
    count = cards_db.count()
    assert count == 2
    
'''
Os testes individuais, como test_empty() e test_two(), podem ser mantidos menores 
e focar no que estamos testando, e não nas partes de configuração e desmontagem.

As funções de fixação e teste são funções distintas. Nomear cuidadosamente suas 
fixações para refletir o trabalho realizado na fixação ou o objeto retornado pela 
fixação, ou ambos, ajudará na legibilidade
'''

'''
Rastreamento de execução de fixação com –setup-show
ch3/test_fixture.py::test_count_two 
        SETUP    F cards_db
        ch3/test_fixture.py::test_count_two (fixtures used: cards_db) PASSED
        TEARDOWN F cards_db
'''

'''
Especificando o escopo do dispositivo
Cada fixture do pytest possui um escopo que define quando a configuração (setup) e
a desmontagem (teardown) serão executadas em relação aos testes que a utilizam.
O escopo padrão é função, executando antes e depois de cada teste.
Para recursos lentos ou custosos (como conexões de banco ou geração de dados pesados), 
repetir esse processo em todos os testes é ineficiente.
No entanto, pode haver momentos em que você não queira que isso aconteça.
Talvez a configuração e a conexão com o banco de dados sejam demoradas, ou você esteja
gerando grandes conjuntos de dados, ou esteja recuperando dados de um servidor 
ou dispositivo lento. Na verdade, você pode fazer o que quiser dentro de um equipamento,
e algumas dessas ações podem ser lentas.
Alterar o escopo (por exemplo, para módulo) permite que a configuração ocorra uma 
única vez para vários testes, otimizando o tempo total de execução.
'''

'''
scope=’function’
Execute uma vez por função de teste. A parte de configuração é executada antes de cada
teste usando o dispositivo. A parte de desmontagem é executada após cada teste usando
o dispositivo. Este é o escopo padrão usado quando nenhum parâmetro de escopo é especificado.

scope=’class’
Execute uma vez por classe de teste, independentemente de quantos métodos de teste há
na classe.

scope=’module’
Execute uma vez por módulo, independentemente de quantas funções de teste, métodos 
ou outros acessórios no módulo o utilizem.

scope=’package’
Execute uma vez por pacote ou diretório de teste, independentemente de quantas funções
de teste, métodos ou outros acessórios no pacote o utilizam.

scope=’session’
Execute uma vez por sessão. Todos os métodos e funções de teste que usam um ambiente de
escopo de sessão compartilham uma chamada de configuração e desmontagem.

Com um fixture definido dentro de um módulo de teste, os escopos de sessão e pacote
agem exatamente como o escopo do módulo. Para usar esses outros escopos, precisamos 
colocá-los em um arquivo conftest.py .
'''
