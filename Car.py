#simple car class with member variables for name, orientation, head coordinates, and length. Hashable.
class Car:
        def __init__(self, start, char, orient, leng):
            self.char = char
            self.orient = orient
            self.start = start
            self.len = leng

        
        def print(self):
            print(
                'Name: ', self.char,
                '\nOrientation: ', self.orient,
                '\nStart: ', self.start,
                '\nLength: ', self.len
            )

        def sizeup(self):
            self.len += 1

        def __attrs(self):
            return(self.char, self.orient, tuple(self.start), self.len)

        def __eq__(self, other):
            return isinstance(other, Car) and self.__attrs() == other.__attrs()
        
        def __hash__(self):
            return hash(self.__attrs())
