from bancopg import *
from functools import partial
import hashlib
import urllib.request
import requests
import json
import unidecode
#unidecode retira caracteres
#api_nome= input("Coloque o id da API : ")
api_nome= "chave privada"






def falta_valor(valor_total,valor_pago1):
    if valor_total == valor_pago1 :
        pass
    

    falta = valor_total - valor_pago1
    if falta != 0:
        print( " falta %d reais"%(falta))


def lista_clientes():

        select_cadastro_cliente = Pessoa.select().distinct().order_by(Pessoa.id_pes)

        for i in select_cadastro_cliente:

            print(i.id_pes,'-',i.nome_pes)


        #classe_pesquisa_cliente = int(input("Numero do Cliente : "))
       # print()

       # select_cadastro_cliente =Pessoa.select().where(Pessoa.nome_pes == lista_classe[classe_pesquisa_cliente]).order_by(Pessoa.nome_pes)
        

def lista_classes():
        select_cadastro_produto = Produto.select(Produto.classe_pro).distinct().order_by(Produto.classe_pro)

        ordem=1
        lista_classe ={}

        for i in select_cadastro_produto:

            print(ordem,'-',i.classe_pro)
            lista_classe[ordem]=i.classe_pro
            ordem +=1

        classe_pesquisa_estoque = int(input("Numero da Classe produto : "))
        print()

        select_lista_classe =Produto.select().where(Produto.classe_pro == lista_classe[classe_pesquisa_estoque]).order_by(Produto.nome_pro)

        for ii in select_lista_classe:

            print(
                f"==========================================\n"
                f"Nome do Produto : {ii.nome_pro}  \n"
                f"Id do Produto : {ii.id_pro} \n"
                f"Classe do Produto : {ii.classe_pro} \n"
                f"Quantidade de Estoque : {ii.estoque_pro} \n"
                f"Valor Unitario : R$ {ii.preco_pro}  \n"
                f"==========================================\n"
                )
        print()   

def lista_administradora():
        select_cadastro_adminstradora = Administradora.select(Administradora.tipo_adm).distinct().order_by(Administradora.tipo_adm)

        ordem=1
        lista_classe ={}

        for i in select_cadastro_adminstradora:

            print(ordem,'-',i.tipo_adm)
            lista_classe[ordem]=i.tipo_adm
            ordem +=1

        classe_pesquisa = int(input("Tipo de Pagemento: "))
        print()


        select_lista_adm =Administradora.select().where(Administradora.tipo_adm == lista_classe[classe_pesquisa])#.order_by(Administradora.nome_adm)

        
        ordem1=1
        lista_classe1 ={}
        
        for ii in select_lista_adm:

            print(ordem1,'-',ii.nome_adm)
            lista_classe1[ordem1]=ii.nome_adm
            ordem1 +=1

        print() 


