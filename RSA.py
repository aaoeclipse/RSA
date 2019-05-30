import numpy as np
import random, sys, os
import math as math
class RSA:
    """ RSA encrypts and decrypts """

    def __init__(self, primeNum=0, encrypt=False, decrypt=False, enc_and_decrypt=False, mssg=''):
        """  """
        
        if primeNum != 0:
            # First time you can create a file
            print('[*] Generating file with primary numbers...')
            self.prime = self.create_prime_file(1,primeNum)
            print('[+] Created Succesfuly!')
            print('[*] Generating keys...')
            self.generate_keys()
            return
        else:
            self.prime = self.load_prime_numbers()
            if encrypt:
                # self.generate_keys()
                self.load_keys()
                self.cipher(mssg)
            elif decrypt:
                self.load_keys()
                numMssg = []
                for ch in mssg.split(','):
                    numMssg.append(int(ch))
                self.decipher(numMssg)
            elif enc_and_decrypt:
                self.load_keys()
                self.decipher(self.cipher(mssg))

    def generate_keys(self):
        self.generate_N()
        self.publicKey = self.get_public_key()
        self.privateKey = self.get_private_key()
        self.save_keys()
    
    def load_prime_numbers(self):
        """ Loads prime numbers form text file """
        return np.load('primeNum.npy')

    def create_prime_file(self, init, final, create=True):
        """ gets prime numbers between params init and final """
        primeNumbers = np.array([])
        for num in range(init,final):
            if (num % 100 == 0):
                print('Loading... {}%'.format(num/final * 100))
            prime = True
            for i in range(2,num):
                if (num%i==0):
                    prime = False
            if prime:
                primeNumbers = np.hstack((primeNumbers, [num]))
        if create:
            np.save('primeNum', primeNumbers)
            print('Loading...100%!')
            return primeNumbers
        else:
            print('Loading...100%!')
            return primeNumbers

    def generate_N(self):
        """ Choses 2 random prime numbers and sets the multiple to N """
        while True:
            rp = random.randint(1,len(self.prime))
            rq = random.randint(1,len(self.prime))
            if rp != rq:
                break
                
        self.p = self.prime[rp]
        self.q = self.prime[rq]
        self.N = int(self.p * self.q)
        print('p: {}, q: {}, N: {}'.format(self.p,self.q,self.N))

    def get_public_key(self):
        """ Returns the public key (e, N) """
        self.phi = int((self.p - 1)*(self.q-1))
        
        while True:
            pos = random.randint(0,self.N%len(self.prime))
            self.e = int((self.prime[pos]))
            if self.e < self.phi:
                if self.is_coprime(self.e, self.N) == 1:
                    print('e: {}, phi: {}, N: {}'.format(self.e, self.phi, self.N))
                    break

        return np.array([self.e, self.N])
        
    def is_coprime(self, g, N):
        """ Check if g is coprime with g and N """
        while(N):
            g,N=N,g%N
        return g
        
    def get_private_key(self):
        """ Find d and get the private key """
        tmp = 0
        while True:
            tmp = tmp + 1
            if (tmp  * self.e ) % self.phi == 1:
                break
        self.d = tmp
        print('d: {} N: {}'.format(self.d, self.N))
        return np.array([self.d, self.N])

    def save_keys(self):
        """ Save both private and public key """
        np.save('publicKey', self.publicKey)
        np.save('privateKey', self.privateKey)

    def cipher(self, mssg):
        """ test """
        mssg = mssg.lower()
        if self.publicKey is None:
            print('[*] Please load the keys.')
            exit(0)
        mssgEncrypted = []
        for letter in mssg:
            element = (ord(letter) - 97)
            element = pow(element, self.publicKey[0].item(), self.publicKey[1].item())

            element = int(element) % self.publicKey[1]
            mssgEncrypted.append(int(element))
        print('Encrypted Message: ({})'.format(mssgEncrypted))
        return mssgEncrypted

    def decipher(self, cipher):
        """ test """
        num = []
        print('Decrypted Message: (', end='')
        for x in cipher:
            # result = (x ** self.privateKey[0]) % self.privateKey[1]
            element = pow(x, self.privateKey[0].item(), self.privateKey[1].item())
            num.append(element)
            print('{}'.format(chr(element + 97)), end='')
            # element = int((x ** self.privateKey[0]) % self.privateKey[1])
            # print(chr(element+96), end='')
        print(')')
        print('Decrypted Message in Numbers: {}'.format(num))



    def load_keys(self):
        self.privateKey = np.asarray(np.load('privateKey.npy'))
        self.publicKey = np.asarray(np.load('publicKey.npy'))
        print('private key: {}'.format(self.privateKey))
        print('public key: {}'.format(self.publicKey))
    
    

def help():
    print('')
    print('WELCOME to RSA Desipher')
    print('Instrucctions: ')
    print('-help: to show help menu')
    print('-keys [# of prime num to use]: generates the keys and save it on privateKey.npy and publicKey.npy')
    print('\t if [# of prime num to use] is left empty, uses 50 as default')
    print('=====================================')
    print('Keys must have been created from this point onwards')
    print('=====================================')
    print('-e [mssg]: encrypts message with keys created')
    print('-e "[mssg with many words]": encrypts message with keys created')
    print('-d [num separated by ,]: decrypt message with keys created')
    print('\t EXAMPLE:')
    print('\t 75, 84, 29, 29, 50')
    print('-de [mssg]: encrypts and decrypts given message')
    print('')

if len(sys.argv) == 1:
    help()
else:
    if sys.argv[1] == '-help':
        help()
    elif sys.argv[1] == '-keys':
        if len(sys.argv) == 3:
            num = sys.argv[2]
            if num.isnumeric():
                rsa = RSA(int(num))
        else:
            rsa = RSA(50)

    elif sys.argv[1] == '-e':
        if len(sys.argv) == 2:
            print('[-] No message! for more help use -h or -help')
            exit(0)
        mssg = sys.argv[2]
        if len(mssg) == 0:
            print('[-] No message! for more help use -h or -help')
        rsa = RSA(encrypt=True, mssg=mssg)
    elif sys.argv[1] == '-d':
        if len(sys.argv) == 2:
            print('[-] No message! for more help use -h or -help')
            exit(0)
        mssg = sys.argv[2]
        if len(sys.argv) > 3:
            for i in range(3,len(sys.argv)):
                mssg += sys.argv[i]
        rsa = RSA(decrypt=True, mssg=mssg)
    elif sys.argv[1] == '-de':
        if len(sys.argv) == 2:
            print('[-] No message! for more help use -h or -help')
            exit(0)
        mssg = sys.argv[2]
        rsa = RSA(enc_and_decrypt=True, mssg=mssg)
    else:
        help()