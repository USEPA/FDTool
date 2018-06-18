# ObtainEquivalences(C_km1, F) - obtains equivalent candidates
#                                from the discovered FDs.
#
# E = Null_Set
# for each candidate X in C_km1
#   for each Y -> v_i *Exists* F
#       if (X *isContainedIn* Y^{+} and Y *isContainedIn* X^{+}) then   
#           E = E *Union* { X <-> Y}    \\by Theorem 3
# return (E);

import binaryRepr

def f(C_km1, F, Closure, U):

    # Set E to null list
    E = []
    
    # Iterate through candidates in C_km1
    for X in C_km1:
        # Iterate through functional dependences Y -> v_i in F
        for Y in F:
            # Check if X is contained in inclusive closure of Y and vice versa
            if set(X).issubset(Closure[binaryRepr.toBin(list(Y[0]), U)]) and set(Y[0]).issubset(Closure[binaryRepr.toBin(X, U)]):
                # Check that equivalence is not already in E and is not trivial
                if [tuple(X), Y[0]] not in E and [Y[0], tuple(X)] not in E and Y[0]!=tuple(X):
                    # Append to equivalence set
                    E.append([tuple(X), Y[0]]);
    return E;

