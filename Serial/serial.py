import serial
import struct
import time


#configuracoes base de rota e porta
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5
)

# limpando o buffer de entrada para evitar lixos de memória
ser.flushInput()  


#configuracoes dos pinos conforme a tabela 1
ENDERECOSBOTOES = {
    "Botão Terreo Sobe": 0x00,
    "Botão 1 And. Desce": 0x01,
    "Botão 1 And. Sobe": 0x02,
    "Botão 2 And. Desce": 0x03,
    "Botão 2 And. Sobe": 0x04,
    "Botão 3 And. Desce": 0x05,
    "Botão Elevador Emergência": 0x06,
    "Botão Elevador T": 0x07,
    "Botão Elevador 1": 0x08,
    "Botão Elevador 2": 0x09,
    "Botão Elevador 3": 0x0A
}

#calculo para deteccao de erros
def calcular_crc(commands):
    crc = 0 #variavel inicializada como 0 
    for command in commands:
        crc = CRC16(crc, command)
    return crc

def CRC16(crc, data):
    crc ^= data & 0xFF
    for _ in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ 0xA001
        else:
            crc >>= 1
    return crc

codigo = 0x03
subCodigo = 0x00
qtd = 11
EndEsp32 = 0x01
request = bytes([EndEsp32, codigo, subCodigo, qtd, 6, 7, 6, 7])

crc16 = calcular_crc(request)
crcBytes = int(crc16).to_bytes(2, byteorder = 'little')

requestCRC = request + crcBytes

ser.write(requestCRC)

response = ser.read(16)

print(f'Valor do botão terreo sobe é {response[2]}')
print(f'Valor do botão primeiro desce é {response[3]}')
print(f'Valor do botão primeiro sobe é {response[4]}')
print(f'Valor do botão segundo desce é {response[5]}')
print(f'Valor do botão segundo sobe é {response[6]}')
print(f'Valor do botão terceiro desce é {response[7]}')
print(f'Valor do botão painel elevador emergencia é {response[8]}')
print(f'Valor do botão painel elevador terreo é {response[9]}')
print(f'Valor do botão painel elevador 1 é {response[10]}')
print(f'Valor do botão painel elevador 2 é {response[11]}')
print(f'Valor do botão painel elevador 3 é {response[12]}')

# Função de solicitacao do valor do encoder
def solicitarValorEncoder():
    request = bytes([0x01, 0x23, 0xC1]) + bytes([6, 7, 6, 7])
    crc16 = calcular_crc(request)
    crcBytes = struct.pack('<H', crc16)
    requestCRC = request + crcBytes
    ser.write(requestCRC)
    response = ser.read(7)  # A resposta deve ter 7 bytes conforme a tabela
    valorEncoder = struct.unpack('<I', response[3:7])[0]  # Convertendo 4 bytes em int
    return valorEncoder



def enviaValorInteiro(ser, command,value,  matricula): 
    message = command + struct.pack('>i',value) + bytes([int(digit) for digit in matricula]) 
    crc = calculaCRC(message)
    message += int(crc).to_bytes(2, 'little')
    print(f'Mensagem enviada: {message}')
    ser.write(message) 

def leitura(ser, response_type): 
    
    # tratando o envio de inteiro e recebimento da resposta (inteiro de 4 bytes)
    
    if response_type == 0xB1:
        data = ser.read(4) 
        integer_value = struct.unpack('>i', data)[0] 
        print(f"Valor inteiro recebido: {integer_value}")
        
    elif response_type == 0x01+0x23+0xA1:  #Inteiro 
        data = ser.read(6) 
        integer_value = struct.unpack('>i', data)[0] 
        print(f"Valor inteiro recebido: {integer_value}")
        
def lerEnconder(retornoConexao):
    message = b'\x01'  + b'\x23' + b'\xC1'
    enviaValorInteiro(retornoConexao, message, '6767', None)
    return leitura(retornoConexao, response_type=0X00+0X16+0xC1)
   
print(solicitarValorEncoder())

   
def enviaPWM(retornoConexao):
    global potencia
    message = b'\x01'  + b'\x16' + b'\xC2'
    enviaValorInteiro(retornoConexao, message,'6767', potencia )