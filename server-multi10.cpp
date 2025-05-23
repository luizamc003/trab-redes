#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <cstring>
#include <unistd.h>
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>

const int THREAD_POOL_SIZE = 10;

std::queue<int> clientQueue;
std::mutex queueMutex;
std::condition_variable queueCondition;

void handleClient(int clientSocket)
{
    char buffer[1024];
    std::memset(buffer, 0, sizeof(buffer));

    // lê dados do cliente
    while (true)
    {
        ssize_t bytesRead = read(clientSocket, buffer, sizeof(buffer) - 1);
        if (bytesRead <= 0)
        {
            break;
        }

        buffer[bytesRead] = '\0'; // tratando dados como string
        std::cout << "Received: " << buffer << std::endl;

        ssize_t bytesWritten = 0;
        while (bytesWritten < bytesRead)
        {
            ssize_t result = write(clientSocket, buffer + bytesWritten, bytesRead - bytesWritten);
            if (result <= 0)
            {
                break;
                bytesWritten += result;
            }
        }

        std::cout << "Closing connection with client" << std::endl;
        close(clientSocket);
    }
}

void workerThread()
{
    while (true)
    {
        int clientSocket;

        // aguarda por um cliente na fila
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            queueCondition.wait(lock, []
                                { return !clientQueue.empty(); });

            clientSocket = clientQueue.front();
            clientQueue.pop();
        }

        handleClient(clientSocket);
    }
}

int main()
{
    int port = 4444;

    //  socket
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == -1)
    {
        std::cerr << "Failed to create socket!" << std::endl;
        return -1;
    }

    // configuração do endereço do servidor
    // configurando servidor
    sockaddr_in serverAddr;
    std::memset(&serverAddr, 0, sizeof(serverAddr)); // inicializa a estrutura com zeros
    serverAddr.sin_family = AF_INET;                 // IPv4
    serverAddr.sin_addr.s_addr = INADDR_ANY;         // aeita conexões de qualquer endereço IP
    serverAddr.sin_port = htons(port);               // define a porta do servidor

    // associa o socket à porta
    if (bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1)
    {
        std::cerr << "Failed to bind socket to port " << port << "!" << std::endl;
        close(serverSocket);
        return -1;
    }

    if (listen(serverSocket, 5) == -1)
    {
        std::cerr << "Failed to listen on port " << port << "!" << std::endl;
        close(serverSocket);
        return -1;
    }

    std::cout << "Server started on port " << port << std::endl;

    // cria o pool de threads
    std::vector<std::thread> threadPool;
    for (int i = 0; i < THREAD_POOL_SIZE; ++i)
    {
        threadPool.emplace_back(workerThread);
    }

    while (true)
    {
        // cceita uma conexão de cliente
        sockaddr_in clientAddr;
        socklen_t clientLen = sizeof(clientAddr);
        int clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &clientLen);
        if (clientSocket == -1)
        {
            std::cerr << "Failed to accept connection!" << std::endl;
            continue;
        }

        std::cout << "Accepted connection from client!" << std::endl;

        // adiciona o cliente a fila ou retorna erro se a fila estiver cheia
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            if (clientQueue.size() >= THREAD_POOL_SIZE)
            {
                std::cerr << "All threads are busy. Rejecting client." << std::endl;
                const char *message = "Server is busy. Try again later.\n";
                write(clientSocket, message, strlen(message));
                close(clientSocket);
            }
            else
            {
                clientQueue.push(clientSocket);
                queueCondition.notify_one();
            }
        }
    }

    close(serverSocket);
    return 0;
}