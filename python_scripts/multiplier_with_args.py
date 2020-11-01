import argparse


def multiply(a, b):
    return float(a) * float(b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('multiplicando', type=float, help='Número multiplicando')
    parser.add_argument('multiplicador', type=float, help='Número multiplicador')
    args = parser.parse_args()
    res = multiply(args.multiplicando, args.multiplicador)
    print(f'El resultado de la multiplicación es: {res}')
