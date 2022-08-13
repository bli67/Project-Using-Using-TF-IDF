import argparse
import json
import pandas as pd
import os.path as os


def count(stop_words, dia):
    d = {}
    for dialog in dia:
        trans_table = str.maketrans("()[],-.?!:;#&", '             ')
        dialog = dialog.translate(trans_table)
        words = dialog.split()
        for word in words:
            word = word.lower()
            if word not in stop_words and word.isalpha() and word != "":
                if word in d.keys():
                    d[word] += 1
                else:
                    d[word] = 1
    return d



def take_stopwords():
    stop_words = []
    p = os.abspath(__file__)
    temp = p.split(sep="\\")
    p = "\\".join(temp[:-2]) + "\hw8\data\stopwords.txt"
    with open(p, 'r') as f:
        content = f.readlines()
        for line in content:
            if line[0] != '#':
                stop_words.append(line.replace("\n", ""))
        f.close()
    return stop_words


def trim(df):
    pony_names = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    word_counts = {}
    stop_words = take_stopwords()
    for pony in pony_names:
        dialogs = list(df[df.pony.str.lower() == pony]['dialog'])
        word_counts[pony] = count(stop_words, dialogs)
    all_words = {}
    for pony in word_counts.keys():
        d = word_counts[pony]
        for word in d.keys():
            if word not in all_words.keys():
                all_words[word] = d[word]
            else:
                all_words[word] += d[word]
    for pony in word_counts.keys():
        temp = {}
        for word in word_counts[pony]:
            if all_words[word] >= 5:
                temp[word] = word_counts[pony][word]
        word_counts[pony] = temp
    return word_counts


def main():
    par = argparse.ArgumentParser()
    par.add_argument('-o', action='store', dest='output')
    par.add_argument('-d', action='store', dest='data')
    args = par.parse_args()

    with open(args.data, 'r') as f:
        df = pd.read_csv(f)
        f.close()

    word_counts = trim(df)

    with open(args.output, 'w') as f:
        json.dump(word_counts, f, indent=4)
        f.close()


if __name__ == '__main__':
    main()
