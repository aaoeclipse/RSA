import numpy as np
import random, sys, os

class RSA:
    """ RSA encrypts and decrypts """

    def __init__(self, primeNum=0):
        """  """
        if primeNum != 0:
            # First time you can create a file
            print('Generating file with primary numbers...')
            self.create_prime_file(1,primeNum)
            print('Created Succesfuly!')
            return

        self.prime = self.load_prime_numbers()
        # self.generate_keys()
        self.load_keys()
        self.decipher(self.cipher('abc'))
    
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
            if (num % 1000 == 0):
                print('Loading... {}%'.format(num/final * 100))
            prime = True
            for i in range(2,num):
                if (num%i==0):
                    prime = False
            if prime:
                primeNumbers = np.hstack((primeNumbers, [num]))
        if create:
            np.save('primeNum', primeNumbers)
        else:
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
        mssgEncrypted = np.array([])
        for letter in mssg:
            element = np.array([ord(letter) - 96])
            element = element ** self.publicKey[0] % self.publicKey[1]
            mssgEncrypted = np.hstack((mssgEncrypted, element))
        print(mssgEncrypted)
        return mssgEncrypted

    def decipher(self, cipher):
        """ test """
        for x in cipher:
            element = int((x ** self.privateKey[0]) % self.privateKey[1])
            print(chr(element+96), end='')

    def load_keys(self):
        self.privateKey = np.load('privateKey.npy')
        self.publicKey = np.load('publicKey.npy')
        print('private key: {}'.format(self.privateKey))
        print('public key: {}'.format(self.publicKey))

rsa = RSA()