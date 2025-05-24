# Trabalho de Redes

**Alunos:** Leonardo Viera Silva, Luíza Machado Costa Nascimento, Pablo Henrique Silva de Faria

## Sobre o Trabalho

Este projeto consiste no desenvolvimento de duas versões multithread de um servidor, com foco em gerenciar múltiplas conexões de clientes de forma eficiente. O projeto foi implementado em **C++** e **Python**, com uma branch experimental em **Go**.

### Acesso ao Código em C++

## Para acessar o código em C++, vá para a pasta c++.

## Documentação C++

### Implementação em C++

#### Arquivos

- **server-multi.cpp**: Implementação de um servidor multithread onde cada conexão de cliente é gerenciada por uma nova thread.
- **server-multi10.cpp**: Implementação de um servidor com um pool fixo de 10 threads para gerenciar conexões de clientes.
- **client.cpp**: Implementação de um cliente que se conecta ao servidor e permite o envio e recebimento de mensagens.

---

### Como Compilar e Executar

#### Pré-requisitos

- **Compilador C++**: Certifique-se de ter o `g++` instalado.
- **Make**: Para facilitar a compilação e execução.

#### Comandos Disponíveis no Makefile

1. **Compilar os Executáveis**

Para compilar todos os arquivos do projeto, execute:

```bash
make
```

2. **Executar o Servidor Multithread**

Para rodar o servidor onde cada cliente é gerenciado por uma nova thread:

```bash
make run-server-multithread
```

3. **Executar o Servidor com 10 Threads**

Para rodar o servidor com um pool fixo de 10 threads:

```bash
make run-server-10threads
```

4. **Executar o Cliente**

Para rodar o cliente e se conectar ao servidor:

```bash
make run-client ARGS="<screenName> <serverIP>"
```

- Substitua `<screenName>` pelo nome do cliente, como `client1`.
- Substitua `<serverIP>` pelo endereço IP do servidor (ex.: `127.0.0.1`).

**Exemplo:**

```bash
make run-client ARGS="client1 127.0.0.1"
```

5. **Limpar os Executáveis**

Para remover os executáveis gerados:

```bash
make clean
```

---

### Funcionamento dos Servidores

#### **server-multi.cpp**

- Cada cliente que se conecta ao servidor é gerenciado por uma nova thread.
- As threads são destacadas (`detach`), permitindo que sejam executadas independentemente.

#### **server-multi10.cpp**

- Utiliza um pool fixo de 10 threads para gerenciar conexões.
- As conexões de clientes são enfileiradas e processadas pelas threads disponíveis.
- Caso todas as threads estejam ocupadas, novas conexões são rejeitadas com uma mensagem de "Servidor ocupado".

---

### Funcionamento do Cliente

- O cliente se conecta ao servidor especificado e permite o envio de mensagens.
- As mensagens são enviadas no formato `[screenName]: <mensagem>`.
- O cliente também recebe e exibe as respostas do servidor.
- Para encerrar a conexão, digite `exit`.

---

### Exemplo de Execução

1. **Iniciar o Servidor**

Em um terminal, inicie o servidor (exemplo com o servidor de 10 threads):

```bash
make run-server-10threads
```

2. **Iniciar o Cliente**

Em outro terminal, inicie o cliente:

```bash
make run-client ARGS="user1 127.0.0.1"
```

Digite mensagens no cliente e veja as respostas do servidor.

---

## Estrutura do Código

### Servidor (`server-multi10.cpp`)

- **handleClient**: Função que gerencia a comunicação com o cliente.
- **workerThread**: Função executada por cada thread do pool para processar conexões.
- **main**: Configura o servidor, cria o pool de threads e gerencia conexões de clientes.

### Cliente (`client.cpp`)

- **main**: Configura o cliente, conecta ao servidor e gerencia o envio/recebimento de mensagens.

---

## Observações

- Certifique-se de que a porta `4444` não esteja em uso antes de iniciar o servidor.
- Caso a porta esteja ocupada, você pode alterá-la no código-fonte, substituindo:

  ```cpp
  int port = 4444;
  ```

  Por outra porta, como:

  ```cpp
  int port = 5555;
  ```

---

## Documentação Python

### Implementação em Python
A implementação em Python se dividiu em duas: 
- implementacao_server_echo, a qual é um servidor echo, ou seja, que repete tudo que for enviado a ele - exceto o comando quit.
- implementacao_comando_echo, a qual é um servidor que implementa o COMANDO, ou seja, ao receber o comando `echo`, repete tudo o que vem após ele.

#### Arquivos

- **client.py**: Implementação de um cliente que se conecta ao servidor e permite o envio e recebimento de mensagens. Esse arquivo é comum para as implementações em Python deste repositório.
- **implementacao_server_echo/numero1.py**: Implementação de um servidor echo com um número variável de threads, sempre criando uma para cada nova conexão e destruindo-a quando a conexão é encerrada.
- **implementacao_server_echo/numero2.py**: Implementação de um servidor echo com número fixo de threads. Possui 10 threads e, quando elas são todas ocupadas, não aceita mais conexões até que alguma seja liberada.
- **implementacao_comando_echo/numero1.py**: Implementação de um servidor que possui o comando echo e com um número variável de threads, sempre criando uma para cada nova conexão e destruindo-a quando a conexão é encerrada.
- **implementacao_comando_echo/numero2.py**: Implementação de um servidor que possui o comando echo e com número fixo de threads. Possui 10 threads e, quando elas são todas ocupadas, não aceita mais conexões até que alguma seja liberada

### Como Executar

1. **Inicializar o servidor**
Para inicializar o servidor, use o comando a seguir, substituindo X por `server` ou `comando` e Y por `1` ou `2`. 
```
python3 implementacao_X_echo/numeroY.py 
```

2. **Inicializar o cliente**
Como o cliente é apenas um para ambas implementações em Python, basta executa-lo em outro terminal
```
python3 client.py
```

## Observações

- A porta que está sendo usada como padrão nessa implementação é a 1337. Certifique-se de que não há outro programa usando-a antes de inicializar o servidor.
- Se necessário, troque-a por outra, substituindo o trecho 
```PORTA = 1337``` 
no código do cliente e do servidor pela porta desejada