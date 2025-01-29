-- example of using the functions in the symGens file

load "symGens"
R = QQ[x_1..x_3]

I = genSymIdeal {x_1-x_2}
isPSI I

J = genSymIdeal {x_1^2*x_2+x_2^2*x_3+x_3^2*x_1}
K = I*J
numMinSymGens(K)
isPSI K

I = genSymIdeal {random(3, R)}
J = genSymIdeal {random(3, R)}
numMinSymGens(I*J)
