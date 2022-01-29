import numpy as np
from sympy import reshape

imagePoints = np.zeros((4,2,1,))

points = np.ones((4,2))

a = 190

objectPoints = np.array([[-a/2, a/2, 0], [-a/2, -a/2, 0], [a/2, -a/2, 0], [a/2, a/2, 0]])
print(np.reshape(objectPoints, (4,3,1)))

imagePoints = np.reshape(points, (4,2,1))
imagePoints = np.reshape(points, (4,2,1), dtype=np.float32)

print(imagePoints)
imagePoints[0] = [[points[0][0]], [points[0][1]]]
imagePoints[1] = [[points[1][0]], [points[1][1]]]
imagePoints[2] = [[points[2][0]], [points[2][1]]]
imagePoints[3] = [[points[3][0]], [points[3][1]]]


print(imagePoints)

print(np.random.random((4,2,1)))
