from bancopg import *
from funcao import *

#cadastrar produto
#escolher um produto e quantidade

#escolher um cliente




while True:
    cria_banco()
    print('DIGITE A OPCAO DESEJADA  ')
    print('1 - Cadastro ')
    print('2 - Pesquisar ')
    print('3 - CadProd manual   ')
    print('4 - Select SQL  ')
    print('5 - Lista Pessoa    ')
    print('6 - Cadastro API   ')
    print('7 - Estoque   ')
    print('8 - Fazer vendas   ')
    print('9 - ApagarProduto   ')
    print('10 - ApagarBanco   ')
    print('11 - Sair   ')
    #print('12 - Cadastrar Administradora API   ')
    #print('13 -    ')
    
    
    consulta = int(input(': '))

    if consulta == 1:
        cadastro()

    if consulta == 2 :
        pesquisa()
        
    if consulta == 3 :
        cadastro_produto()
        
    if consulta == 4:
        select_pessoa()
        
    if consulta == 5 :
        lista_pessoa()

    if consulta == 6 :
        cadastro_pessoa_api()
        cadastro_produto_api() 
        cadastro_administradora()
       

    if consulta == 7 :
        estoque()
        
    if consulta == 8 :
        venda_venda()
        
    if consulta == 9:
        apagar_produto()
    if consulta == 10 :
        apaga_banco()
 
    if consulta == 11 :
        break
        

        