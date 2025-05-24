CXX = g++
CXXFLAGS = -Wall -std=c++17
CLIENT_SRC = client.cpp
SERVER_SRC_MULTI = server-multi.cpp
SERVER_SRC_10 = server-multi10.cpp
CLIENT_BIN = client
SERVER_BIN = server
SERVER_BIN_10 = server10

all: $(CLIENT_BIN) $(SERVER_BIN) $(SERVER_BIN_10)

$(CLIENT_BIN): $(CLIENT_SRC)
	$(CXX) $(CXXFLAGS) -o $@ $<

$(SERVER_BIN): $(SERVER_SRC_MULTI)
	$(CXX) $(CXXFLAGS) -o $@ $<

$(SERVER_BIN_10): $(SERVER_SRC_10)
	$(CXX) $(CXXFLAGS) -o $@ $<

run-server-multithread: $(SERVER_BIN)
	./$(SERVER_BIN)

run-server-10threads: $(SERVER_BIN_10)
	./$(SERVER_BIN_10)

run-client: $(CLIENT_BIN)
	./$(CLIENT_BIN) $(ARGS)

clean:
	rm -f $(CLIENT_BIN) $(SERVER_BIN) $(SERVER_BIN_10)