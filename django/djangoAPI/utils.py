'''Some General Utils'''


def num_to_alpha(num):
    '''
    Converts a number to its alpha base(26) implimentation
    Starts at 1 = a, 27 = aa
    '''
    lst = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    if num < 27:
        return lst[num - 1]
    return num_to_alpha(int(num/26)) + lst[(num % 26) - 1]


class Result():
    """Format of results that come from model class functions"""

    def __init__(self, success=False, message='', exception=None, error_code=0, obj_id=[], obj=[]):
        self.success = success
        self.message = message
        self.exception = exception
        self.obj_id = obj_id
        self.error_code = error_code
        self.obj = obj
