import csv

def clean(inputFile,OutputFile):
    newData = []
    with open(inputFile, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for data in spamreader:
            newData.append(data[1:])

    with open(OutputFile, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for data in newData:
            spamwriter.writerow(data)

if(__name__ == "__main__"):
    clean("data.csv","data_cleaned.csv")
