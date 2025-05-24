import socket

HOST = "127.0.0.1"
PORTA = 1337

# Cria um socket e o conecta no host e porta especificados
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORTA))

while True:
    
    # Aguarda entrada do usuario para mandar ao host
    msg = input("> ")
    try:
    
        # Tenta enviar a mensagem
        soc.send(msg.encode('utf-8'))
    
    # Confere se a conexão ainda existe
    except BrokenPipeError:
        print('Servidor encerrou a conexão')
        break
    
    # Se a mensagem nao for vazia, tenta receber a resposta
    if msg:
        resposta = soc.recv(1024)
        
        # Habilita possibilidade de sair via comando do client
        if msg == 'quit':
            break

        # Decodifica a resposta (bytes -> string)
        print(f"{resposta.decode('utf-8')}")

# Fecha a conexão
soc.close()
