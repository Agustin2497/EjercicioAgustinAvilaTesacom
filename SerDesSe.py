""""------------------------------------------------------------------------
-- ToDo
-- v0.1.0 | Agustin | Primera versión
--
------------------------------------------------------------------------ """
from dataclasses import field
import struct
from bitarray import bitarray


"""------------------------------------------------------------------------
-- ToDo
-- v0.1.0 | Agustin | Primera versión
--
-- @param {*} buffer -> Trama a deserializar (cadena / bytes)
-- @param {*} format -> Diccionario / tabla de formato de serialización (ver notas adjuntas)
-- @return {*} diccionario / tabla "composición" (trama deserializada en campos tag = valor)
-- @version 0.1.0
------------------------------------------------------------------------"""

def decode(buffer, format):
    result = {}
    byteaux = bitarray()
    buf_aux = bitarray()
    #print("############ buffer ###############")
    #print(buffer)

    for field in format: 
        
        field_name = field["tag"]
        print("____________________________")
        print(field_name)
        field_type = field["type"]
        field_len = field["len"]
        #field_format = f">{field_len // 8}{field_type}"

        ###Seleccion de Bytes - por tipo de dato ###
        if field_type == "I":                                   # Para el formato h 16bit   

            if field_len < (8):                                 # Para el formato h con menosd de 8 bit
                buffer_struc = bytearray([0,0,0,0])
                # Traigo el primer byte por mas que no use todo
                primer_byte = buffer[0]
                # Lo convierte en una cadena binaria, elimina el prefijo '0b' y agrega ceros a la izquierda                         
                cadena_binaria = bin(primer_byte)[2:].zfill(8) 
                # Extrae los primeros 4 bits de la cadena binaria 
                bit_extraidos = cadena_binaria[:field_len]
                # Agrega 0 a la izquierda para completar el byte      
                bit_extraidos = bit_extraidos.zfill(8)
                # Agrega 0 al byte mas significativo          
                print((bit_extraidos))
                buffer_struc[0] = 0x00
                buffer_struc[1] = 0x00
                buffer_struc[2] = 0x00
                # Iterar sobre cada bit en bit_extraidos del buffer
                for i, bit in enumerate(bit_extraidos):
                    # Si el bit es 1, establecer el bit correspondiente en el nuevo bytearray
                    if bit == "1":
                        buffer_struc[3] |= 1 << (7 - i)
                           
                ## Armo formato
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)

                # Eliminar los bits más significativos de field_len del primer byte del buffer
                buffer[0] = buffer[0] & ((1 << X) - 1)

                # Desplazar los bits restantes field_len lugares hacia la izquierda
                for i in range(1, len(buffer)):
                    buffer[i-1] |= ((buffer[i] << field_len) ) & 0xFF
                    buffer[i] &= (((1 << field_len) - 1)) & 0xFF

                print("##################################################################")



            # Para el formato h con menosd de 16 bit
            if (field_len < 16) and (field_len > 8):  
                print("entre 8 y 16 bits no esta implementado")                               
                """                
                ent = 16 - field_len
                # Extraer primer byte
                primer_byte = buffer[0]
                # Extraer X bits más significativos del segundo byte
                mascara = (1 << ent) - 1
                X_bits = (buffer[1] & (mascara << (8 - ent))) >> (8 - ent)
                mascara2 = (1 << 8) - 1 
                # Combinar los dos valores extraídos en un solo entero | desplazo los bits al lugar menos significativo
                entero = (primer_byte << (16-field_len)) | (X_bits & mascara2)
                 
                # Crear un buffer de 16 bits inicializado a cero
                buffer_struc = bytearray([0, 0])
                # Almacenar los primeros 8 bits del entero resultante en el primer byte del buffer de 16 bits
                buffer_struc[0] = buffer[0]
                # Almacenar los últimos 8 bits del entero resultante en el segundo byte del buffer de 16 bits
                buffer_struc[1] = entero & 0xFF
                
                # Eliminar los bits más significativos de field_len del primer byte del buffer
                buffer[0] = buffer[0] & ((1 << (16 - field_len)) - 1)

                # Desplazar los bits restantes field_len lugares hacia la izquierda
                for i in range(1, len(buffer)):
                    if field_len > 8:
                        buffer[i-1] |= (buffer[i] << (field_len - 8)) & 0xFF
                        buffer[i] = (buffer[i] >> (8 - (field_len - 8))) & 0xFF
                    else:
                        buffer[i-1] |= (buffer[i] << field_len) & 0xFF
                        buffer[i] = (buffer[i] >> (8 - field_len)) & 0xFF"""

                print("##################################################################")

        
            if field_len == 16:
                # Crear un buffer de 16 bits inicializado a cero
                buffer_struc = bytearray([0, 0, 0, 0])
                # Almacenar los primeros 8 bits del entero resultante en el primer byte del buffer de 16 bits
                buffer_struc[0] = 0x00
                buffer_struc[1] = 0x00
                buffer_struc[2] = buffer[0]
                # Almacenar los últimos 8 bits del entero resultante en el segundo byte del buffer de 16 bits
                buffer_struc[3] = buffer[1]   
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)
                buffer = buffer[field_len//8:]
                print("##################################################################")

            if field_len == 8:
                # Crear un buffer de 16 bits inicializado a cero
                buffer_struc = bytearray([0, 0, 0, 0])
                # Completo los primeros 8 bits en 0
                buffer_struc[0] = 0x00
                buffer_struc[1] = 0x00
                buffer_struc[2] = 0x00
                # Almacenar los 8 bits del 1er byte del buffer
                buffer_struc[3] = buffer[0]
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)
                buffer = buffer[1:]  
                print("##################################################################")          
                 
        if field_type  == "i":

            if field_len == (8):
                bit_de_signo = buffer[0] & 0x80

                if bit_de_signo > 0: #Si es negativo
                    # Crear un buffer de 32 bits inicializado a cero
                    buffer_struc = bytearray([0, 0, 0, 0])
                    buffer_struc[0] = 0xFF
                    buffer_struc[1] = 0xFF
                    buffer_struc[2] = 0xFF
                    buffer_struc[3] = buffer[0]
                    field_format = f">{field_type}"
                    field_data = struct.unpack(field_format, buffer_struc)
                    buffer = buffer[1:]  
                else:
                    # Crear un buffer de 32 bits inicializado a cero
                    buffer_struc = bytearray([0, 0, 0, 0])
                    buffer_struc[0] = 0x00
                    buffer_struc[1] = 0x00
                    buffer_struc[2] = 0x00
                    buffer_struc[3] = buffer[0]
                    field_format = f">{field_type}"
                    field_data = struct.unpack(field_format, buffer_struc)
                    buffer = buffer[1:] 

        if field_len == (16):
            bit_de_signo = buffer[0] & 0x80

            if bit_de_signo > 0: #Si es negativo
                # Crear un buffer de 32 bits inicializado a cero
                buffer_struc = bytearray([0, 0, 0, 0])
                buffer_struc[0] = 0xFF
                buffer_struc[1] = 0xFF
                buffer_struc[2] = buffer[0]
                buffer_struc[3] = buffer[1]
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)
                buffer = buffer[2:]  
            else:
                # Crear un buffer de 32 bits inicializado a cero
                buffer_struc = bytearray([0, 0, 0, 0])
                buffer_struc[0] = 0x00
                buffer_struc[1] = 0x00
                buffer_struc[2] = buffer[0]
                buffer_struc[3] = buffer[1]
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)
                buffer = buffer[2:]   

        if field_len == (32):

            bit_de_signo = buffer[0] & 0x80

            if bit_de_signo > 0: #Si es negativo
                # Crear un buffer de 32 bits inicializado a cero
                buffer_struc = bytearray([0, 0, 0, 0])
                buffer_struc[0] = buffer[0]
                buffer_struc[1] = buffer[1]
                buffer_struc[2] = buffer[2]
                buffer_struc[3] = buffer[3]
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)
                buffer = buffer[4:]  
            else:
                # Crear un buffer de 32 bits inicializado a cero
                buffer_struc = bytearray([0, 0, 0, 0])
                buffer_struc[0] = buffer[0]
                buffer_struc[1] = buffer[1]
                buffer_struc[2] = buffer[2]
                buffer_struc[3] = buffer[3]
                field_format = f">{field_type}"
                field_data = struct.unpack(field_format, buffer_struc)
                buffer = buffer[4:]  

        if field_type  == "f":
            X = 4
            buffer_struc = bytearray([0, 0, 0, 0])
            buffer_struc[0] = buffer[0]
            buffer_struc[1] = buffer[1]
            buffer_struc[2] = buffer[2]
            buffer_struc[3] = buffer[3]


        #field_format = f">{field_type}"
        #field_data = struct.unpack(field_format, buffer_struc)
        result[field_name] = field_data[0]
        #buffer = buffer[field_len//8:]

    return result

"""------------------------------------------------------------------------
-- v0.1.0 | Agustin Avila | Primera versión
-- @param {*} src -> Diccionario / tabla a frasear (serializar)
-- @param {*} format -> Formato de serialización (ver notas adjuntas)
-- @return {*} buffer -> diccionario / tabla serializado/a (cadena / bytes)
"""


def encode(src, format):

    buffer = bitarray()

    for field_spec in format:
        field_data = src[field_spec['tag']]
        field_len = field_spec['len']

        if field_spec['type'] == 'i':
            buffer.frombytes(struct.pack('>i', field_data)[4-field_len//8:])
        elif field_spec['type'] == 'I':
            buffer.frombytes(struct.pack('>I', field_data)[4-field_len//8:])
        elif field_spec['type'] == 'f':
            buffer.frombytes(struct.pack('>f', field_data)[4-field_len//8:])
    return buffer

