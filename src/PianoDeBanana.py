import serial
import time
import re
import keyboard

def read_esp32_data(sequencia, port="COM16", baudrate=9600, limiar=4000): 
    try:
        monitor_serial = serial.Serial(port, baudrate, timeout=1)
        print(f"Conectado à porta {port}")
        
        estado_teclas_anterior = {}
        teclas_pressionadas = {}

        # Inicializa o estado anterior das teclas como não pressionadas
        for tecla in sequencia:
            estado_teclas_anterior[tecla] = False

        while True:
            if monitor_serial.in_waiting > 0:
                line = monitor_serial.readline().decode('utf-8').strip()
                print(line)
                
                # Procura por padrões como "T1: 4095", "T2: 3500", etc.
                padrao = r'(T\d+):\s*(\d+)'
                matches = re.findall(padrao, line)
                
                if matches:
                    ser_pressionada = []
                    for tecla, valor_str in matches:
                        if tecla in sequencia:
                            valor = int(valor_str)
                            tecla_keyboard = sequencia[tecla]
                            pressionada_atual = valor < limiar
                            
                            # Verifica se o estado mudou
                            if pressionada_atual != estado_teclas_anterior[tecla]:
                                if pressionada_atual:
                                    ser_pressionada.append(tecla_keyboard)
                                    # Tecla foi pressionada (valor abaixo do limiar)
                                    teclas_pressionadas[tecla] = True
                                    # print(f"Tecla {tecla} ({tecla_keyboard}) PRESSIONADA - Valor: {valor}")
                                else:
                                    # Tecla foi solta (valor acima do limiar)
                                    keyboard.release(tecla_keyboard)
                                    if tecla in teclas_pressionadas:
                                        del teclas_pressionadas[tecla]
                                    # print(f"Tecla {tecla} ({tecla_keyboard}) SOLTA - Valor: {valor}")
                                
                                # Atualiza o estado anterior
                                estado_teclas_anterior[tecla] = pressionada_atual

                    keyboard.press(ser_pressionada)
            
    except serial.SerialException as e:
        print(f"Erro na comunicação serial: {e}")
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário")
        # Garante que todas as teclas sejam soltas ao sair
        for tecla in sequencia.values():
            keyboard.release(tecla)
    finally:
        # Garante que todas as teclas sejam soltas
        for tecla in sequencia.values():
            keyboard.release(tecla)


sequencia_guitar_hero = {
    "T1": "a",
    "T2": "s",
    "T3": "j",
    "T4": "k",
    "T5": "l"
}

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
    read_esp32_data(sequencia_brilha_brilha, port="COM16", limiar=4000)  # Altere para a porta do seu ESPuueu6r6u9
    # 666669666rrrrrrrr66ewwwddaaa6eeyy99uuu