def cadastro():


    cadastro_nova_pessoa=unidecode.unidecode(input('digite seu Nome : ')).upper()

    print('-------Cadastro de endereço-------')

    cadastro_novo_endereco=input('Digite o CEP do Endereço : ')
    with urllib.request.urlopen(f"https://viacep.com.br/ws/{cadastro_novo_endereco}/json/") as url:
        cep_dados = json.loads(url.read().decode())

        print('Estado: ' + cep_dados['uf'].upper())
        print('Bairro: ' + cep_dados['bairro'].upper())
        print('Cidade: ' + cep_dados['localidade'].upper())
        print('Rua: ' + cep_dados['logradouro'].upper())

    numero_endereco=input('Digite o numero da casa : ')
    complemento_endereco=unidecode.unidecode(input('Digite o complemento do endereço : ')).upper()

    telefone = input('Digite seu numero de telefone : ')
    

    data = datetime.now()
    data_data= data.strftime('%d/%m/%Y %H:%M:%S')


    soma = cadastro_nova_pessoa+cep_dados['logradouro'].upper()+numero_endereco+cep_dados['bairro'].upper()+cep_dados['localidade'].upper()+cadastro_novo_endereco+telefone#+data_data
    md5 = hashlib.md5(soma.encode("utf-8")).hexdigest()

    try:   
        Endereco.create(md5_end = md5 ,logradouro_end=cep_dados['logradouro'].upper() ,numero_end=numero_endereco ,complemento_end=complemento_endereco ,bairro_end=cep_dados['bairro'].upper() ,cidade_end=cep_dados['localidade'].upper() ,cep_end=cadastro_novo_endereco,uf_end =cep_dados['uf'].upper())
        
        Pessoa.create(nome_pes =cadastro_nova_pessoa,md5_pes = md5,cadastro_api_pes = 'NAO')
        
        Telefone.create(md5_tel = md5 ,telefone=telefone)  
        
        Data.create(md5_dt=md5,criacao=data_data)   

    except (IntegrityError):#,OperationalError,InternalError):

        print()
        print('Usuario já cadastrado , por favor refaça ou digite Sair para finalizar ')
        print()
        banco.close()
        cadastro()



    id_pessoa1 = Pessoa.select().where(Pessoa.md5_pes == md5 ).get()
    id_endereco = Endereco.select().where(Endereco.md5_end == md5 ).get()
    id_telefone1 = Telefone.select().where(Telefone.md5_tel == md5 ).get()

    id_de_endereco=id_endereco.id_endereco
    id_de_telefone = id_telefone1.id_tel

    update_cria_pessoa=Pessoa.update({Pessoa.id_end:id_de_endereco,Pessoa.id_telefone:id_de_telefone}).where(Pessoa.md5_pes == md5)#.get()
    update_cria_pessoa.execute()
    banco.close()
    input('Aperte ENTER')


def pesquisa():
    while True:
        try:

            pesquisa_dados = unidecode.unidecode(input("Digite o nome a pesquisar ou Sair para finalizar: ")).upper()
            

            print()
            tabela_pessoa = Pessoa.select().where(Pessoa.nome_pes == pesquisa_dados).get()
            tabela_endereco = Endereco.select().where(Endereco.id_endereco == tabela_pessoa.id_pes).get()




            for m in ( Pessoa.select().where(Pessoa.nome_pes == pesquisa_dados)):

                tabela_endereco = Endereco.select().where(Endereco.id_endereco == m.id_pes).get()

                print()
                print(
                    f"==========================================\n"
                    f"Nome da Pessoa : {m.nome_pes} \n"
                    f"Nome Fantasia : {m.nome_fantasia} \n"
                    f"==========================================\n"
                    f"***Endereço da Pessoa *** \n"
                    f"Cep : {tabela_endereco.cep_end} \n"
                    f"Logradouro : {tabela_endereco.logradouro_end} \n"
                    f"Complemento : {tabela_endereco.complemento_end}\n"
                    f"Numero da Casa : {tabela_endereco.numero_end} \n"
                    f"Bairro : {tabela_endereco.bairro_end} \n"
                    f"Cidade : {tabela_endereco.cidade_end} \n"
                    f"Estado : {tabela_endereco.uf_end} \n"  )
                
        except(DoesNotExist):    

            if pesquisa_dados == 'SAIR':
                break
                
            print("-----Pessoa nao cadastrada tente novamente ou digite sair----")
            print()
            banco.close()
            
            pesquisa()
            
    input('Aperte ENTER')



def select_pessoa():

    sql1= banco.execute_sql('select public.pessoa.nome_pes, public.Endereco.logradouro_end, public.Endereco.numero_end, public.Endereco.bairro_end, public.Endereco.cep_end, public.Endereco.cidade_end, public.Endereco.complemento_end from public.Endereco inner join public.pessoa on public.Endereco.id_endereco = public.pessoa.id_end ;')
    for ii in sql1.fetchall():
        print( *ii ,sep =' ')
        print()
    banco.close()
    input('Aperte ENTER')


