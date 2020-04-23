import csv
import argparse


def split_cols_csv(infile, no_files, outfile):
    """
    Split csv into several files using the no_files value. First column
    is consistent in each file.
    Args:
        infile: Input csv
        no_files: Number of files to output
        outfile: Output filename for each file. Starts at 1, ends at
            no_files

    """
    def find_length_lst(lst):
        """
        Split the length of columns into equal parts. Append to list.
        Append final item using length of columns, as the final split
        may be larger than the other splits.
        Args:
            lst: List

        Returns:
            List with split lengths
        """
        index = 1
        lst.append(index)
        num = int(no_files)
        length_col = no_cols // num
        for _ in range(num - 1):
            index += length_col
            lst.append(index)
        lst.append(no_cols)
        return lst

    def write_new_row(r, mode, lst):
        """
        Write new row to each split file
        Args:
            r: row as a list
            mode: Mode when opening file (either write or append)
            lst: List containing split lengths

        """
        for j in range(len(lst) - 1):
            with open(f'{outfile}{j + 1}.csv', mode, newline='',
                      encoding='utf-8-sig') as csv_outfile:
                csv_writer = csv.writer(csv_outfile,
                                        delimiter=',',
                                        quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(
                    [r[0]] + r[lst[j]:lst[j + 1]])

    length_lst = []
    check_row_length_lst = []
    with open(infile, 'r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for i, row in enumerate(csv_reader):
            if i == 0:
                no_cols = len(row)
                check_row_length_lst.append(no_cols)
                length_lst = find_length_lst(length_lst)
                write_new_row(row, 'w', length_lst)
            else:
                no_cols = len(row)
                check_row_length_lst.append(no_cols)
                write_new_row(row, 'a', length_lst)

    print(f'Minimum items per row: {min(check_row_length_lst)}')
    print(f'Maximum iters per row: {max(check_row_length_lst)}')

    with open('check_row_length.txt', 'w') as f:
        for item in check_row_length_lst:
            f.write("%s\n" % item)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Split csv file into a number of files')
    parser.add_argument('infile', help='Input csv')
    parser.add_argument('no_files', help='Number of files for output split')
    parser.add_argument('outfile',
                        help='Output filename. Starts from <outfile>1.csv to'
                             '<outfile><no_files>.csv')

    args = parser.parse_args()
    split_cols_csv(args.infile, args.no_files, args.outfile)
