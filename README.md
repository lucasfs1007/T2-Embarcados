# Trabalho 2 (2023-2)

Trabalho 2 da disciplina de Fundamentos de Sistemas Embarcados (2023/2)

## 1. Aluno

**Nome**: Lucas Felipe Soares

**Matrícula**: 202016767

**Semestre**: 2023.2

## 2. Vídeo

O vídeo a seguir trata-se de uma breve apresentação sobre a arquitetura do projeto e como algumas lógicas e soluções foram pensadas: 

[Link do vídeo](https://youtu.be/zeUXjW5pre0)

## 3. Atividades UART

A seguir veremos uma base da execução das atividades anteriores ao trabalho 2. 

### Atividade 1:

Na execução da atividade 1 a seguir, veremos o programa enviando o número 12 que deixei pré-definido e retornando o dobro como configurado. 

Na imagem abaixo, veremos o print do envio de um inteiro...no caso selecionei o número 12:

![imagem do codigo](/Imagens/enviaInteiro.png)

Na imagem abaixo, vemos a confrmação da conexão sendo estabelecida e o envio do dobro do valor que passei. Aparentemente é a configuração da placa por padrão na data que foi testada:

![imagem do terminal](/Imagens/terminal2Ex1.png)

Na imagem abaixo, vemos a execução dos comandos dentro da live:

![imagem da live](/Imagens/terminalEx1.png)

Na imagem abaixo, vemos a execução recebendo String e Float

![Imagem terminal float e string](/Imagens/recebeFloat.png)

### Atividade 2:

Na imagem abaixo, veremos o print de execução da atividade 2. A atividade 2 corresponde a uma evolução da atividade 1, com a adaptação de envio das mensagens para o protocolo MODBUS. Na imagem a seguir veremos a execução do terminal de tal atividade:

![imagem terminal atividade 2](/Imagens/atividade2.png)

Já nas imagens a seguir, veremos trechos de códigos mais pertinentes...quanto a leitura da mensagem,definição da tabela e a função de cálculo de erros (CRC)

![codigo 1 atividade 2](/Imagens/atividade2Code1.png)

![codigo 2 atividade 2](/Imagens/atividade2Code2.png)

![codigo 3 atividade 2](/Imagens/atividade2Code3.png)

## 4. Como rodar o projeto:

**Pré-Requisito**: <br>
**Python3** <br>
**bmp280**: Necessário a instalação dessa biblioteca para pegar a temperatura ambiente do elevador. Na Rasp40, por exemplo não consegui utiliza-la, mas na rasp47 (onde demonstrarei com o print mais abaixo) consegui.

### 1° passo: Conectar-se a placa.

É necessário que se utilize o comando de SSH para se conectar na placa, é importante que seja que possua a possibilidade de se utilizar a biblioteca do bmp280, como por exemplo: ```164.41.98.29``` para a placa 7. O comando a ser executado no terminal é: ```ssh <usuario>@<ip-raspberry-pi> -p 13508```

### 2° passo: enviar os arquivos para a placa.

É necessário que se utilize o comando de SCP para enviar os arquivos do repositório para que eles sejam executados na placa. O comando para se executar no terminal é: ```scp -P 13508 -r ./diretorio <usuário>@<ipPlaca>:~/```

### 3° Passo - Executar os arquivos

Com os arquivos enviados para a placa é necessário em terminais diferentes executar esses quatro comandos, sendo o primeiro o de maior importância:

#### ```python3 elevador.py```

#### ```python3 serial.py```

#### ```python3 atividade1.py```

#### ```python3 atividade2.py```

obs: é necessário se conectar e enviar os arquivos em cada terminal.

### Passo alternativo

Caso não seja possível executar os arquivos é possível após a conexão com a placa se utilizar o comando: 
```nano elevador.py``` colar o conteúdo do arquivo elevador.py dentro do nano, salva-lo e executar utilizando: 
```python3 elevador.py``` e executa-lo. A ideia seria similar aos outros arquivos, conecta outros dois terminais e repete o processo com os respectivos arquivos.

## 5. Imagens da execução

Na imagem a seguir, veremos uma das primeiras execuções de quando foi executado o quesito 5, "**Leitura dos Registradores dos Botões**". Até esse dado momento não havia uma leitura do encode para saber a posição do elevador apenas a verificação se o botão foi pressionado ou não. Na imagem abaixo veremos a leitura dos botões em seu estado inicial:

### Leitura dos botões

![Leitura dos botões](/Imagens/leituraBotoes.png)

A seguir veremos o terminal após apertar os botões na dashboard e executarmos novamente:

![Leitura dos botões 2](/Imagens/leituraBotoes2.png)

### Leitura do encoder atividade

Na imagem abaixo, veremos um print da imagem na live da leitura do encoder estava configurada em 100 ms:

![Leitura encoder](/Imagens/leituraEncoder.png)

Já na imagem abaixo, quando utilizo o padrão de leitura dos comandos UART em 50 ms estabelicidos para o porjeto

![Leitura encoder 2](/Imagens/leituraEncoder2.png)

### Leitura da temperatura ambiente

Na imagem abaixo, veremos a lógica de implementação da obtenção da temperatura ambiente dentro do elevador. Para a isso, utilizei a lib da **bmp280** com a utilização de um código template que puxa a temperatura em graus celsius.

![codigo temperatura](/Imagens/temperaturaAmbienteCode.png)

Já na imagem abaixo, veremos esse print da imagem acima em execução com a temperatura aproximada de 26 graus. Ademais, já é possível ver os encoders referentes a essa placa nesse mesmo terminal. Esse tópico será tratado mais abaixo.

![terminal temperatura](/Imagens/terminalTemperatura.png)

Em alguns testes feitos depois, foi feita a passagem da temperatura via LCD para as dashboars. Na imagem abaixo, veremos o registro de 23.63 graus e nesse teste em específico meu terminal printava 23.10 graus, demonstrando uma pequena variação entre ambas mas ao meu ver pegando uma margem de erro aceitável em relação a temperatura.

![Temperatura Dashboard](/Imagens/temperaturaDashBoard.png)

## 6. Lógicas pertinentes:

### Configuração base dos pinos da GPIO

![pinos](/Imagens/configurcaoBasePinos.png)

### Leitura da posição dos andares utilizando encoder

Na imagem abaixo, veremos o funcionamento do terminal indentificando a posição dos andares da rasp 40. Esse valor possuiu algumas flutuações em variados testes e com isso utilizei uma média.

![leitura dos encoder](/Imagens/lendoPosicaoAndares.png)

### Frenagem do motor

Para poder ser feita a freagem do motor, primeiramente tive de buscar a posição do andar utilizando o encoder para saber quando devo diminuir a potencia para poder freiar o andar. Com isso peguei um intervalo arbitrário para melhor pegar a posição. Na imagem abaixo veremos um dos códigos que foi desenvolvido com essa lógica.

![Codigo freio](/Imagens/parandoMotorPrimeiroAndar.png)

Já na imagem abaixo, veremos a dashboard confirmando o elevador parado de fato no primeiro andar.

![Dashboard Freiada](/Imagens/freioPrimeiroAndar.png)

## 7. Lógicas criadas mas não testadas

Na lógica abaixo, criei uma estrutura para cada andar para verificar se foi solicitado um botão de chamada. Caso fosse chamado para um mesmo andar retonaria um print de erro, se fosse para outro deveria subir ou descer para o mesmo.

![Caso andar](/Imagens/logicaVaiParaAndar.png)

Já aqui, controlo a potência do motor para que ele faça esse deslocamento e o zero e freio no andar desejado.

![freio](/Imagens/parandoMotorPrimeiroAndar.png)