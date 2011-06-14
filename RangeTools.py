'''A Module containing utilities dealing with unusual ranges and functions for common modeling tasks.'''
def drange(start, stop, step):
    '''Returns a generator object'''
    # from: http://stackoverflow.com/questions/477486/python-decimal-range-step-value
    r = start
    while r < stop:
            yield r
            r += step
