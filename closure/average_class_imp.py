class Average():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)

# Use python 3.x to run        
if __name__ == "__main__":
    avg = Average()
    print(avg(10))
    print(avg(11))
    print(avg(12))
