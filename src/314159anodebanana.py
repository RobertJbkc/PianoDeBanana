import serial
from time import sleep
import re
import keyboard
from collections import deque
import numpy as np


def rodar(mapa_teclas, porta: str, baudrate: int = 9600, timeout=None, n_media: int = 5, limiar: float = 4000):

    esp32 = serial.Serial(port=porta, baudrate=baudrate, timeout=timeout)

    sleep(0.5)
    print(f'[ESP32]: Conectando na porta {porta}...')
    sleep(2.5) # Tempo para garanti que a conxão foi aberta
    print(f'-- ESP32 conectada na porta {porta}. Canal Serial aberto --')

    buffers = [
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media),
            deque(maxlen=n_media)
    ]

    em_pressao = {}


    while len(buffers[-1]) != n_media:
        # saida = esp32.readline().decode('utf-8').rstrip().split(sep=',')
        saida = esp32.readline().decode('utf-8').rstrip()
        padrao = r'(T\d+):\s*(\d+)'
        matches = re.findall(padrao, saida)
        saida = [i[1] for i in matches]

        # saida = [i[4:] for i in saida]
        # saida.pop(-1)
        for i, j in enumerate(saida):
            buffers[i].append(float(j))
    
    print('[PC]: Completando o buffer de dados...')
    sleep(0.5)
    print('[PC]: Buffer de dados completo.')

    contador = 0
    while True:
        # saida = esp32.readline().decode('utf-8').rstrip().split(sep=',')
        saida = esp32.readline().decode('utf-8').rstrip()
        padrao = r'(T\d+):\s*(\d+)'
        matches = re.findall(padrao, saida)


        saida = [i[1] for i in matches]
        # saida.pop(-1)
        for i, j in enumerate(saida):
            buffers[i].append(float(j))

        if contador // n_media == 1:
            medias = []
            for i in buffers:
                media = np.array(i).mean()
                medias.append(media)

            print([float(i) for i in medias]) ### Remover depois

            precionar_estas_teclas = []
            for posicao, valor in enumerate(medias):    
                if valor < limiar:
                    precionar_estas_teclas.append(mapa_teclas[posicao]) ### Pode ser uma lista ordenada
                    em_pressao[posicao] = True

                else:
                    em_pressao[posicao] = False
                    keyboard.release(mapa_teclas[posicao])
            
            for tecla in precionar_estas_teclas:
                print('[PC]: vou precionar estas:', precionar_estas_teclas)
                keyboard.press(tecla)
            precionar_estas_teclas = []

            contador = 0
        contador += 1

if __name__ == '__main__':
    mapa = ['t', '6', 'y', '7', 'u', 'i']
    rodar(mapa, 'COM16', baudrate=9600, n_media=5, limiar=4000)