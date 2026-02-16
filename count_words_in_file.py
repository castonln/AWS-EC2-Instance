import os

def count_words_in_file(root):
    count = 0

    try:
        # Only works for the filepath given in the lab.
        filepath = os.path.join(root, 'Limerick.txt')
        with open(filepath, 'r') as f:
            data = f.read()
            words = data.split()
            count += len(words)
        return count
    except:
        return None