def cadastro_produto():
    
    cadastro_produto_nome = unidecode.unidecode(input('Digite o nome do produto : ')).upper()
    cadastro_produto_preco=float(input('Digite o preco do produto usar ponto no lugar de virgula '))
    cadastro_produto_estoque = float(input('Digite o estoque do produto usar ponto no lugar de virgula '))
    criar_classe =unidecode.unidecode(str(input("Deseja criar nova classe SIM , ou NAO para usar existente"))).upper()
    
    if criar_classe == 'SIM':
        nome_classe_nova = unidecode.unidecode(input("Digite o nome da classe :")).upper()

        Produto.create(nome_pro =cadastro_produto_nome,preco_pro=cadastro_produto_preco,estoque_pro=cadastro_produto_estoque,classe_pro=nome_classe_nova,cadastro_api_pro = 'NAO')
        corrige_sequence()
        
    
    if criar_classe == 'NAO':
        print('Classes existentes ') 
        
    
        select_cadastro_produto = Produto.select(Produto.classe_pro).distinct().order_by(Produto.classe_pro)

        ordem=1
        lista_classe ={}

        for i in select_cadastro_produto:

            print(ordem,'-',i.classe_pro)
            lista_classe[ordem]=i.classe_pro
            ordem +=1

        print ("Digite o numero da classe do produto ")
        cadastro_produto_classe=int(input(':'))
        print()
        select_cadastro_classe = Produto.select(Produto.classe_pro).distinct().where(Produto.classe_pro ==lista_classe[cadastro_produto_classe])   

        Produto.create(nome_pro =cadastro_produto_nome,preco_pro=cadastro_produto_preco,estoque_pro=cadastro_produto_estoque,classe_pro=select_cadastro_classe,cadastro_api_pro = 'NAO')
        corrige_sequence()

    
    input('Aperte ENTER')
    print()


def cadastro_pessoa_api():#a8797bd0-3af9-437e-997b-d4a813121f46
    cad_pessoa= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_CLIENTE_REDE?CHAVE={api_nome}').json()
    cad_pessoa_empresa= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_CLIENTE_EMPRESA_REDE?CHAVE={api_nome}').json()


    
    try:
        for icad_pessoa_empresa in cad_pessoa_empresa:
        
            if icad_pessoa_empresa['empresaCodigo'] ==3893:
            
                for icad_pessoa in cad_pessoa:
                
                    if icad_pessoa['clienteCodigo'] == icad_pessoa_empresa['clienteCodigo']:
                    
                        inteiro_pessoa =icad_pessoa['clienteCodigo']
                        inteiro_pessoa= str(inteiro_pessoa)
                        
                        soma = icad_pessoa['cidade']+icad_pessoa['uf']+unidecode.unidecode(icad_pessoa['razao'])+unidecode.unidecode(icad_pessoa['fantasia'])+inteiro_pessoa
                        md5 = hashlib.md5(soma.encode("utf-8")).hexdigest()
                                    #nome_classe_nova = unidecode.unidecode(icad_pessoa['razao'])
                        Pessoa.create(nome_pes =unidecode.unidecode(icad_pessoa['razao']),nome_fantasia=unidecode.unidecode(icad_pessoa['fantasia']),md5_pes = md5,cadastro_api_pes='SIM')
                        Endereco.create(md5_end = md5 ,cidade_end=icad_pessoa['cidade'],uf_end =icad_pessoa['uf'])

                        id_pessoa2 = Pessoa.select().where(Pessoa.md5_pes == md5 ).get()
                        id_Endereco = Endereco.select().where(Endereco.md5_end == md5 ).get()
                        
                        id_de_endereco=id_Endereco.id_endereco

                        update_pessoa=Pessoa.update({Pessoa.id_end:id_de_endereco}).where(Pessoa.md5_pes == md5)
                        update_pessoa.execute()
                        
    except (IntegrityError):
        pass

    banco.close()
    


