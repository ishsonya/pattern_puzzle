import itertools
import screen_parser
import time
def is_valid(row, pattern, starts):
    # TODO:
    psize = len(pattern)
    for idx in range(1, psize):
        if starts[idx] - (starts[idx - 1] + pattern[idx - 1] + 1) < 0:
            return False
    if starts[-1] + pattern[-1] > len(row):
        return False

    next_row = [0 for _ in row]
    for start, ln in zip(starts, pattern):
        for x in range(ln):
            next_row[start + x] = 1
    for o, n in zip(row, next_row):
        if o != -1 and o != n:
            return False
    return True

def design(idx___color, pattern):
    intersection = None
    n = len(idx___color)
    i = 0
    for starts in itertools.combinations(range(n), len(pattern)):
        i += 1
        if i % 100000 == 0:
            print('designing patterns', i)
        # print(starts, pattern)
        if is_valid(idx___color, pattern, starts):
            curr = [0 for _ in range(n)]
            for start, ln in zip(starts, pattern):
                for x in range(ln):
                    curr[start + x] = 1
            if intersection is None:
                intersection = [x for x in curr]
                # print(intersection)
            else:
                for i in range(n):
                    if intersection[i] != curr[i]:
                        intersection[i] = -1
    if intersection is None:
        print(idx___color)
        print(pattern)
        raise Exception('No valid combination')
    print('patterns partly designed')
    return intersection




def solve(n, col___pattern, row___pattern):
    # imitating my behaviour
    row__col___color = [[-1 for _ in range(n)] for x in range(n)]
    i = 0
    while True:
        # print(i)
        # print(*row__col___color, sep='\n')
        i += 1
        if i % 500 == 0:
            print('working on it ', i)
        was_modified = False
        for idx in range(n):
            # print(idx)
            # row
            old_row = row__col___color[idx]
            new_row = design(old_row, row___pattern[idx])
            if any(x[0]!=x[1] for x in zip(new_row, old_row)):
                was_modified = True
                row__col___color[idx] = new_row
            # col
            old_col = [row__col___color[x][idx] for x in range(n)]
            new_col = design(old_col, col___pattern[idx])
            if any(x[0] != x[1] for x in zip(new_col, old_col)):
                was_modified = True
                for c in range(n):
                    row__col___color[c][idx] = new_col[c]
        if not was_modified:
            break
    print("ANS")
    print(*row__col___color, sep='\n')
    return row__col___color

def parse_input():
    n = int(input())
    col___pattern = []
    row___pattern = []
    for _ in range(n):
        pattern = [int(x) for x in input().split()]
        col___pattern.append(pattern)
    for _ in range(n):
        pattern = [int(x) for x in input().split()]
        row___pattern.append(pattern)
    return n, col___pattern, row___pattern

def autosolve():
    t = time.time()
    n, cols, rows, top_left, size = screen_parser.get_rows__cols()
    t1 = time.time() - t
    t = time.time()
    ans = solve(n, cols, rows)
    t2 = time.time() - t
    print('Parsing input took: {} seconds'.format(t1))
    print('Solving puzzle took: {} seconds'.format(t2))
    input('Are you ready for filling?')
    screen_parser.fill(n, top_left, size, ans)

if __name__ == '__main__':
    import pyautogui
    pyautogui.PAUSE = 0.05
    autosolve()
