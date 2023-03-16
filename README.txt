En el código de play.py se utiliza una librería creada por Agustín Ávila Quiroga para la serialización y deserialización de datos en formatos predefinidos, lo que permite una transferencia de datos más eficiente y una reducción en la cantidad de datos si es necesario.

TENER CUENTA:

Es importante tener en cuenta que, en esta versión, la deserialización no funciona correctamente para datos que no tienen tamaños de 8, 16 o 32 bits completos. Esto se resolverá en futuras versiones, ya que la actual puede presentar errores en tamaños entre 8 y 16 bits o entre 16 y 32 bits.
En el archivo "play.py" se tiene la opción de abrir un archivo JSON o cualquier otro archivo que contenga los datos necesarios. Esto es algo que se podría considerar para una versión no beta.

*Datos y formatos desarrollados:

data = {"PTemp": 25, "BattVolt.value": 12.3, "WaterLevel": 200}
format = [
    {"tag": "PTemp", "type": "i", "len": 32},
    {"tag": "BattVolt.value", "type": "f", "len": 32},
    {"tag": "WaterLevel", "type": "i", "len": 32}
]

*Archivo donde "play.py" en donde se utiliza estos datos y formato tiene el siguiente código:

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


*Ejemplo desarrollado en consola:

>>>python -m play

 Datos a serializar:  {'PTemp': 25, 'BattVolt.value': 12.3, 'WaterLevel': 200}
 Datos en buffer en bits:  bitarray('000000000000000000000000000110010100000101000100110011001100110100000000000000000000000011001000')
 Datos en buffer en formato c/ byte:  bytearray(b'\x00\x00\x00\x19AD\xcc\xcd\x00\x00\x00\xc8')
____________________________
PTemp
____________________________
BattVolt.value
____________________________
WaterLevel
Datos Deserializados:  {'PTemp': 25, 'BattVolt.value': 12.300000190734863, 'WaterLevel': 200}
