import RPi.GPIO as GPIO
import threading
import time
import struct
import serial
import bmp280
import smbus2


# removendo os warnings
GPIO.setwarnings(False)

#configuracoes base de rota e porta
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5
   
)

def main():
    # threads
    thread1 = threading.Thread(target= tratamentoSensor)
    thread1.start()
    thread2 = threading.Thread(target=get_temp_ambiente)
    thread2.start()
    pid_configura_constantes(Kp_ = 30.0, Ki_ = 0.2, Kd_= 400.0)
    pid_atualiza_referencia(6000) #primeiro andar
    get_temp_ambiente()
    sobeElevador()
    enviaTemp(retornoConexao)
    enviaValorFloat(ser, command,matricula, value)
    #desceElevador()
    #freiaElevador()
    thread1.join()
    thread2.join()

# Inicialize a biblioteca GPIO e seus respectivos pinos
GPIO.setmode(GPIO.BCM)
DIR1 = 20
DIR2 = 21
POTM = 12
SENSORTERREO = 18
SENSORPRIMEIROANDAR = 23
SENSORSEGUNDOANDAR = 24
SENSORTERCEIROANDAR = 25

#saidas --> valores que podem mudar
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(POTM, GPIO.OUT)

# entradas - leitura
GPIO.setup(SENSORPRIMEIROANDAR, GPIO.IN) 
GPIO.setup(SENSORSEGUNDOANDAR, GPIO.IN)
GPIO.setup(SENSORTERCEIROANDAR, GPIO.IN)
GPIO.setup(SENSORTERREO, GPIO.IN)
GPIO.setup(SENSORTERCEIROANDAR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SENSORSEGUNDOANDAR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SENSORTERCEIROANDAR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SENSORTERREO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# configuracoes do motor
def desligado(DIR1, DIR2 ):
    GPIO.output(DIR1, GPIO.LOW) 
    GPIO.output(DIR2, GPIO.LOW)

def desce(DIR1, DIR2 ):
    GPIO.output(DIR1, GPIO.LOW) 
    GPIO.output(DIR2, GPIO.HIGH)

def sobe(DIR1, DIR2 ):
    GPIO.output(DIR1, GPIO.HIGH)
    GPIO.output(DIR2, GPIO.LOW)

def freio(DIR1, DIR2 ):
    GPIO.output(DIR1, GPIO.HIGH) 
    GPIO.output(DIR2, GPIO.HIGH)


    #variaveis dos botoes
    
    #terreo
BOTAOSUBIDAT = 0X00

# primeiro andar
BOTAODESCIDA1 = 0X01
BOTAOSUBIDA1 =  0X02

    #segundo andar
BOTAODESCIDA2 = 0X03
BOTAOSUBIDA2 = 0X04

    # terceiro andar
BOTAODESCIDA3 = 0X05

   # botao emergencia
BOTAOEMERGENCIA = 0X06 


#botoes internos elevador
BOTAOELEVADORT = 0X07
BOTAOELEVADOR1 = 0X08
BOTAOELEVADOR2 = 0X09 
BOTAOELEVADOR3 = 0X0A
  
    #Variaveis globais de sensores
SENSORATIVADOT = 0
SENSORATIVADO1 = 0
SENSORATIVADO2 = 0
SENSORATIVADO3 = 0

TIME = 0.001

    #variaveis relacionadas ao controle do elevador
retornoConexao = 0 # a mesma da atividaDE 1 E 2
valorPidControle = 1
potencia = 0

motor = GPIO.PWM(POTM, 1000) #  canal e Frequencia de 1KHZ
motor.start(0)

GPIO.add_event_detect(SENSORTERREO, GPIO.RISING)
GPIO.add_event_detect(SENSORPRIMEIROANDAR, GPIO.RISING)
GPIO.add_event_detect(SENSORSEGUNDOANDAR, GPIO.RISING)
GPIO.add_event_detect(SENSORTERCEIROANDAR, GPIO.RISING)



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

def solicitarValorEncoder():
    ser.flushInput()
    request = bytes([0x01, 0x23, 0xC1]) + bytes([6, 7, 6, 7])
    crc16 = calcular_crc(request)
    crcBytes = struct.pack('<H', crc16)
    requestCRC = request + crcBytes
    ser.write(requestCRC)
    response = ser.read(7)  # A resposta deve ter 7 bytes conforme a tabela
    valorEncoder = struct.unpack('<I', response[3:7])[0]  # Convertendo 4 bytes em int
    return valorEncoder

def tratamentoSensor():
    
    global SENSORTERREO
    global SENSORPRIMEIROANDAR
    global SENSORSEGUNDOANDAR
    global SENSORTERCEIROANDAR
   
    
    while True:
        if GPIO.event_detected(SENSORTERREO):
            print("terreo ativado")
            valorEncoder = solicitarValorEncoder()
            print(valorEncoder)
            
        elif GPIO.event_detected(SENSORPRIMEIROANDAR):
            print("primeiro andar ativado")
            valorEncoder = solicitarValorEncoder()
            print(valorEncoder)
            
        elif GPIO.event_detected(SENSORSEGUNDOANDAR):
            print("segundo andar ativado")
            valorEncoder = solicitarValorEncoder()
            print(valorEncoder)
            
        elif GPIO.event_detected(SENSORTERCEIROANDAR):
            print("terceiro andar ativado")
            valorEncoder = solicitarValorEncoder()
            print(valorEncoder)
            
        
        time.sleep(TIME)      

# Controle andares elevador
def controlaElevador():
   global potencia
   global motor
   encoderAtual = solicitarValorEncoder()
   potenciaNecessaria = pid_controle(encoderAtual)
   
   #vamos definir a potencia do elevador de acordo com sua posicao
   while True:
        encoderAtual = solicitarValorEncoder()
        if encoderAtual >= 6000 and encoderAtual <= 6055 : #freiando pro primeiro andar
            freiaElevador()
            motor.ChangeDutyCycle(0)
            print("devo parar aqui")
            break
        potenciaNecessaria = pid_controle(abs(encoderAtual))
        if potenciaNecessaria >= 0 and potenciaNecessaria <= 100:
            motor.ChangeDutyCycle(potenciaNecessaria)
        
        time.sleep(0.2)



def sobeElevador():
    sobe(DIR1, DIR2 )
    controlaElevador()

def desceElevador():
    desce(DIR1,DIR2)
    controlaElevador()
    
def freiaElevador():
    freio(DIR1,DIR2)
    controlaElevador()



# pid
saida_medida = 0.0
sinal_de_controle = 0.0
referencia = 0.0
Kp = 0.0  # Ganho Proporcional
Ki = 0.0  # Ganho Integral
Kd = 0.0  # Ganho Derivativo
T = 1.0  # Período de Amostragem (ms)
last_time = 0
erro_total = 0.0
erro_anterior = 0.0
sinal_de_controle_MAX = 100.0
sinal_de_controle_MIN = -100.0

def pid_configura_constantes(Kp_, Ki_, Kd_):
    global Kp, Ki, Kd
    Kp = Kp_
    Ki = Ki_
    Kd = Kd_

def pid_atualiza_referencia(referencia_):
    global referencia
    referencia = float(referencia_)

def pid_controle(saida_medida):
    global erro_total, erro_anterior, sinal_de_controle

    erro = referencia - saida_medida

    erro_total += erro  # Acumula o erro (Termo Integral)

    if erro_total >= sinal_de_controle_MAX:
        erro_total = sinal_de_controle_MAX
    elif erro_total <= sinal_de_controle_MIN:
        erro_total = sinal_de_controle_MIN

    delta_error = erro - erro_anterior  # Diferença entre os erros (Termo Derivativo)

    sinal_de_controle = Kp * erro + (Ki * T) * erro_total + (Kd / T) * delta_error  # PID calcula sinal de controle

    if sinal_de_controle >= sinal_de_controle_MAX:
        sinal_de_controle = sinal_de_controle_MAX
    elif sinal_de_controle <= sinal_de_controle_MIN:
        sinal_de_controle = sinal_de_controle_MIN

    erro_anterior = erro

    return sinal_de_controle

#essa funcao aparece no terminal
def get_temp_ambiente():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    # Inicializar o sensor BMP280
    sensor = bmp280.BMP280(i2c_dev=bus, i2c_addr=address)

    # Realizar a leitura da temperatura
    temperatura = sensor.get_temperature()

    return temperatura

print("Temperatura:")
print(get_temp_ambiente())

def enviaTemp(retornoConexao):
   formattedFloat = "{:.2f}".format(get_temp_ambiente())
   message = b'\x01'  + b'\x16' + b'\xD1'
   enviaValorFloat(retornoConexao, message,'6767',formattedFloat)
   
matricula = 6767

def enviaValorFloat(ser, command,matricula, value): 
    print(value)
    message = command + struct.pack('<f',float(value))+bytes([int(digit) for digit in matricula])
    valorCRC = calcular_crc(message)
    message += int(valorCRC).to_bytes(2, 'little')
    print(f'FLOAT ENVIADO: {message}')
    ser.write(message)

main()