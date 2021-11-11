#Laboratorio 10, programa principal
# Simulación de cifrado ElGamal
# Jose Javier Hurtarte 19707
# Andrei Francisco Portales 19825
# Christian Pérez 19710


from keyUtils import fermatRandomPrime,randrange,save,read
from hashlib import sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
#generate class called Alice

P=fermatRandomPrime(1,10000,100000)[0]

def AES_encrypt(raw, key):
        raw = pad(raw.encode(),16)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

def AES_decrypt(enc, key):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:]), 16).decode()

class Alice:
    def __init__(self):
            self.p = P
            self.g = randrange(2,self.p-1) #se utiliza un valor menor a P-1 y mayor o igual a 2 para mayor seguridad
            self.a = randrange(2,self.p-1)
            while(self.a == self.g):
                self.a = randrange(2,self.p-1) #por si llega a ser igual a g, se genera un nuevo valor para no comprometer la seguridad
                #esto es una probabilidad bajisima de un minimo de 1/10,000 pero es correcto considerar el caso, ya que si no
                #podria existir alguna vez en donde si y se comparta la llave privada tambien por accidente
            self.calculateSharedKey()
            
    def calculateSharedKey(self):
        self.A = pow(self.g,self.a,self.p)

    def decrypt(self,B, cipherText):
        C = pow(B,self.a,self.p)
        raw_key = str(B)+str(C)#la misma llave utilizada en la encripcion
        K = sha256(raw_key.encode()).digest()
        # TODO: decrypt the message using AES with CBC mode and the key K
        return AES_decrypt(cipherText,K)


# create class Bob
class Bob:
    def __init__(self, g, A):
        self.p = P
        self.g = g
        self.A = A
        self.b = randrange(2,self.p-1)
        self.calculateSharedKey()
        

    def calculateSharedKey(self):
        self.B = pow(self.g,self.b,self.p)
    
    def encrypt(self, message):
        C = pow(self.A,self.b,self.p)
        raw_key = str(self.B)+str(C)#La llave en si antes de colocarla en el hash
        K = sha256(raw_key.encode()).digest()
        return AES_encrypt(message, K)




# F por allison x2
#x3

opciones = """


Cifrado ElGamal:
1. Generar claves
2. Encriptar mensaje
3. Decriptar mensaje
4. Salir
"""
alice = Alice()
bob = Bob(alice.g, alice.A)

def menu():
    
    
    salida = True

    while salida:
        print(opciones)
        opcion = input('\nOpcion: ')
        
        if opcion == '1':
            alice = Alice()
            bob = Bob(alice.g, alice.A)
            input('\nClaves de Alice y Bob generadas, presione enter para continuar:\n')
            pass
        elif opcion == '2':
            encrypted = bob.encrypt(input('\nIngresa el texto que deseas cifrar: ')) #se pasa el mensaje para encriptar
            #las llaves de encripcion se pasaron en la inicialización de bob
            save('cypher_text.txt', encrypted.decode())
            print('\nEl mensaje cifrado es: ', encrypted.decode())
            print('\nTambien se guardo en un archivo llamado cypher_text.txt')
            input('\nPresiona enter para continuar:')
        elif opcion == '3':
            decrypt_option = ""
            while decrypt_option != '1' and decrypt_option != '2':
                print("""
            
¿Cómo deseas decifrar el mensaje?
1. mediante un archivo
2. mediante un input de texto en consola

            """)
                decrypt_option = input('\nOpcion: ')

            cypher_read = None
            if decrypt_option == '1':
                try:
                    cy_filename = input('\nIngresa el nombre y la extensión del archivo que contiene el mensaje cifrado: ')
                    cypher_read = read(cy_filename).encode()
                except:
                    cypher_read = None
                    print('\nNo se pudo encontrar el archivo',cy_filename)

            elif decrypt_option == '2':
                cypher_read = input('\nIngresa el texto que deseas descifrar: ').encode()

            if cypher_read != None:
                try:
                    decrypted = alice.decrypt(bob.B, cypher_read)
                    save('plain_text.txt', decrypted)
                    print('\nEl mensaje descifrado es: ',decrypted )
                    print('\nTambien se guardo el mensaje en un archivo llamado plain_text.txt')
                except:
                    print('\nHa habido un error en el formato del archivo y no se ha podido descifrar')
            input('\nPresiona enter para continuar:')
            
        elif opcion == '4':
            salida = False
            print('\nHasta la proximaaa...')


if __name__ == '__main__':
    menu()