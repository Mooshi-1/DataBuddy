import itertools

def main():
    available = ['RA', 'RB', 'RC', 'RD', 'RE']
    itertools.product(available, 1)
    

    test = itertools.product('ABCD', repeat = 2)
    print(test)


if __name__ == '__main__':
    main()