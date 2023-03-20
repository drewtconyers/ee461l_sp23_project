def encrypt(input_text, N, D):
    valid = valid_input(input_text, N, D)
    if not valid:
        return "invalid input"
    reverse = input_text[::-1]
    shiftedstring = ''
    for i in range(len(reverse)):
        shiftedstring += shift(reverse[i], N, D)
    return shiftedstring


def decrypt(input_text, N, D):
    valid = valid_input(input_text, N, D)
    if not valid:
        return "encrypted password not valid"
    D *= -1
    reverse = input_text[::-1]
    decryptedstring = ''
    for i in range(len(reverse)):
        decryptedstring += shift(reverse[i], N, D)
    return decryptedstring


def shift(char, N, D):
    asc = ord(char)
    if D == 1:
        i = 0
        while i < N:
            if asc == 126:
                asc = 34
                i += 1
            else:
                asc += 1
                i += 1
    elif D == -1:
        i = 0
        while i < N:
            if asc == 34:
                asc = 126
                i += 1
            else:
                asc -= 1
                i += 1
    char = chr(asc)
    return char


def valid_input(input_text, N, D):
    if '!' in input_text:
        return False
    elif ' ' in input_text:
        return False
    elif N < 1:
        return False
    elif D != 1 and D != -1:
        return False
    else:
        return True


def read_database():
    with open('database.txt', 'r') as f:
        list = []
        for line in f:
            item = line.strip().split(" ")
            list.append(item)
        return list



