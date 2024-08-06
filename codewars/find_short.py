def find_short(s):
    length = len(s)
    print(length)
    word_counter = 0
    counter = 0
    word_len_list = []
    for i in range(length):
        word_len_list.append(i)
        if s[i] == " ":
            word_len_list.append(i)
            word_counter += 1

    print(word_len_list)
            


    words = f"words: {word_counter + 1}"

print(find_short("turns out random test cases are easier than writing out basic ones"))
