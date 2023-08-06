import math
#useful tool for dex
class DexHelper:

    ################################################
    #   optimal trade volume
    ################################################
    #   This is a implement of optimal trade volume,
    #   please reffer to 
    #       https://arxiv.org/pdf/2105.02784.pdf  
    #   for more math detail,
    ################################################

    #uniswap swap fee
    r1=0.997
    r2=1

    #update swap fee based on the protocol
    def set_r1(self,_r1):
        self.r1=_r1

    def set_r2(self,_r2):
        self.r2=_r2

    #trianglular arbitrage optimal volume
    # arbitrage route 1->2->3->1
    # a12 is the token1 reserve volume in token pair 1-2
    def optimal_volume(self,_a12,_a21,_a23,_a32,_a31,_a13):
        a13_prime=self.get_a13_prime(_a12,_a21,_a23)
        a31_prime=self.get_a31_prime(_a21,_a32,_a23)
        a=self.get_a(a13_prime,_a31,a31_prime)
        a_prime=self.get_a_prime(_a13,a31_prime,_a31)
        denominator=(1+math.isqrt(self.r1*self.r2*a_prime*a-1)-a)
        return denominator/self.r1

    #combination arbitrage optimal volume TBD
    def optimal_volume(self):
        return

    def get_a(self,_a13_prime,_a31,_a31_prime):
        return _a13_prime*_a31/(_a31+self.r1*self.r2*_a31_prime)

    def get_a_prime(self,_a13,_a31_prime,_a31):
        return (self.r1*self.r2*_a13*_a31_prime)/(_a31+self.r1*self.r2*_a31_prime)
    
    def get_a13_prime(self,_a12,_a21,_a23):
        return _a12*_a23/(_a23+self.r1*self.r2*_a21)    
        
    def get_a31_prime(self,_a21,_a32,_a23):
        return self.r1*self.r2*_a21*_a32/(_a23+self.r1*self.r2*_a21)