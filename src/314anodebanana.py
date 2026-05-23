import serial
from time import sleep
import re
import keyboard
from collections import deque
import numpy as np


class ESP32():
    """Classe destinada ao controle e, principalmente, leitura da placa ESP32 via comunicação Serial"""
    def __init__(self, porta: str, baudrate: int = 9600, timeout=None, n_media: int = 5, limiar: float = 4000):
        self.porta = porta
        self.baudrate = baudrate
        self.timeout = timeout
        self.n_media = n_media
        self.limiar = limiar

        self.buffers = [
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media)
        ]

        self.em_pressao = {}

    def conectar(self):
        """Conecta o computador (Python) à placa ESP32 via conexão Serial"""

        self.esp32 = serial.Serial(port=self.porta, baudrate=self.baudrate, timeout=self.timeout)

        sleep(0.5)
        print(f'[ESP32]: Conectando na porta {self.porta}...')
        sleep(2.5) # Tempo para garanti que a conxão foi aberta
        print(f'-- ESP32 conectada na porta {self.porta}. Canal Serial aberto --')

    def deconectar(self):
        """Fecha a conexão entre a ESP32 e o computador (Python)"""

        if self.esp32:
            self.esp32.close()

    def completar_deque(self):
        """Função para preencher os buffers antes de começar a rodar o código"""

        while len(self.buffers[-1]) != self.n_media:
            saida = self.esp32.readline().decode('utf-8').rstrip().split(sep=',')
            saida = [i[4:] for i in saida]
            saida.pop(-1)
            for i, j in enumerate(saida):
                self.buffers[i].append(float(j))
        
        print('[PC]: Completando o buffer de dados...')
        sleep(0.5)
        print('[PC]: Buffer de dados completo.')

    def ler_serial(self):
        """Lê a saída Serial enviada pela placa ESP32. O método usado é o "read_line", que lê até um ""\n"""

        saida = self.esp32.readline().decode('utf-8').rstrip().split(sep=',')
        saida = [i[4:] for i in saida]
        saida.pop(-1)
        for i, j in enumerate(saida):
            self.buffers[i].append(float(j))

    # def media_movel(self):
    #     medias = []
    #     for i in enumerate(self.buffers):
    #         media = np.array(i).mean()
    #         medias.append(media)
    #         print([float(i) for i in medias]) ### Remover depois

    #     return medias        

    def usar_valores(self, mapa_teclas):
        """Realiza a média móvel com o buffer"""

        medias = []
        for i in self.buffers:
            media = np.array(i).mean()
            medias.append(media)

        print([float(i) for i in medias]) ### Remover depois

        # medias = self.media_movel()

        precionar_estas_teclas = []
        for posicao, valor in enumerate(medias):    
            if valor < self.limiar:
                precionar_estas_teclas.append(mapa_teclas[posicao]) ### Pode ser uma lista ordenada
                self.em_pressao[posicao] = True

            else:
                self.em_pressao[posicao] = False
                keyboard.release(mapa_teclas[posicao])
        
        for tecla in precionar_estas_teclas:
            print('[PC]: vou precionar estas:', precionar_estas_teclas)
            keyboard.press(tecla)
        precionar_estas_teclas = []

    def rodar(self, mapa):
        esp32.conectar()
        esp32.completar_deque()
        contador = 0
        while True:
            esp32.ler_serial()
            if contador // self.n_media == 1:
                esp32.usar_valores(mapa)
                contador = 0
            
            contador += 1


sequencia_brilha_brilha = {
    "T1": "u",
    "T2": "9", 
    "T3": "y",
    "T4": "6",
    "T5": "r", 
    "T6": "e"
}

sequencia_jogo = {
    "T1": "right",
    "T2": "up", 
    "T3": "left",
    "T4": "d",
    "T5": "w", 
    "T6": "a"
}

if __name__ == "__main__":

    mapa = ['t', '6', 'y', '7', 'u', 'i']

    esp32 = ESP32('COM16', baudrate=9600, timeout=None)
    esp32.rodar(mapa)

