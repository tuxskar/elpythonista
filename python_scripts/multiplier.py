def multiply(a, b):
    return float(a) * float(b)


def main():
    a = input('Inserte un número: ')
    b = input('Inserte otro número: ')
    res = multiply(a, b)
    print(f'La multiplicación es {res}')


if __name__ == '__main__':
    main()
