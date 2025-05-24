import socket
import threading

def handle_conn(conn: socket.socket):
    thread_name = threading.current_thread().name # pega o nome da thread, vem no formato "Thread-X (funcao)"
    thread_number = thread_name[:thread_name.find(' ')] # pega o numero da thread
    contador_vazias = 0
    with conn:
        print(f"Conectado! Executando na thread {thread_number}")
        while True:
            entradaBytes = conn.recv(1024) # fica recebendo dados
             
            entradaStr = entradaBytes.decode('utf-8') # recebe em bytes, entao tem que decodificar
            entrada = entradaStr.split() # transforma em lista pra poder mexer mais abaixo
            
            try: # confere os comandos
                if entrada[0] == 'echo':
                    conn.sendall(entradaStr.replace('echo ','').encode('utf-8'))
                if entrada[0] == 'quit':
                    print(f"[Thread {thread_number}] Saindo!")
                    # conn.sendall("\nSaindo!\n\n".encode('utf-8'))
                    break
                else:
                    conn.sendall(' '.encode('utf-8'))

            except IndexError: # caso o usuario tenha apertado so o Enter
                print(f"[Thread {thread_number}] Erro na entrada. Está vazia?")
                contador_vazias += 1
                if contador_vazias == 5: # na 5° mensagem vazia fecha a conexao
                    break

            except Exception:
                print(f"[Thread {thread_number}] Erro desconhecido!")
            else: # se der tudo certo, mostra o que recebeu sem o \n
                print(f"[Thread {thread_number}] Recebi: {entradaStr.replace('\n','')}") 
                contador_vazias = 0
    

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reuso de endereço, serve pra nao ter que mudar a porta toda hora
soc.bind(('127.0.0.1', 1337))
soc.listen() # escutando

while True:
    conn, ad = soc.accept() # aceita conexões
    thread = threading.Thread(target=handle_conn, args=(conn,))
    thread.start()

