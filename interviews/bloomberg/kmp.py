

def search(needle, highstack):
    needle_lpss = []

    for i in range(1, len(needle)+1):
        # max length of suffix of needle[:i] which is also postfix
        sub_needle = needle[:i]

        for j in range(len(sub_needle), -1, -1):
            if sub_needle[:j] == sub_needle[-j:]:
                needle_lpss.append(j)
                break
        else:
            needle_lpss.append(0)

    print(needle_lpss)

    return

    hs_offset = 0
    n_offset = 0
    while hs_offset <= (len(highstack) - len(needle)):
        if n_offset == len(needle):
            pass

        if needle[n_offset] == highstack[hs_offset + n_offset]:
            n_offset += 1
        else:
            pass


search("abxab", "xxxxxx")
