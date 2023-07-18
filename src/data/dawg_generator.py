from dawg_graph import DAWG
import pickle


def generate_dawg_data_set():
    print("creating DAWG data set started")
    words_dawg = DAWG()

    with open("src/data/raw_data_source/slowa.txt") as file:
        while (line := file.readline().rstrip()):
            words_dawg.add_word(line)
        words_dawg.compress()

    with open("src/data/scrabble_words_complete.pickle", "wb") as file_handler:
        pickle.dump(words_dawg, file_handler)

    print("creating DAWG data set finished")
