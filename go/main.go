package main

import (
	"fmt"
	"log"
	"net"
	"strings"
	"time"
)

func main() {
	listener, err := net.Listen("tcp", ":8000")
	if err != nil {
		log.Fatalf("Impossível ouvir! %v", err)
	}
	ticker := time.NewTicker(1 * time.Second)
	// go client()
	for ; ; <-ticker.C { // loop infinito
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Erro ao aceitar! %v", err)
			continue
		}
		go handleConn(conn)
	}
}

// func client() {
// 	conn, err := net.Dial("tcp", "localhost:8000")
// 	if err != nil {
// 		log.Fatalf("Impossível conectar! %v", err)
// 	}
// 	conn.Write([]byte("echo hello\n"))
// 	// defer conn.Close()
// }

func handleConn(conn net.Conn) {

	buffer := make([]byte, 1024) // cria um buffer (array de byte) de 1024 bytes

	for {
		n, err := conn.Read(buffer)
		if err != nil {
			log.Printf("Erro ao ler!\n%v\n", err)
			return
		}

		msg := strings.TrimSpace(string(buffer[:n])) // o string() serve pra printar o que recebeu, senao so veriamos varios numeros. O Trimspace é pra tirar \r e \n

		fmt.Printf("Recebi: %v\n", msg)

		msgSlice := strings.Split(msg, " ")

		if msgSlice[0] == "quit" {
			quit(conn)
		}
		if msgSlice[0] == "echo" {
			echo(conn, msgSlice[1:])
		}
	}
}

func quit(conn net.Conn) {
	fmt.Printf("Saindo!\n")
	conn.Close()
	return
}

func echo(conn net.Conn, msg []string) {
	// fmt.Printf("%v ", msg)
	conn.Write([]byte(strings.Join(msg, " ") + "\n"))
}
