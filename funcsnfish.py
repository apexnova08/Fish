def wordInString(word, string):
    if word == string or f" {word} " in string or string.startswith(f"{word} ") or string.endswith(f" {word}"):
        return True
    else: return False