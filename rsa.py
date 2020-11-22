from random import randrange
from sympy import randprime, gcd
from functools import reduce

#Ke spuštění je potřeba Python >=3.9.0 (kvůli nové implementaci funkce pow(...))
#V souboru keys.txt najdete v tomto pořadí: Veřejný klíč, soukromý klíč a modulo
#V souboru source.txt najdete vstupní text pro šifrování, který se dá přepsat. Při kódování se počítá s použitím UTF-8
#Autor: Ondřej Chudáček,  221548, BPC2-IBE/02

#Převede šifrovaný int na string
def getText(integer):

    strg = ''

    #Převede vždy mocnimu 1 000 000 na příslušný UTF-8 znak
    while(integer > 0):
        strg = strg + chr(integer % 1000000)
        integer = integer // 1000000
    
    #Otočí řetězec
    return strg[::-1]


#Vygeneruje náhgodné číslo o n bitech
def generateAPrime(noBits = 512):
    return randprime(2 ** noBits, (2 ** (noBits+1)) - 1)

# Vytvoří (a vrátí) veřejný a soukromý klíč a modulo ve formátu pole.
def getKeys():
    isGCD = False
    print('Generování klíčů...')

    #Vytvoří dvě velká prvočísla o 1024 bitech
    factorPrimeOne = generateAPrime(1024)
    factorPrimeTwo = generateAPrime(1024)

    #Vynásobí prvočíla a spočítá eulerovu funkci pro tento součin
    #Násobek bude působit jako naše modulo při šifrování
    mod = factorPrimeOne*factorPrimeTwo
    euler = (factorPrimeOne - 1)*(factorPrimeTwo - 1)

    #Hledáme náhodný veřejný klíč o 2048 bitech, který není soudělný s eulerovou funkcí modula
    #Pokud je soudělný, vgenerujeme nový
    while(isGCD is False):
        pk = randrange(2 ** 2048, (2 ** 2049) - 1)
        if(gcd(euler, pk) == 1):
            isGCD = True

    #Vygenerujeme soukromý klíč, který je inverzním prvekem veřejného klíče při modulu euler
    sk = int(pow(pk, -1, euler))

    #Vrátíme hodnoty ve formátu pole. Pořadí je veřejný klíč, soukromý klíč a modulo
    return [pk, sk, mod]

#Zašifruje/dešifruje text v podobě int. Šifrování a dešifrování funguje stejně.
#Na vstupu je klíč (soukromý pro dešifrování a veřejný pro šifrování), zpráva ve fromátu int a modulo
#Výstupem je zašifrovaná zpráva ve formátu int
def encryptDecrypt(key, message, mod):
    return int(pow(message, key, mod))

def main():
    #Otevřeme a načteme soubor se zdrojovým textem
    with open('source.txt', 'r') as fr:
        readList = fr.read()
    
    #Vygenerujeme si sadu klíčů a modulo
    keys = getKeys()

    #Napíšeme do souboru pro případné další použití sadu parametrů pro další použití 
    with open('keys.txt', 'w') as fw:
        fw.write(str(keys[0]) + "\n\n" + str(keys[1]) + "\n\n" + str(keys[2]))

    #Zašifrujeme text. Nejdříve musíme vstupní text zakódovat a to pomocí převedení řetězce na pole int a následného sečtení mocnin (kompatibilní pro UTF-8).
    ciphertext = encryptDecrypt(keys[0], reduce(lambda acc, current: acc*1000000 + current, map(lambda letter: ord(letter), readList)), keys[2])

    #Vypíšme zašifrovaný text v podobě přirozeného čísla
    print('Šifrovaný text: ', ciphertext, '\n')

    #Dešifrujeme text
    decrypted = encryptDecrypt(keys[1], ciphertext, keys[2])

    #Dekóduejeme dešifrovaný text
    decodedText = getText(decrypted)

    #Vypíšme dekódvaný dešifrovaný text
    print('Dešifrovaný text: ', decodedText)


main()