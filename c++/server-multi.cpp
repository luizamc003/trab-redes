#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <cstring>
#include <unistd.h>
#include <thread>

// para comunicação com cliente
void handleClient(int clientSocket)
{

    // /ID da thread que está lidando com o cliente
    std::cout << "Thread ID: " << std::this_thread::get_id() << " handling client" << std::endl;

    // armazenando dados do cliente
    char buffer[1024];
    std::memset(buffer, 0, sizeof(buffer));

    // loop para ler mensagens do cliente
    while (true)
    {
        // lê os dados enviados pelo cliente
        ssize_t bytesRead = read(clientSocket, buffer, sizeof(buffer) - 1);
        if (bytesRead <= 0) // se o cliente desconectar ou ocorrer um erro
        {
            break;
        }

        buffer[bytesRead] = '\0';                         // tratar os dados como string
        std::cout << "Received: " << buffer << std::endl; // dados recebidos

        // echo
        ssize_t bytesWritten = 0;
        while (bytesWritten < bytesRead) // garante que todos os dados sejam enviados
        {
            ssize_t result = write(clientSocket, buffer + bytesWritten, bytesRead - bytesWritten);
            if (result <= 0) // Se ocorrer um erro durante o envio
            {
                break;
            }
            bytesWritten += result;
        }
    }

    std::cout << "Closing connection with client" << std::endl;
    close(clientSocket);
}

int main()
{
    int port = 4444; // porta

    // socket
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == -1)
    {
        std::cerr << "Failed to create socket!" << std::endl;
        return -1;
    }

    // configurando servidor
    sockaddr_in serverAddr;
    std::memset(&serverAddr, 0, sizeof(serverAddr)); // inicializa a estrutura com zeros
    serverAddr.sin_family = AF_INET;                 // IPv4
    serverAddr.sin_addr.s_addr = INADDR_ANY;         // Aaeita conexões de qualquer endereço IP
    serverAddr.sin_port = htons(port);               // define a porta do servidor (convertida para big-endian)

    // associa o socket à porta especificada
    if (bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1)
    {
        std::cerr << "Failed to bind socket to port " << port << "!" << std::endl;
        close(serverSocket);
        return -1;
    }

    if (listen(serverSocket, 5) == -1) // O número 5 define o tamanho da fila de conexões pendentes
    {
        std::cerr << "Failed to listen on port " << port << "!" << std::endl;
        close(serverSocket);
        return -1;
    }

    std::cout << "Server started on port " << port << std::endl;

    while (true)
    {
        sockaddr_in clientAddr;                   // etrutura para armazenar o endereço do cliente
        socklen_t clientLen = sizeof(clientAddr); // tamanho da estrutura do cliente
        int clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &clientLen);
        if (clientSocket == -1) // verifica se a conexão foi aceita com sucesso
        {
            std::cerr << "Failed to accept connection!" << std::endl;
            continue; // continua para a próxima iteração do loop
        }

        std::cout << "Accepted connection from client!" << std::endl;

        std::thread clientThread(handleClient, clientSocket);
        clientThread.detach(); // thread  executada independentemente
    }

    close(serverSocket);
    return 0;
}