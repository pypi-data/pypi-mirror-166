from tqdm import tqdm
import numpy as np
import warnings

from .lie import poly, lexp

def Sinhc(x):
    if x != 0:
        return np.sinh(x)/x
    else:
        return 1

def bch_2x2(A, B):
    '''
    An implementation of the Baker-Campbell-Hausdorff equation for complex 2x2 matrices, see
    Foulis: "The algebra of complex 2 × 2 matrices and a 
             general closed Baker–Campbell–Hausdorff formula",
             J. Phys. A: Math. Theor. 50 305204 (2017)
    '''
    assert A.shape == (2, 2) and B.shape == (2, 2)
    C = A@B - B@A
    a = A[0, 0] + A[1, 1] # Tr(A)
    b = B[0, 0] + B[1, 1] # Tr(B)
    alpha = A[0, 0]*A[1, 1] - A[1, 0]*A[0, 1] # det(A)
    beta = B[0, 0]*B[1, 1] - B[1, 0]*B[0, 1] # det(B)
    
    AB = A@B
    omega = AB[0, 0] + AB[1, 1] # tr(AB)
    epsilon = omega - a*b/2
    
    sigma2 = a**2/4 - alpha
    tau2 = b**2/4 - beta
    sigma = np.sqrt(sigma2) # sign (...)
    tau = np.sqrt(tau2) # sign (...)
    
    cosh_chi = np.cosh(sigma)*np.cosh(tau) + epsilon/2*Sinhc(sigma)*Sinhc(tau)
    chi = np.arccosh(cosh_chi)

    p = Sinhc(sigma)*np.cosh(tau)/Sinhc(chi)
    q = np.cosh(sigma)*Sinhc(tau)/Sinhc(chi)
    r = Sinhc(sigma)*Sinhc(tau)/(2*Sinhc(chi))
    k = (a + b - a*p - b*q)/2
    
    I = np.eye(2)
    return k*I + p*A + q*B + r*C

def lp2mat(p):
    '''
    Transform a polynomial of order 2 to its respective matrix form (the resulting
    matrix will be traceless).
    '''
    assert p.dim == 1
    a1 = p.get((1, 1), 0)
    a2 = p.get((2, 0), 0)
    a3 = p.get((0, 2), 0)
    out = np.zeros([2, 2], dtype=np.complex128)
    out[0, 0] = -a1*1j
    out[0, 1] = -2*a3*1j
    out[1, 0] = 2*a2*1j
    out[1, 1] = a1*1j
    return out

def mat2lp(mat):
    '''
    Transform a 2x2 matrix of zero trace to a poynomial of 2nd order.
    '''
    assert mat[0, 0] == -mat[1, 1]
    a1 = 1j*mat[0, 0]
    a2 = -1j/2*mat[1, 0]
    a3 = 1j/2*mat[0, 1]
    return poly(values={(1, 1): a1, (2, 0): a2, (0, 2): a3})

def hadamard2d(*hamiltonians, keys, exact=False, **kwargs):
    '''
    Rearrange the terms in a sequence of Hamiltonians according to Hadamard's theorem:

    Consider a sequence of Hamiltonians
       h0, h1, h2, h3, h4, h5, ...
    By Hadamard's theorem, the sequence is equivalent to
       exp(h0)h1, h0, h2, h3, h4, h5, ...
    Continuing this argument, we could write
       exp(h0)h1, exp(h0)h2, h0, h3, h4, h5, ...
    and so on, so that we reach
       exp(h0)h1, exp(h0)h2, exp(h0)h3, ..., exp(h0)hn, h0

    Instead of applying exp(h0) to every entry, we can perform this procedure with every 2nd
    term of the sequence:

       exp(h0)h1, h0, h2, h3, h4, h5, ...

       exp(h0)h1, h0, exp(h2)h3, h2, h4, h5, ...

       exp(h0)h1, exp(h0)exp(h2)h3, h0, h2, h4, h5, ...

       exp(h0)h1, exp(h0)exp(h2)h3, h0, h2, exp(h4)h5, h4, ...

       exp(h0)h1, exp(h0)exp(h2)h3, exp(h0)exp(h2)exp(h4)h5, h0, h2, h4, ...

    If not every second entry, but instead a list like h0, h2, h3 and h5 are of interest, then:

       exp(h0)h1, h0, h2, exp(h3)h4, h3, h5, ...

       exp(h0)h1, exp(h0)exp(h2)exp(h3)h4, h0, h2, h3, h5, ...

    In this routine the Hamiltonians are distinguished by two families defined by keys.
    Family one will be treated as the operators h0, h2, h3, h5, ... in the example above,
    which will be exchanged with members of family two.
    
    !!! Attention !!! 
    Only polynomials of dim 1 (i.e. 2D phase spaces) are supported at the moment.
    
    Parameters
    ----------
    hamiltonians: poly object(s)
        The Hamiltonians to be considered.
        
    keys: list
        A list of keys to distinguish the first group of Hamiltonians against the second group.
        
    exact: boolean, optional
        Whether to distinguish the Hamiltonians of group 1 by the given keys (True) or a subset of the given keys (False).
        
    **kwargs
        Optional keyworded arguments passed to the lexp.calcFlow routine.
    
    Returns
    -------
    list
        A list of the Hamiltonians [exp(h0)h1, exp(h0)exp(h2)exp(h3)h4, ...] as in the example above.
        
    poly
        A polynomial representing the last Hamiltonian h0#h2#h3#h5, ... as in the
        example above. Here '#' denotes the Baker-Campbell-Hausdorff operation.
    '''
    current_g1_op = []
    new_hamiltonians = []
    for hamiltonian in tqdm(hamiltonians, disable=kwargs.get('disable_tqdm', False)):
        
        if exact:
            condition = hamiltonian.keys() == set(keys)
        else:
            condition = set(hamiltonian.keys()).issubset(set(keys))
        
        if condition:
            # in this case the entry k belongs to group 1, which will be exchanged with the
            # entries in group 2.
            if len(current_g1_op) == 0:
                current_g1_op = lp2mat(hamiltonian)
            else:
                current_g1_op = bch_2x2(current_g1_op, lp2mat(hamiltonian))
        else:
            if len(current_g1_op) == 0:
                new_hamiltonians.append(hamiltonian)
            else:
                op = lexp(mat2lp(current_g1_op), **kwargs)
                new_hamiltonians.append(op(hamiltonian, **kwargs))
    if len(current_g1_op) == 0 or len(new_hamiltonians) == 0:
        warnings.warn(f'No operators found to commute with, using keys: {keys}.')
    return new_hamiltonians, mat2lp(current_g1_op)
