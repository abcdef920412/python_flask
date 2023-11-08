from socket import *
serverPort = 9000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    
    numbers_list = []
    i = 0
    errorFlag = 0
    for num_str in sentence.split():
        try:
            num_int = int(num_str)
        except ValueError:
            errorFlag = 1
            break
        numbers_list.append(num_int)
        i = i + 1
        if(i > 2):
            errorFlag = 1
            break
    
    if(i != 2):
        errorFlag = 1
    
    if(errorFlag):
        Sentence = 'Plaese input two integers'
    else:
        Sentence = str(numbers_list[0] + numbers_list[1])
    connectionSocket.send(Sentence.encode())
    connectionSocket.close()
    