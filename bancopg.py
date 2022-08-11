from peewee import *
from datetime import *


banco= PostgresqlDatabase(
    'teste',
    user = 'postgres',
    password='123456',
    host = 'localhost',
    port = 5433
)



class BaseModel(Model):
    class Meta : 
        database = banco



class Endereco(BaseModel):
    id_endereco = AutoField ()
    logradouro_end = CharField(max_length=50,null=True)
    numero_end = IntegerField(null=True)
    bairro_end = CharField(max_length=50,null=True)
    cep_end = IntegerField(null=True)
    cidade_end = CharField(max_length=100,null=True)
    uf_end= CharField(null=True)
    complemento_end = CharField(max_length=32,null=True)
    md5_end = CharField(max_length=32,null=True,unique=True)

class Telefone(BaseModel):
    id_tel = AutoField ()
    telefone = CharField(max_length=32,null=True)
    md5_tel = CharField(max_length=32,null=False)

class Pessoa(BaseModel):
    
    id_pes = AutoField()#(primary_key=True,null = False)#unique=True)
    nome_pes = CharField(max_length=60,null=False)
    nome_fantasia= CharField(max_length=60,null=True)
    id_end =ForeignKeyField(column_name='id_end', field='id_endereco', model=Endereco ,null = True)
    id_telefone = ForeignKeyField(column_name='id_telefone', field='id_tel', model=Telefone, null = True, unique=False)
    md5_pes = CharField(max_length=32,null=False,unique=True)
    cadastro_api_pes = CharField(max_length=3,null=True)

class Data(BaseModel):

    criacao = CharField()#DateTimeField(default=datetime.now)
    modificacao = DateTimeField(default=datetime.now)
    nascimento = DateTimeField(default=datetime.now)
    batismo = DateTimeField(default=datetime.now)
    md5_dt = CharField(max_length=32,null=False)


class Produto(BaseModel):
    id_pro = AutoField()
    nome_pro  = CharField(max_length=60,null=True)
    preco_pro = CharField(constraints=[SQL("DEFAULT 0")],null=True)
    classe_pro =CharField(max_length=60,null=True)
    estoque_pro = CharField(constraints=[SQL("DEFAULT 0")],max_length=15,null=True)
    unidade_pro =CharField(null=True)
    cadastro_api_pro = CharField(max_length=3,null=True)


class Administradora(BaseModel):
    id_adm = AutoField ()
    nome_adm = CharField(max_length=20,null=True)
    tipo_adm = CharField(max_length=50,null=True)
    cadastro_api_adm=CharField(null=True)


class Vendas(BaseModel):
    id_venda = AutoField ()
    formapag = ForeignKeyField(column_name='formapag', field='id_adm', model=Administradora,null = True)
    pessoa_venda = ForeignKeyField(column_name='pessoa_venda', field='id_pes', model=Pessoa,constraints=[SQL("DEFAULT 1")],null = True)
    data_venda = DateTimeField( null=True )
    
    
class ItemVenda(BaseModel):
    id_item_venda = AutoField ()
    id_vendas_item=ForeignKeyField(column_name='id_vendas_item', field='id_venda', model=Vendas ,null = True)
    id_produto_item_venda = ForeignKeyField(column_name='id_produto_venda', field='id_pro', model=Produto ,null = True)
    quantidade_item_venda = CharField(null=True)
    valor_unitario =CharField(null=True)
    valor_total =CharField(null=True)
    data_item_venda = DateTimeField( null = True)
    #data_item_venda = DateTimeField(formats=['dd-MM-yyyy HH:mm:ss'], null = True)

    #md5_item_venda = CharField(max_length=32,null=True,unique=True)


def cria_banco():
    banco.create_tables([Pessoa,Endereco,Data,Telefone,Produto,Administradora,ItemVenda,Vendas])

def apaga_banco():   
    banco.drop_tables([Pessoa,Endereco,Data,Telefone,Produto,Administradora,ItemVenda,Vendas] ,cascade=True)
