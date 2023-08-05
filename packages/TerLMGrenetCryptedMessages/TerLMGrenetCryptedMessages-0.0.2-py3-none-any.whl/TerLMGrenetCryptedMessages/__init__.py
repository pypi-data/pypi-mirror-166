def CarVersNb(car):
    position={' ':0,'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,
    'R':18,'S':19,'T':20, 'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}
    return position[car]

def NbVersCar(nb):
    alphabet=' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet[nb]

def caractereDecale(c,n):
    nouvellePos= n+ CarVersNb(c)
    return NbVersCar(nouvellePos%27)

def codeMessage(text, n):
    codedMessage = ''
    for i in range(len(text)):
        codedMessage += caractereDecale(text[i], n)
    return codedMessage

def freqCaracter(car, text):
    """ count the apparition frequency of the caracter chain choosen
    >>> freqCaracter('p', 'apple')
    0.4
    >>> freqCaracter('a', 'cars')
    0.25
    """
    NbCar = 0
    for i in range(len(text)):
        if text[i] == car:
            NbCar += 1
    return NbCar/len(text)

def detailFreq(listeCar, text):
    """ list the frequency of all caracters given in text, give th result in an array
    >>> detailFreq('au', 'apiculteur')
    [('a', 0.1), ('u', 0.2)]
    """
    outTab = []
    for i in range(len(listeCar)):
        freq = freqCaracter(listeCar[i], text)
        outTab += [(listeCar[i], freq)]
    return outTab

def KeyCrack(text):
    """ give the most probable Cesar's keys and the most probable decoded messages for a coded message
    >>> KeyCrack('MHCVXLVCVXSHULHXU')
    [('JE SUIS SUPERIEUR', -3), ('WRMEGVEMEGBRDVRGD', -17), ('UPKCETCKCE PBTPEB', -19), ('FAWOQEOWOQLANEAQN', -7), ('XSNFHWFNFHCSEWSHE', -16)]
    """
    freqs = detailFreq(' ABCDEFGHIJKLMNOPQRSTUVWXYZ', text)

    max=0
    max2=0
    maxs=[]
    maxs2=[]
    for i in range(len(freqs)):
        if freqs[i][1]>max:
            max = freqs[i][1]
            maxs = [freqs[i]]
        elif freqs[i][1]==max:
            maxs += [freqs[i]]
        elif freqs[i][1]>max2:
            max2 = freqs[i][1]
            maxs2 = [freqs[i]]
        elif freqs[i][1]==max2:
            maxs2 += [freqs[i]]
    outMessages1 = []
    outMessages2 = []
    for i in range(len(maxs)):
        NbCar = CarVersNb(maxs[i][0])
        key = 5 - NbCar
        outMessages1 += [(codeMessage(text, key), key)]
    for i in range(len(maxs2)):
        NbCar = CarVersNb(maxs2[i][0])
        key = 5 - NbCar
        outMessages2 += [(codeMessage(text, key), key)]
    outMessages = outMessages1 + outMessages2
    return outMessages

def VigenereGrid(letterA, letterB):
    """ encrypt letters with vigener grid
    >>> VigenereGrid('C', 'F')
    'H'
    """
    grid = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'BCDEFGHIJKLMNOPQRSTUVWXYZA', 'CDEFGHIJKLMNOPQRSTUVWXYZAB', 'DEFGHIJKLMNOPQRSTUVWXYZABC',
    'EFGHIJKLMNOPQRSTUVWXYZABCD', 'FGHIJKLMNOPQRSTUVWXYZABCDE', 'GHIJKLMNOPQRSTUVWXYZABCDEF', 'HIJKLMNOPQRSTUVWXYZABCDEFG',
    'IJKLMNOPQRSTUVWXYZABCDEFGH', 'JKLMNOPQRSTUVWXYZABCDEFGHI', 'KLMNOPQRSTUVWXYZABCDEFGHIJ', 'LMNOPQRSTUVWXYZABCDEFGHIJK',
    'MNOPQRSTUVWXYZABCDEFGHIJKL', 'NOPQRSTUVWXYZABCDEFGHIJKLM', 'OPQRSTUVWXYZABCDEFGHIJKLMN', 'PQRSTUVWXYZABCDEFGHIJKLMNO',
    'QRSTUVWXYZABCDEFGHIJKLMNOP', 'RSTUVWXYZABCDEFGHIJKLMNOPQ', 'STUVWXYZABCDEFGHIJKLMNOPQR', 'TUVWXYZABCDEFGHIJKLMNOPQRS',
    'UVWXYZABCDEFGHIJKLMNOPQRST', 'VWXYZABCDEFGHIJKLMNOPQRSTU', 'WXYZABCDEFGHIJKLMNOPQRSTUV', 'XYZABCDEFGHIJKLMNOPQRSTUVW',
    'YZABCDEFGHIJKLMNOPQRSTUVWX', 'ZABCDEFGHIJKLMNOPQRSTUVWXY']
    encryptedLetter = grid[CarVersNb(letterA)-1][CarVersNb(letterB)-1]
    return encryptedLetter

def KeyText(word, key):
    """ replace all the letter of the word with key's letters
    >>> KeyText('MANETTE', 'PECHE')
    'PECHEPE'
    """
    keytext = ''
    for i in range(len(word)//len(key)):
        keytext += key
    for i in range(len(word)%len(key)):
        keytext += key[i]

    return keytext


def codeVigenere(word, key):
    """ encryption of a word with vigener cipher
    >>> codeVigenere('ANTICONSTITUTIONNELLEMENT', 'PORTE')
    'PBKBGDBJMMIIKBSCBVEPTAVGX'
    """
    plaintext = word.replace(" ", "")
    keytext = KeyText(plaintext, key)
    cryptedMessage = ''
    for i in range(len(plaintext)):
        cryptedMessage += VigenereGrid(plaintext[i], keytext[i])
    return cryptedMessage

def decodeVigenere(word, key):
    """ decryption of a word with vigener cipher
    >>> decodeVigenere('NPTFALPBMP', 'LIT')
    'CHAUSSETTE'
    """
    keytext = KeyText(word, key)
    uncryptedMessage = ''
    for i in range(len(word)):
        for j in range(26):
            if VigenereGrid(keytext[i], NbVersCar(j)) == word[i]:
                uncryptedMessage += NbVersCar(j)
    return uncryptedMessage
