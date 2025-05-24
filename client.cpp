#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

int main(int argc, char *argv[])
{
    // parametros recebidos
    if (argc != 3)
    {
        std::cerr << "Usage: " << argv[0] << " <screenName> <serverIP>" << std::endl;
        return -1;
    }

    std::string screenName = argv[1];
    std::string serverIP = argv[2];
    int port = 4444;

    // criação do socket
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == -1)
    {
        std::cerr << "Failed to create socket!" << std::endl;
        return -1;
    }

    // configuração do endereço do servidor
    sockaddr_in serverAddr;
    std::memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);

    // converte o IP do servidor para o formato binário
    if (inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr) <= 0)
    {
        std::cerr << "Invalid server IP address!" << std::endl;
        close(clientSocket);
        return -1;
    }

    // conecta ao servidor
    if (connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1)
    {
        std::cerr << "Failed to connect to server!" << std::endl;
        close(clientSocket);
        return -1;
    }

    std::cout << "Connected to " << serverIP << " on port " << port << std::endl;

    // loop para enviar e receber mensagens
    std::string message;
    char buffer[1024];
    while (true)
    {
        std::cout << "Enter message: ";
        std::getline(std::cin, message);

        if (message == "exit")
        {
            std::cout << "Closing connection..." << std::endl;
            break;
        }

        // envia a mensagem para o servidor
        std::string formattedMessage = "[" + screenName + "]: " + message;
        if (send(clientSocket, formattedMessage.c_str(), formattedMessage.size(), 0) == -1)
        {
            std::cerr << "Failed to send message!" << std::endl;
            break;
        }

        // recebe a resposta do servidor
        std::memset(buffer, 0, sizeof(buffer));
        ssize_t bytesRead = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
        if (bytesRead > 0)
        {
            std::cout << "Server: " << buffer << std::endl;
        }
        else
        {
            std::cerr << "Failed to receive response or connection closed by server!" << std::endl;
            break;
        }
    }

    // fecha o socket
    close(clientSocket);
    return 0;
}