from collections import Counter, defaultdict, deque
from functools import reduce
from heapq import heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded


def solve(snailnums):
    def parse(snailnum):
        stack = []
        pair = []

        for c in snailnum:
            if c == '[':
                stack.append(pair)
                pair = []
            elif c == ']':
                pair2 = stack.pop()
                stack.append(pair) 
                pair = pair2
            elif c == ',':
                pair = [stack.pop()]
            else:
                stack.append(int(c))

        return stack     

    def explode(snailnum):
        n = len(snailnum)
        brackets = 0

        for i, c in enumerate(snailnum):
            if c == '[':
                brackets += 1
            elif c == ']':
                brackets -= 1
            elif c.isdigit() and brackets > 4 and snailnum[i+1] == ',' and snailnum[i+2].isdigit():
                a = int(c)
                b = int(snailnum[i+2])
                leftat = -1
                rightat = -1

                for j in range(i-1, -1, -1):
                    if snailnum[j].isdigit() and (snailnum[j+1] == ',' or snailnum[j-1] == ','):
                        leftat = j
                        break

                for j in range(i+4, n):
                    if snailnum[j].isdigit() and (snailnum[j+1] == ',' or snailnum[j-1] == ','):
                        rightat = j
                        break

                leftest = snailnum[:i-1]

                if leftat > -1:
                    leftval = int(snailnum[leftat]) + a
                    leftest = snailnum[:leftat] + str(leftval) + snailnum[leftat+1:i-1]

                middle = '0'

                rightest = snailnum[i+4:]

                if rightat > -1:
                    rightval = int(snailnum[rightat]) + b
                    rightest = snailnum[i+4:rightat] + str(rightval) + snailnum[rightat+1:]

                return (True, leftest + middle + rightest)

        return (False, snailnum)                

    def split(snailnum):
        n = len(snailnum)

        for i, c in enumerate(snailnum[:-1]):
            if c.isdigit() and snailnum[i+1].isdigit():
                val = int(snailnum[i:i+2])
                a = val//2
                b = val-a
                return (True, snailnum[:i] + f'[{a},{b}]' + snailnum[i+2:])

        return (False, snailnum)

    def calc(snailnum):
        while True:
            exploded, snailnum = explode(snailnum)
            didsplit, snailnum = split(snailnum)

            if not exploded and not didsplit:
                break

        return snailnum

    def add(a, b):
        return f'[{a},{b}]'

    val = calc(add(snailnums[0], snailnums[1]))

    for snailnum in snailnums[2:]:
        val = calc(add(val, snailnum))

    return val

    return sum(calc(num) for num in snailnums)


def main():
    lines = []

    with open('18.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
