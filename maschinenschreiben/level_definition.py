# Yes, this is ugly, but as this ain't a beauty-contest, I want this be done quickly:
# At each level, we will add new letters. To be learned.
curriculum = [
    'asdf',
    'jklö',
    'erui',
    'qwop',
    'ghtz',
    'cvnmb',
    'yx,.-',
    'äü',
    '1234567890',
]
for k in range(len(curriculum)):
    curriculum[k] += curriculum[k].upper()


# Based on the list above, we construct the dictionary which contains the letters eligible per level:
eligible_letters_per_level = [
    ''.join(
        sorted(set(''.join(
            curriculum[0:k + 1])
        ))
    ) for k in range(len(curriculum))
]


# Some quick-and-dirty-tests:
if __name__ == '__main__':
    print(curriculum)
    print(eligible_letters_per_level)
