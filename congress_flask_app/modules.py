import csv

def convert_to_dict(filename):
    datafile = open(filename, newline='')

    my_reader = csv.DictReader(datafile)

    list_of_dicts = []
    for row in my_reader:
        list_of_dicts.append( dict(row) )

    datafile.close()
    
    return list_of_dicts


def make_ordinal(num):
    base = num % 10
    if base in [0,4,5,6,7,8,9] or num in [11,12,13]:
        ext = "th"
    elif base == 1:
        ext = "st"
    elif base == 2:
        ext = "nd"
    else:
        ext = "rd"
    return str(num) + ext



if __name__ == '__main__':
    test_make_ordinal()
    presidents_list = convert_to_dict("presidents.csv")
    search_the_list(presidents_list)
    print(make_ordinal(12))
    print(make_ordinal(32))
