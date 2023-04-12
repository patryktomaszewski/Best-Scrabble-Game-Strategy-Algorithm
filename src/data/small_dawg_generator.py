from dawg_graph import DAWG
import pickle


words_dawg = DAWG()
i = 0
with open("./raw_data_source/slowa.txt") as file:
    while (line := file.readline().rstrip()):
        if i % 10 == 0:
            words_dawg.add_word(line)
        i += 1

with open("./scrabble_words_small.pickle", "wb") as file_handler:
    pickle.dump(words_dawg, file_handler)