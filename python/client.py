import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 1337))

while True:
    msg = input("> ")
    try:
        soc.send(msg.encode('utf-8'))
    except BrokenPipeError:
        print('Servidor encerrou a conexão')
        break
    if msg:
        resposta = soc.recv(1024)
        if msg == 'quit':
            break

        print(f"{resposta.decode('utf-8')}")



soc.close()