def cadastro_produto_api():

    apaga_pro_api = Produto.delete().where(Produto.cadastro_api_pro == 'SIM')
    apaga_pro_api.execute()
    corrige_sequence()
    banco.close()
   
    cad_produto= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_PRODUTO_REDE?CHAVE={api_nome}').json()
    cad_produto_empresa= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_PRODUTO_EMPRESA_REDE?CHAVE={api_nome}').json()
    cad_classe= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_GRUPO_REDE?CHAVE={api_nome}').json()


    for i1 in cad_produto_empresa:
        if i1["empresaCodigo"] ==3893:
            

                for i in cad_produto:
                    if i["produtoCodigo"] == i1["produtoCodigo"]:
                        for i2 in cad_classe:
                            if i2["grupoCodigo"]==i["grupoCodigo"]:
                                Produto.create(nome_pro =unidecode.unidecode(i["nome"]).upper(), 
                                classe_pro = unidecode.unidecode(i2["nome"]).upper(),
                                preco_pro =(i1["precoVenda"]),
                                estoque_pro =(i1["estoqueQtde"]),
                                cadastro_api_pro = 'SIM'
                                )
    



def apagar_produto():
    apagar = Produto.delete()#.where(Produto.nome_pro == 'DIESEL S500')
    apagar.execute()
    banco.close()
    input('Aperte ENTER')


def corrige_sequence():

    #corrige_sequences_a = Produto.select().count()
    
    corrige_sequences_a = Produto.select(fn.MAX(Produto.id_pro)).scalar()
    #print(corrige_sequences_a)
    
    if corrige_sequences_a != None:
        corrige_sequences_a = corrige_sequences_a +1
        corrige_sequences= banco.execute_sql('ALTER SEQUENCE public.produto_id_pro_seq INCREMENT 1 MINVALUE 1 MAXVALUE 922337 START 1 RESTART %d CACHE 1 NO CYCLE; '%(corrige_sequences_a))
    #corrige_sequences= banco.execute_sql('SELECT setval('produto_id_pro_seq', (SELECT count(produto.id_pro) FROM produto)+1);')


def estoque():
    try:
        lista_classes()
        
        id_produto_estoque =   int(input("Digite o Id do Produto : "))
        quantidade_produto_estoque =   float(input("Nova quantidade de Estoque : "))
        print()
        update_estoque=Produto.update({Produto.estoque_pro:quantidade_produto_estoque}).where(Produto.id_pro == id_produto_estoque)#.get()
        update_estoque.execute()    
        banco.close()
        
        
    except (ValueError,KeyError):
        print("Valor errado")
        estoque()
    banco.close()
    input('Aperte ENTER')
   
   
def lista_pessoa():
    select_lista_pessoa =Pessoa.select().order_by(Pessoa.nome_pes)

    for ii in select_lista_pessoa:

        print(
        f"Nome da Pessoa : {ii.nome_pes}  \n"
        f"Id da Pessoa : {ii.id_pes} \n"
                )
 
    input('Aperte ENTER')
        
        
        
def cadastro_administradora():
    
    cad_administradora= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_FORMA_PAGAMENTO_REDE?chave={api_nome}').json()

    apagar_administradora = Administradora.delete()
    apagar_administradora.execute()
    corrige_sequences_adm = Administradora.select(fn.count(Administradora.id_adm)).scalar()
    
    
    if corrige_sequences_adm != None:
        
        corrige_sequences_adm = corrige_sequences_adm +1
        corrige_sequences= banco.execute_sql('ALTER SEQUENCE public.administradora_id_adm_seq INCREMENT 1 MINVALUE 1 MAXVALUE 922337 START 1 RESTART %d CACHE 1 NO CYCLE; '%(corrige_sequences_adm))

    #Administradora.create(nome_adm ='DINHEIRO',tipo_adm='DINHEIRO',cadastro_api_adm='SIM')
    
    for icad_administradora in cad_administradora:
        
        #if icad_administradora['empresaCodigo'] ==3893:
        Administradora.create(nome_adm =unidecode.unidecode(icad_administradora['nome']),tipo_adm=unidecode.unidecode(icad_administradora['tipo']),cadastro_api_adm='SIM')

    input('Aperte ENTER')


#def cadastro_administradora():
    
#    cad_administradora= requests.get(f'https://web.qualityautomacao.com.br/INTEGRACAO/CONSULTAR_ADMINISTRADORA_REDE?CHAVE={api_nome}').json()

