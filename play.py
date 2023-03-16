import SerDesSe
from SerDesSe import decode, encode
import struct



######################## Formato y Buffer de prueba ####################

format1 = [
    {"tag": "PTemp", "type": "i", "len": 32},
    {"tag": "BattVolt.value", "type": "i", "len": 32},
    {"tag": "WaterLevel", "type": "I", "len": 8}
]
buffer3 = bytearray(b'\x00\x00\x00\x08\x00\x00\x00\x10\x01\x00\x00\x05')


################## Formato y datos utilizados de prueba #################

data = {"PTemp": 25, "BattVolt.value": 12.3, "WaterLevel": 200}
format = [
    {"tag": "PTemp", "type": "i", "len": 32},
    {"tag": "BattVolt.value", "type": "f", "len": 32},
    {"tag": "WaterLevel", "type": "i", "len": 32}
]

#########################################################################
#####################Ingresamos datos y el formato ######################
############################## Serializa ################################
buffer = encode(data, format)
print(" Datos a serializar: ",data)
print(" Datos en buffer en bits: ",buffer)

byte_buffer = bytearray(buffer.tobytes())
print(" Datos en buffer en formato c/ byte: ",byte_buffer )

#########################################################################
#####################Ingresamos datos y el formato ######################
############################## Deserializa ##############################
result = decode(byte_buffer,format)
print("Datos Deserializados: ",result)





