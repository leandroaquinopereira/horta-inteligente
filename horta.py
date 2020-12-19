import paho.mqtt.client as mqtt
from sensores import Sensores
import time
from datetime import datetime

import json

def criandoJson(info):
    return json.dumps(info)

broker = "test.mosquitto.org" 
topic = "inatel/ICT/horta-inteligente" 


cliente = mqtt.Client("Cliente")
cliente.connect(broker)

sensorUmidade = Sensores(name="Umidade", bounds=(0, 1)) #trabalhado em % (considerando status atual)
sensorLuminosidade = Sensores(name="Luminosidade", bounds=(0.5, 1)) #trabalhado em % (considerando últimas 12 horas e 100% como ideal)
carteiraDigital = 311.86

while True:

    info = {"dataHora": datetime.now().strftime("%d/%m/%Y\n\n%H:%M:%S"),
            "valorUmidade": sensorUmidade.getValor(),
            "valorIluminacao": sensorLuminosidade.getValor()}

    #Irrigação    
    info["statusIrrigacao"] = 1 if info["valorUmidade"] < 0.50 else 0
    info["mensagemStatus"] = "Ativado" if info["statusIrrigacao"] == 1 else "Desativado"

    #Carteira Digital para Irrigação
    carteiraDigital = carteiraDigital - 1 if info["statusIrrigacao"] == 1 else carteiraDigital
    info["saldoCarteira"] = str(carteiraDigital)

    #Iluminação
    info["statusLuz"] = 1 if info["valorIluminacao"] < 0.75 else 0
    info["mensagemLuz"] = "Ativado" if info["statusLuz"] == 1 else "Desativado"

    #Carteira Digital para Iluminação
    carteiraDigital = carteiraDigital - 1.50 if info["statusLuz"] == 1 else carteiraDigital
    info["saldoCarteira"] = str(carteiraDigital)

    arquivo = criandoJson(info) #preparando para envio MQTT

    cliente.publish(topic=topic, payload=arquivo)
    print(arquivo) #visualizando info Json enviado

    time.sleep(15)