#    apagar_administradora = Administradora.delete()
#    apagar_administradora.execute()
#    corrige_sequences_adm = Administradora.select(fn.count(Administradora.id_adm)).scalar()
    
    
#    if corrige_sequences_adm != None:
        
#        corrige_sequences_adm = corrige_sequences_adm +1
#        corrige_sequences= banco.execute_sql('ALTER SEQUENCE public.administradora_id_adm_seq INCREMENT 1 MINVALUE 1 MAXVALUE 922337 START 1 RESTART %d CACHE 1 NO CYCLE; '%(corrige_sequences_adm))

#    Administradora.create(nome_adm ='DINHEIRO',tipo_adm='DINHEIRO',cadastro_api_adm='SIM')
    
#    for icad_administradora in cad_administradora:
        
#        if icad_administradora['empresaCodigo'] ==3893:
#            Administradora.create(nome_adm =unidecode.unidecode(icad_administradora['descricao']),tipo_adm=unidecode.unidecode(icad_administradora['tipo']),cadastro_api_adm='SIM')

#    input('Aperte ENTER')




def venda_venda1():
        
        lista_classes() 
        
        id_produto_venda =   int(input("Digite o Id do Produto : "))
        
        select_produto_venda =Produto.select(Produto.estoque_pro).where(Produto.id_pro == id_produto_venda).scalar()
        select_produto_venda = float(select_produto_venda)
        
        select_produto_venda_preco =Produto.select(Produto.preco_pro).where(Produto.id_pro == id_produto_venda).scalar()
        select_produto_venda_preco = float(select_produto_venda_preco)
        
        
        ultimo_id_vendas= banco.execute_sql('SELECT last_value FROM vendas_id_venda_seq')
        ultimo_id=[]
        
        for ii in ultimo_id_vendas:
            ultimo_id.append( *ii )
            #print(ultimo_id[0])
        
            
        quantidade_produto_venda =   float(input("quantidade de venda : "))
        print(f'Valor Total ',round(select_produto_venda_preco*quantidade_produto_venda,2))
        print()
        #valor_venda = Produto.select(Produto.preco_pro).where(Produto.
        novo_estoque=float(round(select_produto_venda-quantidade_produto_venda,4))
        
        
        select_cadastro_adminstradora = Administradora.select(Administradora.tipo_adm).distinct().order_by(Administradora.tipo_adm)
        ordem=1
        lista_classe ={}
        
        print("Escolha o tipo de pagamento")
        for i in select_cadastro_adminstradora:

            print(ordem,'-',i.tipo_adm)
            lista_classe[ordem]=i.tipo_adm
            ordem +=1
            
        print()
        classe_pesquisa = int(input("Tipo de Pagamento: "))
        print()


        select_lista_adm =Administradora.select().where(Administradora.tipo_adm == lista_classe[classe_pesquisa])

        
        ordem1=1
        lista_classe1 ={}
        
        print("Escolha o pagamento")
        for ii in select_lista_adm:

            print(ordem1,'-',ii.nome_adm)
            lista_classe1[ordem1]=ii.nome_adm
            ordem1 +=1
        print() 
        
        pagamento_adm = int(input("Pagamento: "))
        
        update_estoque=Produto.update({Produto.estoque_pro:novo_estoque}).where(Produto.id_pro == id_produto_venda)
        update_estoque.execute()  

        select_lista_adm_tipo =Administradora.select().where(Administradora.nome_adm == lista_classe1[pagamento_adm])
        
        for io in select_lista_adm_tipo:
            
            pagamento_tipo_adm=io.id_adm
            
        
        Vendas.create(formapag=pagamento_tipo_adm,
                      pessoa_venda=1,
                      data_venda= time.strftime('%Y-%m-%d'),#datetime.now()
                      
                      ).get
       # print(Vendas.id_venda)
       # if Vendas.select(fn.count(Vendas.id_venda)).scalar() == 2:
        #    ultimo_id[0]=2
        #    print(ultimo_id[0])
            
        ItemVenda.create(id_vendas_item=ultimo_id[0],id_produto_item_venda = id_produto_venda,
                         quantidade_item_venda=quantidade_produto_venda,
                         valor_unitario = float(select_produto_venda_preco),
                         valor_total =float(round(select_produto_venda_preco*quantidade_produto_venda,2)),
                         data_item_venda = datetime.now()
                         )
        

        banco.close()
        
