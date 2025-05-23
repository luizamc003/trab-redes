import socket
import threading

THREADS_NUM = 10

status_threads = [True] * THREADS_NUM # coloca todas as threads como livre, vamos usar true = livre

def handle_conn(conn: socket.socket, id_thread: int):
    
    with conn:
        print(f"Conectado! Executando na thread {id_thread}")
        while True:
            entradaBytes = conn.recv(1024) # fica recebendo dados
             
            entradaStr = entradaBytes.decode('utf-8') # recebe em bytes, entao tem que decodificar
            entrada = entradaStr.split() # transforma em lista pra poder mexer mais abaixo
            
            try: # confere os comandos
                if entrada[0] == 'echo':
                    conn.sendall(entradaStr.replace('echo ','').encode('utf-8'))
                if entrada[0] == 'quit':
                    print(f"[Thread {id_thread}] Saindo!")
                    conn.sendall("\nSaindo!\n\n".encode('utf-8'))
                    break

            except IndexError: # caso o usuario tenha apertado so o Enter
                print(f"[Thread {id_thread}] Erro na entrada. Está vazia?")
            else: # se der tudo certo, mostra o que recebeu sem o \n
                print(f"[Thread {id_thread}] Recebi: {entradaStr.replace('\n','')}") 
    
    status_threads[id_thread] = True # desocupa a thread
    conn.close()
    

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reuso de endereço, serve pra nao ter que mudar a porta toda hora

soc.bind(('127.0.0.1', 1337))

soc.listen() # escutando

while True:
    conn, ad = soc.accept() # aceita conexões

    if True in status_threads:
        id = status_threads.index(True)

        thread = threading.Thread(target=handle_conn, args=(conn,id,))
        thread.daemon = True # nao bloqueia
        thread.start()
        
        status_threads[id] = False # ocupa a thread

    else:
        conn.sendall("Todas as threads estão ocupadas, aguarde um pouco\n\n".encode('utf-8'))
        conn.close()


