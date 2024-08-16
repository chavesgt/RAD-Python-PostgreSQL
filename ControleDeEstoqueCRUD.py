import psycopg2

class AppBD:
    def __init__(self):
        print('Método Construtor')
        
    def abrirConexao(self):
        try:
          self.connection = psycopg2.connect(user="postgres",
                                  password="576171",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="lojaroupa")
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)
#-----------------------------------------------------------------------------
#Selecionar todos os Produtos
#-----------------------------------------------------------------------------                 
    def selecionarDados(self):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
    
            print("Carregando os produtos")
            sql_select_query = """select * from public."produtos" """
                    
            
            cursor.execute(sql_select_query)
            registros = cursor.fetchall()             
            print(registros)
                
    
        except (Exception, psycopg2.Error) as error:
            print("Error in select operation", error)
    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
        return registros
      
#-----------------------------------------------------------------------------
#Inserir Produto
#-----------------------------------------------------------------------------                 
    def inserirDados(self, codigo, nome, quantidade):
        try:
          self.abrirConexao()
          cursor = self.connection.cursor()
          postgres_insert_query = """ INSERT INTO public."produtos" 
          ("codigo", "nome", "quantidade") VALUES (%s,%s,%s)"""
          record_to_insert = (codigo, nome, quantidade)
          cursor.execute(postgres_insert_query, record_to_insert)
          self.connection.commit()
          count = cursor.rowcount
          print (count, "Produto cadastrado com sucesso!")
        except (Exception, psycopg2.Error) as error :
          if(self.connection):
              print("Falha ao inserir produto", error)
        finally:
            #closing database connection.
            if(self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
                
#-----------------------------------------------------------------------------
#Atualizar Produto
#-----------------------------------------------------------------------------                 
    def atualizarDados(self, codigo, nome, quantidade):
        try:
            self.abrirConexao()    
            cursor = self.connection.cursor()

            print("Registro Antes de editar")
            sql_select_query = """select * from public."produtos" 
            where "codigo" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)    
            # Atualizar registro
            sql_update_query = """Update public."produtos" set "nome" = %s, 
            "quantidade" = %s where "codigo" = %s"""
            cursor.execute(sql_update_query, (nome, quantidade, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Produto atualizado com sucesso! ")    
            print("Registro Depois da Atualização ")
            sql_select_query = """select * from public."produtos" 
            where "codigo" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)    
        except (Exception, psycopg2.Error) as error:
            print("Erro na Atualização", error)    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

#-----------------------------------------------------------------------------
#Excluir Produto
#-----------------------------------------------------------------------------                 
    def excluirDados(self, codigo):
        try:
            self.abrirConexao()    
            cursor = self.connection.cursor()    
            # Atualizar registro
            sql_delete_query = """Delete from public."produtos" 
            where "codigo" = %s"""
            cursor.execute(sql_delete_query, (codigo, ))

            self.connection.commit()
            count = cursor.rowcount
            print(count, "Produto excluído com sucesso! ")        
        except (Exception, psycopg2.Error) as error:
            print("Erro na Exclusão", error)    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
                
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import crud as crud

class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()  
        #componentes
        self.lbCodigo=tk.Label(win, text='Código do Produto:')
        self.lblNome=tk.Label(win, text='Nome do Produto:')
        self.lblQuantidade=tk.Label(win, text='Quantidade:')
        
        self.txtCodigo=tk.Entry(bd=3)
        self.txtNome=tk.Entry()
        self.txtQuantidade=tk.Entry()        
        self.btnInserir=tk.Button(win, text='Inserir', command=self.fInserirProduto)        
        self.btnAtualizar=tk.Button(win, text='Editar', command=self.fEditarProduto)        
        self.btnExcluir=tk.Button(win, text='Excluir', command=self.fExcluirProduto)        
        self.btnLimpar=tk.Button(win, text='Limpar', command=self.fLimparTela)                
        #----- Componente TreeView --------------------------------------------
        self.dadosColunas = ("Código", "Nome", "Quantidade")            
                
        self.treeProdutos = ttk.Treeview(win, 
                                       columns=self.dadosColunas,
                                       selectmode='browse')
        
        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeProdutos.yview)        
        self.verscrlbar.pack(side ='right', fill ='x')
                                
        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)
        
        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Quantidade", text="Quantidade")        

        self.treeProdutos.column("Código",minwidth=0,width=100)
        self.treeProdutos.column("Nome",minwidth=0,width=100)
        self.treeProdutos.column("Quantidade",minwidth=0,width=100)

        self.treeProdutos.pack(padx=10, pady=10)
        
        self.treeProdutos.bind("<<TreeviewSelect>>", 
                               self.apresentarRegistrosSelecionados)                  
        #---------------------------------------------------------------------        
        #posicionamento dos componentes na janela
        #---------------------------------------------------------------------                
        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)
        
        self.lblNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)
        
        self.lblQuantidade.place(x=100, y=150)
        self.txtQuantidade.place(x=250, y=150)
               
        self.btnInserir.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
                   
        self.treeProdutos.place(x=100, y=300)
        self.verscrlbar.place(x=605, y=300, height=225)        
        self.carregarDadosIniciais()
