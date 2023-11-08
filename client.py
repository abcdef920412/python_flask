from socket import *
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((serverName,serverPort))
    sentence = input("Input two integers, separated by a space:")
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ("From Server:", modifiedSentence.decode())
    clientSocket.close()
except ConnectionRefusedError:
    print("An established connection was disconnected by the software on the hostcomputer")
