import struct
import time
import serial


PORT = '/dev/serial0'
BAUDRATE= 9600 #no dois vai ser 15200
TIMEOUT = 0.5


def main():
    retornoConexao = conexao()
    enviaInteiro(retornoConexao)
    enviaFloat(retornoConexao) 
    enviaString(retornoConexao)   
    #solicitaInteiro(retornoConexao)


def conexao():
    uarto_filestream = serial.Serial(port=PORT,baudrate=BAUDRATE,timeout=TIMEOUT)
    if uarto_filestream.isOpen():
        print("conexao incializada")
    else:
        print("Erro na conexão")
    return uarto_filestream

#solicitacoes

def solicitaInteiro(retornoConexao):
    message = 0xA1 
    send_command(retornoConexao, message, '6767')
    read_response(retornoConexao, response_type=0xA1, )
    
def solicitaFloat(retorno_conexao):
    message = 0xA2
    send_command(retorno_conexao, message, '1480')
    read_response(retorno_conexao, response_type=0xA2 )

def solicitaString(retorno_conexao):
    message = 0xA3
    send_command(retorno_conexao, message, '1480')
    read_response(retorno_conexao, response_type=0xA3 )

#envios

def send_command(ser, command, matricula): 
    message = bytes([command] + [int(digit) for digit in matricula]) 
    ser.write(message) 

def send_commandValueInteiro(ser, command,value,  matricula): 
    message = bytes([command] )+ struct.pack('>i',value)+bytes([int(digit) for digit in matricula]) 
    ser.write(message) 

def send_commandValueFloat(ser, command,value,  matricula): 
    message = bytes([command] )+ struct.pack('>f',value)+bytes([int(digit) for digit in matricula]) 
    ser.write(message) 

def send_commandValueString(ser, command, text, matricula):
    message = bytes([command, len(text)]) + bytes(text, 'utf-8') + bytes([int(digit) for digit in matricula])
    ser.write(message)
       
# Função para ler e imprimir resposta 
def read_response(ser, response_type): 
    if response_type == 0xA1:  # Solicitação de dado inteiro (integer) 
        data = ser.read(4) 
        integer_value = struct.unpack('>i', data)[0] 
        print(f"Valor inteiro recebido: {integer_value}")
    elif response_type == 0xB1:
        data = ser.read(4) 
        integer_value = struct.unpack('>i', data)[0] 
        print(f"Valor inteiro recebido: {integer_value}")
    if response_type == 0xA2:  # Solicitação de dado float  
        data = ser.read(4) 
        float_value = struct.unpack('>f', data)[0] 
        print(f"Valor float recebido: {float_value}")
    elif response_type == 0xB2:
        data = ser.read(4) 
        float_value = struct.unpack('>f', data)[0] 
        print(f"Valor float recebido: {float_value}")
    if response_type == 0xA3:  # Solicitação de string
        length = ser.read(1)[0]
        data = ser.read(length)
        received_string = data.decode('utf-8')
        print(f"String recebida: {received_string}")
    elif response_type == 0xB3:  
        length = ser.read(1)[0]
        data = ser.read(length)
        received_string = data.decode('utf-8')
        print(f"String recebida: {received_string}") 
             
def enviaInteiro(retornoConexao):
    valor = 12
    message = 0xB1
    send_commandValueInteiro(retornoConexao, message,valor, '6767')
    read_response(retornoConexao, response_type=0xB1, )
    
def enviaFloat(retornoConexao):
    valor = 12.5
    message = 0xB2
    send_commandValueFloat(retornoConexao, message,valor, '6767')
    read_response(retornoConexao, response_type=0xB2 )

def enviaString(retornoConexao):
    valor = "lucas"
    message = 0xB3
    send_commandValueString(retornoConexao, message,valor, '6767')
    read_response(retornoConexao, response_type=0xB3 )
    
main()