from schema import Kin
from tables import name

Human = Kin(names=name['human'], ability=['Adaptive'])


def main():
    print(Human)
    for name, field in Human.__fields__.items():
        print(field)


if __name__ == '__main__':
    main()
