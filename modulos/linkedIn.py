# modulos/linkedIn.py

import os
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

class LinkedInDatabase:
    def __init__(self, arquivo_path=None):
        if arquivo_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            arquivo_path = os.path.join(base_dir, "dados", "br.linkedin.com_LP-40000.txt")
        self.arquivo_path = arquivo_path
        self.dados = []
        self.carregar_dados()
    
    def carregar_dados(self):
        try:
            if not os.path.exists(self.arquivo_path):
                print(Fore.RED + f"Erro: Arquivo '{self.arquivo_path}' não encontrado!")
                return False
            
            with open(self.arquivo_path, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha and ':' in linha:
                        usuario, senha = linha.split(':', 1)
                        self.dados.append({'usuario': usuario, 'senha': senha})
            
            print(Fore.GREEN + f"✓ Carregados {len(self.dados)} registros do LinkedIn")
            return True
            
        except Exception as e:
            print(Fore.RED + f"Erro: {str(e)}")
            return False
    
    def mostrar_todos(self):
        if not self.dados:
            print(Fore.YELLOW + "Nenhum dado no banco de dados!")
            return None
        
        tabela = []
        for i, item in enumerate(self.dados, 1):
            tabela.append([i, item['usuario'], item['senha']])
        
        print(Fore.CYAN + "\n📊 TODOS OS REGISTROS DO BANCO DE DADOS")
        print(tabulate(tabela, headers=["#", "USUÁRIO", "SENHA"], tablefmt="rounded_grid"))
        print(Fore.MAGENTA + f"\n📌 Total: {len(self.dados)} registros\n")
        
        return self.dados
    
    def buscar_usuario(self, usuario):
        try:
            if not usuario:
                print(Fore.YELLOW + "Digite um usuário válido!")
                return None
            
            resultados = [item for item in self.dados if item['usuario'].lower() == usuario.lower()]
            
            if not resultados:
                print(Fore.RED + f"❌ Usuário '{usuario}' não encontrado!")
                return None
            
            tabela = []
            for i, item in enumerate(resultados, 1):
                tabela.append([i, item['usuario'], item['senha']])
            
            print(Fore.CYAN + f"\n🔍 RESULTADO PARA: {usuario}")
            print(tabulate(tabela, headers=["#", "USUÁRIO", "SENHA"], tablefmt="rounded_grid"))
            print(Fore.MAGENTA + f"\n📌 Encontrado: {len(resultados)} registro(s)\n")
            
            return resultados
            
        except Exception as e:
            print(Fore.RED + f"Erro na busca: {str(e)}")
            return None
    
    def buscar_senha(self, senha):
        try:
            if not senha:
                print(Fore.YELLOW + "Digite uma senha válida!")
                return None
            
            resultados = [item for item in self.dados if item['senha'] == senha]
            
            if not resultados:
                print(Fore.RED + f"❌ Nenhum registro com a senha fornecida!")
                return None
            
            tabela = []
            for i, item in enumerate(resultados, 1):
                tabela.append([i, item['usuario'], item['senha']])
            
            print(Fore.CYAN + f"\n🔍 RESULTADO PARA SENHA: {senha[:20]}...")
            print(tabulate(tabela, headers=["#", "USUÁRIO", "SENHA"], tablefmt="rounded_grid"))
            print(Fore.MAGENTA + f"\n📌 Encontrado: {len(resultados)} registro(s)\n")
            
            return resultados
            
        except Exception as e:
            print(Fore.RED + f"Erro na busca: {str(e)}")
            return None
    
    def salvar(self, dados=None, nome_arquivo="linkedin_export.txt"):
        try:
            if dados is None:
                dados = self.dados
            
            if not dados:
                print(Fore.YELLOW + "Nenhum dado para salvar!")
                return False
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(f"LinkedIn Database Export - {len(dados)} registros\n")
                f.write("=" * 80 + "\n")
                f.write(f"{'USUÁRIO':<40} {'SENHA':<40}\n")
                f.write("-" * 80 + "\n")
                for item in dados:
                    f.write(f"{item['usuario']:<40} {item['senha']:<40}\n")
                f.write("=" * 80 + "\n")
            
            print(Fore.GREEN + f"✓ Dados salvos em: {nome_arquivo}")
            return True
            
        except Exception as e:
            print(Fore.RED + f"Erro ao salvar: {str(e)}")
            return False
    
    def buscar_e_salvar(self, usuario=None, salvar=True):
        if usuario:
            resultados = self.buscar_usuario(usuario)
        else:
            resultados = self.mostrar_todos()
        
        if resultados and salvar:
            nome = f"export_{usuario if usuario else 'todos'}.txt"
            self.salvar(resultados, nome)
        
        return resultados
