import socket
import threading

HOST = '127.0.0.1'
PORTA = 1337

THREADS_NUM = 10 # define o numero de threads

status_threads = [True] * THREADS_NUM # coloca todas as threads como livre, vamos usar True = livre

def finaliza_conn(conn, id_thread): # marca o status da thread como livre e desconecta
    status_threads[id_thread] = True 
    conn.close()

def handle_conn(conn: socket.socket, id_thread: int):
    # Esse contador serve para identificar quando uma conexão morreu de forma inesperada
    contador_vazias = 0
    with conn:
        print(f"Conectado! Executando na thread {id_thread}")
        while True:
            # Recebe dados
            entradaBytes = conn.recv(1024) 
            if not entradaBytes:
                break

            # Recebe em bytes, entao precisamos decodificar
            entradaStr = entradaBytes.decode('utf-8') 
            # Transforma em lista pra poder avaliar os comandos
            entrada = entradaStr.split() 
            
            try: 
                # Confere os comandos
                if entrada[0] == 'echo':
                    conn.sendall(entradaStr.replace('echo ','').encode('utf-8'))

                elif entrada[0] == 'quit':
                    print(f"[Thread {id_thread}] Saindo!")
                    break

                else:
                    # Se nao for um comando, envia um espaço para que o cliente nao trave no recebimento
                    conn.sendall(' '.encode('utf-8'))

            # Caso a mensagem seja vazia
            except IndexError: 
                print(f"[Thread {id_thread}] Erro na entrada. Está vazia?")
                conn.sendall(' '.encode('utf-8'))
                # Usa-se o contador para verificar se a conexão morreu. Na 5° mensagem vazia seguida, fecha a conexao
                contador_vazias += 1
                if contador_vazias == 5:
                    break

            except Exception as e:
                print(f"[Thread {id_thread}] Erro desconhecido!")
                
            else: 
                # Se der tudo certo, mostra o que recebeu sem o \n
                print(f"[Thread {id_thread}] Recebi: {entradaStr.replace('\n','')}") 
                contador_vazias = 0
    
    finaliza_conn(conn, id_thread)
    

# Criamos um socket, permitimos o reuso de endereço/porta para não precisar trocar a cada execução (detalhe da biblioteca)
# e ouvimos no host/porta que configuramos acima
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reuso de endereço, serve pra nao ter que mudar a porta toda hora
soc.bind((HOST, PORTA))
soc.listen() # escutando

while True:
    # Cceita conexões
    conn, ad = soc.accept() 

    # Se houver alguma thread livre
    if True in status_threads:
        # Identificamos o ID da thread (seu indice no array) e a disparamos para cuidar da conexão
        id = status_threads.index(True)
        thread = threading.Thread(target=handle_conn, args=(conn,id,))
        thread.daemon = True # Não bloqueia a principal
        thread.start() # Inicia a thread

        # Ocupa a thread
        status_threads[id] = False 

    else:
        # Se nenhuma thread estiver livre
        conn.sendall("Todas as threads estão ocupadas, aguarde um pouco\n\n".encode('utf-8'))
        conn.close()

