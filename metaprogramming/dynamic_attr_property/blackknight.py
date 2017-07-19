class BlackKnight:
    def __init__(self):
        self.members = ['an arm', 'another arm',
                        'a leg', 'another leg']

        self.phrases = ["'Tis but a scratch.",
                        "It's just a flesh wound.",
                        "I'm invincible!",
                        "All right, we'll call it a draw."]

    @property
    def member(self):
        print('next member is:')
        return self.members[0]

    @member.deleter
    def member(self):
        '''This is just an annotation'''
        text = 'BLACK KNIGHT (loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))


if __name__ == '__main__':

    knight = BlackKnight()
    print(knight.member)

    del knight.member
    print(knight.member)

    del knight.member
    print(knight.member)

    del knight.member
    print(knight.member)

    del knight.member

    try:
        print(knight.member)
    except IndexError:
        print("There's no member left")
