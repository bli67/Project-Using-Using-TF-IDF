import argparse
import json
import math


def idf(word, d):
    count = 0
    for pony in d.keys():
        if word in d[pony].keys():
            count += 1
    return math.log(6/count)

def f_n(d, num):
    if num > len(d):
        return []
    d1 = []
    for k in d.keys():
        if num > 0:
            d1.append(k)
            num -= 1
        else:
            break
    return d1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store', dest='data')
    parser.add_argument('-n', action='store', dest='num')
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        d = json.load(f)
        f.close()

    d1 = {}
    for pony in d.keys():
        d1[pony] = {}
        for word in d[pony].keys():
            tf = d[pony][word]
            tf_idf = tf * idf(word, d)
            d1[pony][word] = tf_idf
    d = d1
    for pony in d.keys():
        d[pony] = dict(sorted(d[pony].items(), key=lambda item: item[1], reverse=True))
        d[pony] = f_n(d[pony], int(args.num))
    print(json.dumps(d, indent=4))


if __name__ == '__main__':
    main()
