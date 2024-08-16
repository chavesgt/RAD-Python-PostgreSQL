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
    
            print("Selecionando todos os produtos")
            sql_select_query = """select * from public."produtos" """
                    
            
            cursor.execute(sql_select_query)
            registros = cursor.fetchall()             
            print(registros)
                
    
        except (Exception, psycopg2.Error) as error:
            print("Erroba na Seleção", error)
    
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
          print (count, "Registro inserido com successo na tabela PRODUTOS")
        except (Exception, psycopg2.Error) as error :
          if(self.connection):
              print("Falha ao inserir registro na tabela PRODUTOS", error)
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

            print("Registro Antes da Atualização ")
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
            print(count, "Registro atualizado com sucesso! ")    
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
            print(count, "Registro excluído com sucesso! ")        
        except (Exception, psycopg2.Error) as error:
            print("Erro na Exclusão", error)    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
                
#-----------------------------------------------------------------------------
