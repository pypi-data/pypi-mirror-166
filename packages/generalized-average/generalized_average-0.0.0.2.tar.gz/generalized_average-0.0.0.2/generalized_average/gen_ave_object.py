from generalized_matth.matt_funct import  AVERAG_TYPE
from aenum import  extend_enum
import numpy as np


def extend_matt_enum():
    for name, value in (
            ('HARMONIC', 0),
            ('ARITHMETIC', 1),

    ):
        extend_enum(AVERAG_TYPE, name, value)
    return
class main_generalzied_object:
    def __init__(self,average_val):
        extend_matt_enum()
        if average_val==1:
            self.pair_mean = self.arithmetic_for_pairs
            self.array_mean =   self.arithmetic_for_array
        elif average_val == 0:
            self.pair_mean = self.harmonic_for_pairs
            self.array_mean = self.harmonic_for_array
        elif average_val == 2:
            self.pair_mean = self.geometric_for_pairs
            self.array_mean = self.geometric_for_array

        return

    def check_array_positivity(self,x):
        if np.min(x)<=0:
           return 0
        return 1

    def check_positivity(self, x):
        if x <= 0:
            return 0
        return 1

    def arithmetic_for_array(self,x):
        if self.check_array_positivity(x) :
            return np.mean(x)
        print ("Please provide positive data")
        return -1
    def arithmetic_for_pairs(self,x,y):
        if self.check_positivity(x) and self.check_positivity(y) :
            return 0.5*(x+y)
        print ("Please provide positive data")
        return -1
    def harmonic_for_array(self,x):
        if self.check_array_positivity(x) :
            ss =np.sum([1/i for i in x])
            return len(x)/ss
        print ("Please provide positive data")
        return -1
    def harmonic_for_pairs(self,x,y):
        if self.check_positivity(x) and self.check_positivity(y) :
            return 2*(x*y)/(x+y)
        print ("Please provide positive data")
        return -1
    def geometric_for_array(self,x):
        if self.check_array_positivity(x) :
            return np.exp(np.mean(np.log(x)))


        print ("Please provide positive data")
        return -1
    def geometric_for_pairs(self,x,y):
        if self.check_positivity(x) and self.check_positivity(y) :
            return np.sqrt(x * y)
        print ("Please provide positive data")
        return -1

if __name__ =='__main__':
    bb= main_generalzied_object(2)
    x= np.array([1,2,3,4,5])

    print (bb.array_mean(x))
    print (bb.pair_mean(12,6))


