def add_if_missing(element, list):
    """
    Appends an item to a list if it does not exist in the list already
    """
    if not element in list:
        list.append(element)
    return list

def minmax(n1, n2):
    """
    Helper function which returns the min and max of two numbers with one call
    """
    smaller = min(n1, n2)
    larger = max(n1, n2)
    return smaller, larger

def sort_tuples_x(list):
    """
    Sorts a lists of tuples by the value of their first index
    """
    list.sort(key = lambda x: x[0])
    return list

def sort_tuples_y(list):
    """
    Sorts a lists of tuples by the value of their second index
    """
    list.sort(key = lambda x: x[1])
    return list

def floor(n):
    return int(n//1)

def lookup(k, ls):
    """
    Python implementation of the Haskell lookup funcion.
    ls is a list of (key, value) tuples. Given a key k,
    this will return the associated value. If multiple entries exist,
    lookup will return the first one in the list
    """
    for i in ls:
        if i[0] == k:
            return i[1]
    return None

class MutableBool:
    def __init__(self, value):
        self.value = value
