# Yes, this is ugly, but as this ain't a beauty-contest, I want this be done quickly:
# At each level, we will add new letters. To be learned.
curriculum = [
    'asdf ',
    'jklö',
    'erui',
    'qwop',
    'ghtz',
    'cvnmb',
    'yx,.-',
    'äüß',
    '1234567890',
    'éèáàôê'
]
for k in range(len(curriculum)):
    curriculum[k] += curriculum[k].upper()
