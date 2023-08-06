class R1(float):
    """
    The simplest example of a nontrivial metric space.
    It is simply the standard metric on the real line.
    It is primarily used for tests.
    """

    def dist(self, other):
        return abs(self - other)
