class WordDoesNotExistError(Exception):
    def __init__(self, word):
        self.message = f"word {word} is not in dictionary"
        super().__init__(self.message)

