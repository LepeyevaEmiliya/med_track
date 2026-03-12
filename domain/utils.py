def paginate(items, page_size):
    idx = 0
    max_val = len(items)
    while idx < max_val:
        yield items[idx: idx + page_size]
        idx += page_size


class MeasurementHistory:
    def __init__(self, history_dct):
        self.history = sorted(history_dct.values(), key=lambda x: x[0])  # словарь организован след. образом: {0: (date, measure)}
        self.max_val = len(self.history)
        self.current = 0


    def __iter__(self):
        return self


    def __next__(self):
        if self.current >= self.max_val:
            raise StopIteration
        
        value = self.history[self.current]
        self.current += 1
        return value