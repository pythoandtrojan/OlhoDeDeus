# modulos/linkedIn.py

import os
from colorama import Fore, Style, init

init(autoreset=True)

class LinkedInDatabase:
    def __init__(self, arquivo_path="dados/br.linkedin.com_LP-40000.txt"):
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
            
            print(Fore.GREEN + f"Carregados {len(self.dados)} registros")
            return True
            
        except Exception as e:
            print(Fore.RED + f"Erro: {str(e)}")
            return False
    
    def buscar(self, usuario=None):
        try:
            if usuario:
                resultados = [item for item in self.dados if item['usuario'].lower() == usuario.lower()]
                if not resultados:
                    print(Fore.RED + f"Usuário '{usuario}' não encontrado!")
                    return None
            else:
                resultados = self.dados
                if not resultados:
                    print(Fore.YELLOW + "Banco de dados vazio!")
                    return None
            
            self._mostrar_tabela(resultados, usuario if usuario else "TODOS OS REGISTROS")
            return resultados
            
        except Exception as e:
            print(Fore.RED + f"Erro na busca: {str(e)}")
            return None
    
    def salvar(self, dados=None, nome_arquivo="linkedin_resultado.txt"):
        try:
            if dados is None:
                dados = self.dados
            
            if not dados:
                print(Fore.YELLOW + "Nenhum dado para salvar!")
                return False
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(f"LinkedIn Database - {len(dados)} registros\n")
                f.write("=" * 80 + "\n")
                for item in dados:
                    f.write(f"{item['usuario']}:{item['senha']}\n")
            
            print(Fore.GREEN + f"Salvo em: {nome_arquivo}")
            return True
            
        except Exception as e:
            print(Fore.RED + f"Erro ao salvar: {str(e)}")
            return False
    
    def buscar_ou_salvar(self, usuario=None, salvar=False, nome_arquivo=None):
        resultados = self.buscar(usuario)
        
        if resultados and salvar:
            nome = nome_arquivo if nome_arquivo else f"resultado_{usuario if usuario else 'todos'}.txt"
            self.salvar(resultados, nome)
        
        return resultados
    
    def _mostrar_tabela(self, dados, titulo):
        print("\n" + "=" * 90)
        print(Fore.CYAN + Style.BRIGHT + f" LinkedIn - {titulo}")
        print("=" * 90)
        
        print(f"{Fore.YELLOW}{'#' :<6} {Fore.GREEN}{'USUÁRIO' :<40} {Fore.BLUE}{'SENHA' :<40}")
        print(Fore.WHITE + "-" * 90)
        
        for i, item in enumerate(dados, 1):
            usuario = item['usuario'][:38] if len(item['usuario']) > 38 else item['usuario']
            senha = item['senha'][:38] if len(item['senha']) > 38 else item['senha']
            
            cor_usuario = Fore.GREEN if i % 2 == 0 else Fore.YELLOW
            print(f"{cor_usuario}{i :<6} {Fore.WHITE}{usuario :<40} {Fore.BLUE}{senha :<40}")
        
        print(Fore.WHITE + "-" * 90)
        print(Fore.MAGENTA + f"Total: {len(dados)} registros")
        print("=" * 90 + "\n")