def venda_venda():
        print("Escolha o Cliente a ser feito a venda")
        print()
        lista_clientes()

        cliente_escolhido = int(input("Digite o codigo do Cliente : "))


        lista_classes() 
        
        id_produto_venda =   int(input("Digite o Id do Produto : "))
        
        select_produto_venda =Produto.select(Produto.estoque_pro).where(Produto.id_pro == id_produto_venda).scalar()
        select_produto_venda = float(select_produto_venda)
        
        select_produto_venda_preco =Produto.select(Produto.preco_pro).where(Produto.id_pro == id_produto_venda).scalar()
        select_produto_venda_preco = float(select_produto_venda_preco)
        
        
        ultimo_id_vendas= banco.execute_sql('SELECT last_value FROM vendas_id_venda_seq')
        ultimo_id=[]
        
        for ii in ultimo_id_vendas:
            ultimo_id.append( *ii )
            

        if ultimo_id[0] == 1:
            Vendas.create()
            
        quantidade_produto_venda =   float(input("quantidade de venda : "))
        valor_total=round(select_produto_venda_preco*quantidade_produto_venda,2)

        print(f'Valor Total ',valor_total)

        print()

        novo_estoque=float(round(select_produto_venda-quantidade_produto_venda,4))
        valor_pago1=0
        
        Vendas.create(
                      pessoa_venda=cliente_escolhido,
                      data_venda= time.strftime('%Y-%m-%d'),#datetime.now()
                      valor_total_venda = valor_total
                      )#.get
        
        while valor_total != valor_pago1:


            select_cadastro_adminstradora = Administradora.select(Administradora.tipo_adm).distinct().order_by(Administradora.tipo_adm)
            ordem=1
            lista_classe ={}


            print("Escolha o tipo de pagamento")
            for i in select_cadastro_adminstradora:

                print(ordem,'-',i.tipo_adm)
                lista_classe[ordem]=i.tipo_adm
                ordem +=1

            print()
            classe_pesquisa = int(input("Tipo de Pagamento: "))
            print()


            select_lista_adm =Administradora.select().where(Administradora.tipo_adm == lista_classe[classe_pesquisa])


            ordem1=1
            lista_classe1 ={}

            print("Escolha o pagamento")


            for ii in select_lista_adm:

                print(ordem1,'-',ii.nome_adm)
                lista_classe1[ordem1]=ii.nome_adm
                ordem1 +=1
            print() 


            pagamento_adm = int(input("Pagamento: "))


            valor_pago=float(input("Valor a ser pago: "))
            valor_pago1 = valor_pago1 + valor_pago
            
            falta_valor(valor_total,valor_pago1)

            select_lista_adm_tipo =Administradora.select().where(Administradora.nome_adm == lista_classe1[pagamento_adm])


            for io in select_lista_adm_tipo:

                pagamento_tipo_adm=io.id_adm

            FormasPag.create(nome_formaspag =lista_classe1[pagamento_adm],
                         valor_formaspag=valor_pago,
                         item_venda_formaspag = ultimo_id[0]+1,
                         id_adm_formaspag = pagamento_tipo_adm
                         )

            
        ItemVenda.create(id_vendas_item=ultimo_id[0]+1,id_produto_item_venda = id_produto_venda,
                         quantidade_item_venda=quantidade_produto_venda,
                         valor_unitario = float(select_produto_venda_preco),
                         valor_total =valor_total,
                         data_item_venda = datetime.now()
                         )


        update_estoque=Produto.update({Produto.estoque_pro:novo_estoque}).where(Produto.id_pro == id_produto_venda)
        update_estoque.execute() 

        banco.close()
        input("")


        
banco.close()
