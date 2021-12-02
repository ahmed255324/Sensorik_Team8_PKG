import math
import numpy
import sympy
from sympy.polys import subresultants_qq_zz
import math

S1, S2, S3, S4, X= sympy. symbols('S1, S2, S3, S4, X')
d12 = 142
d13 = 142**(0.5)
d14 = 142
d23 = 142
d24 = 142**(0.5)
d34 = 142 
p12 = 10*math.pi/180
p13 = 10*math.pi/180
p14 = 10*math.pi/180
p23 = 10*math.pi/180
p24 = 10*math.pi/180
p34 = 10*math.pi/180

f12 = S1**2 + S2**2 - 2*S1*S2*math.cos(p12) - d12**2
f13 = S1**2 + S3**2 - 2*S1*S3*math.cos(p13) - d13**2
f14 = S1**2 + S4**2 - 2*S1*S4*math.cos(p14) - d14**2
f23 = S2**2 + S3**2 - 2*S2*S3*math.cos(p23) - d23**2
f24 = S2**2 + S4**2 - 2*S2*S4*math.cos(p24) - d24**2
f34 = S3**2 + S4**2 - 2*S3*S4*math.cos(p34) - d34**2

matrix = subresultants_qq_zz.sylvester(f13, f23, S3)
g1 = subresultants_qq_zz.sylvester(f12, matrix.det(), S2)
g1 = g1.det()
print(g1)

matrix = subresultants_qq_zz.sylvester(f14, f24, S4)
g2 = subresultants_qq_zz.sylvester(f12, matrix.det(), S2)
g2 = g2.det()
print(g2)

matrix = subresultants_qq_zz.sylvester(f14, f34, S4)
g3 = subresultants_qq_zz.sylvester(f13, matrix.det(), S3)
g3 = g3.det()
print(g3)
