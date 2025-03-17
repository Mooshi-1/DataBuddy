def main():
    tuple_test = []
    tuple_test.append((100, 200, 300))
    
    if 200 == tuple_test[-1][1]:
        print(True)

    tuple_test.pop()
    print(tuple_test)


if __name__ == '__main__':
    main()