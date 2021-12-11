import cv2 
import math
import numpy as np
import sympy
from sympy import sqrt
from sympy.abc import x
from sympy.polys import subresultants_qq_zz

d12 = 142
d13 = 142**(0.5)
d14 = 142
d23 = 142
d24 = 142**(0.5)
d34 = 142 

def resultant(winkeln):
	S1, S2, S3, S4= sympy. symbols('S1, S2, S3, S4')

	f12 = S1**2 + S2**2 - 2*S1*S2*math.cos(winkeln[0][0]) - d12**2
	f13 = S1**2 + S3**2 - 2*S1*S3*math.cos(winkeln[0][1]) - d13**2
	f14 = S1**2 + S4**2 - 2*S1*S4*math.cos(winkeln[0][2]) - d14**2
	f23 = S2**2 + S3**2 - 2*S2*S3*math.cos(winkeln[0][3]) - d23**2
	f24 = S2**2 + S4**2 - 2*S2*S4*math.cos(winkeln[0][4]) - d24**2
	f34 = S3**2 + S4**2 - 2*S3*S4*math.cos(winkeln[0][5]) - d34**2

	matrix = subresultants_qq_zz.sylvester(f13, f23, S3)
	g1 = subresultants_qq_zz.sylvester(f12, matrix.det(), S2)
	g1 = g1.det()
	g1 = g1.subs(S1, sqrt(x))
	g1 = sympy.poly(g1)

	matrix = subresultants_qq_zz.sylvester(f14, f24, S4)
	g2 = subresultants_qq_zz.sylvester(f12, matrix.det(), S2)
	g2 = g2.det()
	g2 = g2.subs(S1, sqrt(x))
	g2 = sympy.poly(g2)

	matrix = subresultants_qq_zz.sylvester(f14, f34, S4)
	g3 = subresultants_qq_zz.sylvester(f13, matrix.det(), S3)
	g3 = g3.det()
	g3 = g3.subs(S1, sqrt(x))
	g3 = sympy.poly(g3)

	a1 = g1.all_coeffs()
	a1 = a1[::-1]
	a2 = g2.all_coeffs()
	a2 = a2[::-1]
	a3 = g3.all_coeffs()
	a3 = a3[::-1]
	A = np.array([a1, a2, a3], dtype='float')

	u, s, vh = np.linalg.svd(A, full_matrices=True)
	vh = np.transpose(vh)
	print(vh)
	v4 = vh[:, -2]
	v5 = vh[:, -1]

	v = cv2.solvePnP()
	
	
	table = [[4, 2, 3, 3],[4, 1, 3, 2],[4, 0, 3, 1],[4, 0, 2, 2],[3, 1, 2, 2],[3, 0, 2, 1],[2, 0, 1, 1]]
	B = np.zeros((7, 3))
	i = 0
	for zeil in table:
		B[i, 0] = v4[zeil[0]]*v4[zeil[1]]-v4[zeil[2]]*v4[zeil[3]]
		B[i, 1] = v4[zeil[0]]*v5[zeil[1]]+v5[zeil[0]]*v4[zeil[1]]-(v4[zeil[2]]*v5[zeil[3]]+v5[zeil[2]]*v4[zeil[3]])
		B[i, 2] = v5[zeil[0]]*v5[zeil[1]]-v5[zeil[2]]*v5[zeil[3]]
		i = i + 1
	u, s, vh = np.linalg.svd(B, full_matrices=True)
	vh = np.transpose(vh)
	v = vh[:, -1]
	lambda_roh = v[0]/v[1]
	roh = 1/(lambda_roh * v4[0] + v5[0])
	lambda_v = lambda_roh * roh
	t = lambda_v * v4 + roh * v5
	return sqrt((t[1]/t[2]))

def abstand_s(s1, cam_2_p):
	s = np.zeros((4,1), dtype=float)

