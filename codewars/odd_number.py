def find_it(seq):
    for i in seq:
        counted_seq = seq.count(i)
        if counted_seq % 2 != 0:
            return i


print(find_it([1,1,2,2,2,4]))
