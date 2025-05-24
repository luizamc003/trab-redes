import socket
import threading

HOST = '127.0.0.1'
PORTA = 1337

def handle_conn(conn: socket.socket):
    # Pega o nome da thread, vem no formato "Thread-X <Função>"
    thread_name = threading.current_thread().name 
    # Pega o numero da thread
    thread_number = thread_name[:thread_name.find(' ')]
    # Esse contador é usado mais abaixo para garantir que uma conexão foi encerrada de maneira inesperada. Assim, fechamos a conexão.
    contador_vazias = 0
    with conn:
        print(f"Conectado! Executando na thread {thread_number}")
        while True:
            # Fica recebendo dados
            entradaBytes = conn.recv(1024) 
            # Recebe em bytes, entao tem que decodificar p/ string
            entradaStr = entradaBytes.decode('utf-8') 
            # Transforma em lista pra poder avaliar comandos
            entrada = entradaStr.split() 
            
            try: 
                # Confere os comandos
                if entrada[0] == 'quit':
                    print(f"[Thread {thread_number}] Saindo!")
                    break

                else:
                    # Como essa implemetação é um SERVIDOR ECHO, repete o que foi enviado
                    conn.sendall(entradaStr.encode('utf-8'))

            except IndexError:
                # Mensagem vazia por acidente do client. Aqui aumentamos o contador_vazias. Se ele chegar a 5 (5 mensagens vazias seguidas)
                # entao, encerramos a conexão
                print(f"[Thread {thread_number}] Erro na entrada. Está vazia?")
                contador_vazias += 1
                if contador_vazias == 5: # na 5° mensagem vazia fecha a conexao
                    break

            except Exception:
                print(f"[Thread {thread_number}] Erro desconhecido!")
            else: 
                # Se der tudo certo, mostra o que recebeu sem o \n e reseta o contador_vazias, pois a conexão não foi encerrada
                print(f"[Thread {thread_number}] Recebi: {entradaStr.replace('\n','')}") 
                contador_vazias = 0
    

# Cria um socket, o conecta no host e porta especificados e escuta
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reuso de endereço, serve pra nao ter que mudar a porta a cada execução (detalhe da implementação do python)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

soc.bind((HOST, PORTA))
soc.listen() 

while True:
    conn, ad = soc.accept() # aceita conexões
    thread = threading.Thread(target=handle_conn, args=(conn,)) # cria thread
    thread.start() # Dispara thread para a conexão

