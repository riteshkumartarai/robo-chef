# Generates modifications for recipes

import random
import util

# Randomly swap between 1-3 pairs of words
def index_swap(words):
    if len(words) < 4:
        return words
    num_to_swap = random.randint(1, 3)
    for i in range(num_to_swap):
        index1 = random.randint(0, len(words)-1)
        index2 = random.randint(0, len(words)-1)
        # Swap
        temp = words[index1]
        words[index1] = words[index2]
        words[index2] = temp
    return words

def random_word_swap(words, word_dict):
    if len(words) < 4:
        return words
    ind_to_swap = random.randint(0,len(words)-1)
    ind_to_choose = random.randint(0,len(word_dict)-1)
    words[ind_to_swap] = random.choice(list(word_dict))
    return words


# Removes a random chunk of the phrase.
def remove_chunk(words):
    if len(words) < 4:
        return words
    # Pick two random indices
    index1 = random.randint(0, len(words)-1)
    index2 = random.randint(0, len(words)-1)

    if (index1 < index2):
        start = index1
        end = index2
    else:
        start = index2
        end = index1

    new_phrase = words[0:start] + words[end:len(words)]
    return new_phrase


# Chooses a random chunk of phrase & moves it to the beginning or the end of the phrase
def distort_chunk(words):
    if len(words) < 4:
        return words
    # Pick two random indices
    index1 = random.randint(0, len(words)-1)
    index2 = random.randint(0, len(words)-1)

    if (index1 < index2):
        start = index1
        end = index2
    else:
        start = index2
        end = index1

    # Randomly choose to put at beginning or end
    location = bool(random.getrandbits(1))
    if (location==0):
        new_phrase = words[0:start] + words[end:len(words)]+ words[start:end]
    else:
        new_phrase = words[start:end] +words[0:start]+ words[end:len(words)]
    return new_phrase


# Writes the modified recipe out to text file
# Format: modified recipe, original phrase, phrase num
def write_modified_recipe(phrases, path, phrase_num, modified_phrase, removal):
    with open(path, 'a') as f:
        if not removal:
            f.write(str(phrase_num) + ' \t ')
        else:
            f.write(str(-phrase_num) + ' \t ')
        refinement = phrases[phrase_num-1]
        f.write(' '.join(refinement) + ' \t ')
        for i,phrase in enumerate(phrases):
            if (i == phrase_num-1):
                if (removal):
                    continue
                else:
                    f.write(' '.join(modified_phrase) + ' \t ')
            else:
                f.write(' '.join(phrase) + ' \t ')
        f.write(' \n ')

# Applies distortion rules and adds modified phrases to the modified phrases list
def add_to_modified_phrases(phrase, phrase_num, modified_phrases, word_dict):
    phrase_with_chunk_removed = remove_chunk(phrase)
    distorted_phrase = distort_chunk(phrase)
    phrase_with_swaps = index_swap(phrase)
    phrase_with_random_word = random_word_swap(phrase, word_dict)

    modifications = [phrase_with_chunk_removed, distorted_phrase, phrase_with_swaps, phrase_with_random_word]
    for m in modifications:
        modified_phrases.append((phrase_num, m))

    return modified_phrases

def generate(recipe, path, word_dict):
    max_phrase_len = 0
    modified_phrases = []
    phrases = []
    for phrase_num, phrase in enumerate(recipe):
        words = util.phrase2words(phrase)
        phrase_len = len(words)
        if phrase_len > max_phrase_len:
            max_phrase_len = phrase_len
        modified_phrases = add_to_modified_phrases(words, phrase_num+1, modified_phrases, word_dict)
        phrases.append(words)
    for phrase_i, mod in modified_phrases:
        write_modified_recipe(phrases, path, phrase_i, mod, False)
    for i,phrase in enumerate(phrases):
        write_modified_recipe(phrases, path, i+1, '', True)

    return len(recipe), max_phrase_len