#-----------------------------------------------------------------------------
    def apresentarRegistrosSelecionados(self, event):  
        self.fLimparTela()  
        for selection in self.treeProdutos.selection():  
            item = self.treeProdutos.item(selection)  
            codigo,nome,quantidade = item["values"][0:3]  
            self.txtCodigo.insert(0, codigo)  
            self.txtNome.insert(0, nome)  
            self.txtQuantidade.insert(0, quantidade)  
#-----------------------------------------------------------------------------
    def carregarDadosIniciais(self):
        try:
          self.id = 0
          self.iid = 0          
          registros=self.objBD.selecionarDados()
          print("************ Dados Disponíveis no BD ***********")        
          for item in registros:
              codigo=item[0]
              nome=item[1]
              quantidade=item[2]
              print("Código = ", codigo)
              print("Nome = ", nome)
              print("Quantidade  = ", quantidade, "\n")
                        
              self.treeProdutos.insert('', 'end',
                                   iid=self.iid,                                   
                                   values=(codigo,
                                           nome,
                                           quantidade))                        
              self.iid = self.iid + 1
              self.id = self.id + 1
          print('Dados da Base')        
        except:
          print('Ainda não existem dados para carregar')            
#-----------------------------------------------------------------------------
#LerDados da Tela
#-----------------------------------------------------------------------------           
    def fLerCampos(self):
        try:
          print("************ Dados Disponíveis ***********") 
          codigo = int(self.txtCodigo.get())
          print('codigo', codigo)
          nome=self.txtNome.get()
          print('nome', nome)
          quantidade=int(self.txtQuantidade.get())          
          print('quantidade', quantidade)
          print('Leitura dos Dados com Sucesso!')        
        except:
          print('Não foi possível ler os dados.')
        return codigo, nome, quantidade
#-----------------------------------------------------------------------------
#Cadastrar Produto
#-----------------------------------------------------------------------------           
    def fInserirProduto(self):
        try:
          print("************ Dados disponíveis ***********") 
          codigo, nome, quantidade= self.fLerCampos()                    
          self.objBD.inserirDados(codigo, nome, quantidade)                    
          self.treeProdutos.insert('', 'end',
                                iid=self.iid,                                   
                                values=(codigo,
                                        nome,
                                        quantidade))                        
          self.iid = self.iid + 1
          self.id = self.id + 1
          self.fLimparTela()
          print('Produto Cadastrado com Sucesso!')        
        except:
          print('Não foi possível fazer o cadastro.')
#-----------------------------------------------------------------------------
#Atualizar Produto
#-----------------------------------------------------------------------------           
    def fEditarProduto(self):
        try:
          print("************ Dados disponíveis ***********")        
          codigo, nome, quantidade= self.fLerCampos()
          self.objBD.atualizarDados(codigo, nome, quantidade)          
          #recarregar dados na tela
          self.treeProdutos.delete(*self.treeProdutos.get_children()) 
          self.carregarDadosIniciais()
          self.fLimparTela()
          print('Produto Atualizado com Sucesso!')        
        except:
          print('Não foi possível fazer a atualização.')
#-----------------------------------------------------------------------------
#Excluir Produto
#-----------------------------------------------------------------------------                  
    def fExcluirProduto(self):
        try:
          print("************ Dados disponíveis ***********")        
          codigo, nome, quantidade= self.fLerCampos()
          self.objBD.excluirDados(codigo)          
          #recarregar dados na tela
          self.treeProdutos.delete(*self.treeProdutos.get_children()) 
          self.carregarDadosIniciais()
          self.fLimparTela()
          print('Produto Excluído com Sucesso!')        
        except:
          print('Não foi possível fazer a exclusão do produto.')
#-----------------------------------------------------------------------------
#Limpar Tela
#-----------------------------------------------------------------------------                 
    def fLimparTela(self):
        try:
          print("************ dados dsponíveis ***********")        
          self.txtCodigo.delete(0, tk.END)
          self.txtNome.delete(0, tk.END)
          self.txtQuantidade.delete(0, tk.END)
          print('Campos Limpos!')        
        except:
          print('Não foi possível limpar os campos.')
#-----------------------------------------------------------------------------
#Programa Principal
#-----------------------------------------------------------------------------          
janela=tk.Tk()
principal=PrincipalBD(janela)
janela.title('Controle De Estoque Loja Roupas R&N Modas')
janela.geometry("720x600+10+10")
janela.mainloop()
#-----------------------------------------------------------------------------




