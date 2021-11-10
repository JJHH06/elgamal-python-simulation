from random import randrange
#k: cantidad de primos a generar
def fermatRandomPrime( k,min, max ,iteraciones = 25):
    result = []
    while(k >0):
        prime = randrange(min,max+1)
        
        if is_prime(prime, k=iteraciones):
            result.append(prime)
            k -=1   
    return result


def is_prime(n, k = 25):
    if n ==2 or n ==1: return False
    for i in range(k):
        a = randrange(2, n)
        if pow(a,(n-1),n) != 1%n:
            return False
    return True

def save(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()

def read(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    return data 
