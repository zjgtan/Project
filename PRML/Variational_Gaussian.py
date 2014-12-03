#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

N = 10000
X_train = np.random.normal(100, 1.0, N)

u0 = 1
lada0 = 0.1

a0 = 0.
b0 = 0.

X_mean = np.mean(X_train)
X_2_sum = np.sum(X_train * X_train)
X_sum = np.sum(X_train)

#E_tau = a / b

u = u0
lada = lada0

E = []

for i in range(2):
	E_u_2 = u * u + 1 / lada
	E_u = u

	a = a0 + N / 2
	b = b0 + 0.5 * X_2_sum - E_u * X_sum + 0.5 * N * E_u_2 + 0.5 * lada0 * E_u_2 - lada0 * E_u * u0 + 0.5 * lada0 * u0 * u0

	E_tau = a / b


	u = ((lada0 * u0) + N * X_mean) / (lada0 + N)
	lada = (lada0 + N) * E_tau

	E.append(E_u)

print "u: 0, {0}".format(u)
print "tau: 1.0, {0}".format(E_tau)


plt.plot(np.array(E))
plt.show()


