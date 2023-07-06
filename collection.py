class Collection:
    def __init__(self, list: list):
        self.list = list
        for i in range(0, len(list)):
            list[i].set_id(i)

    def get(self, i):
        return self.list[i]