
def main(sequence):
    final = []
    for item in sequence:
        if ' A_' in item or ' B_' in item:
            delimiter = ' A_' if ' A_' in item else ' B_'
            parts = item.rsplit(delimiter)
            number = parts[0][4:] + "_RI" + delimiter.strip('_')
            vial = parts[1]
            filename = parts[0] + "_RI" + delimiter + vial
            final.append((number, int(vial), filename))
    print(final)


if __name__ == '__main__':
    sequence = [
            '006_25-0342_IVBGT B_4',
            '007_25-0343_AOBBRT B_5',
            '045_25-0364_GLCNTR_X10 B_40',
            '101_25-0364_PSILCNTR_X10 A_85'
      ]
    main(sequence)