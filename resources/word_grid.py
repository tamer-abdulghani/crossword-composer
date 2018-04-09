import string
import random

OVER = [5, 0, 0, 0, 3, 0, 5, 5, 7, 11, 0, 0, 7, 0, 5, 5, 3, 5]
DOWN = [6, 11, 4, 6, 11, 4, 0, 0, 0, 0, 6, 6, 4, 4, 0, 0, 0, 0]

def make_grid(over_words, down_words):
    o = over_words
    d = down_words
    f = " "
    grid = " ".join(
        " " +
        o[0][:] + f + d[3][0] + f + o[4][:] + "\n" +
        d[0][1] + f + d[1][1] + f + o[6][:] + f + d[5][1] + "\n" +
        o[7][:] + f + d[3][2] + f + d[4][2] + f + d[5][2] + "\n" +
        d[0][3] + f + d[1][3] + f + o[8][:] + "\n" +
        d[0][4] + f + d[1][4] + f*3 + d[3][4] + f + d[4][4] + f*2 + "\n" +
        o[9][:] + "\n" +
        f*2 + d[1][6] + f + d[10][1] + f*3 + d[4][6] + f + d[11][1] + "\n" +
        o[12][:] + f + d[4][7] + f + d[11][2] + "\n" +
        d[12][1] + f + d[1][8] + f + d[10][3] + f + o[14][:] + "\n" +
        d[12][2] + f + o[15][:] + f + d[4][9] + f + d[11][4] + "\n" +
        o[16][:] + f + d[10][5] + f + o[17][:] + "\n")

    return grid[1:]


def rand_word(n):
    return "".join(random.choices(string.ascii_uppercase, k=n))


def random_words():
    over_words = [rand_word(n) for n in OVER]
    down_words = [rand_word(n) for n in DOWN]
    return over_words, down_words


def draw_random_example():
    over_words, down_words = random_words()
    print(make_grid(over_words, down_words))


if __name__=="__main__":
    draw_random_example()
