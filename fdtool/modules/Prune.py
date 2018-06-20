# Prune(C_km1, C_k, E) - exploits the four
#                        pruning rules to reduce the size of search space
#
# for each S *Exists* C_k
#   for each Y -> v_i *Exists* C_km1
#        if (X *isContainedIn* S) then
#        {
#           if (X *Exists* {Z | Y <-> *Exists* E}) then
#           {
#               delete S from C_k;  //Pruning rule 1
#               break;
#           }
#           if (X* *isContainedIn* S) then
#           {
#               delete S from C_k;  //Pruning rule 2
#               break;
#           }
#           S* = S* *Union* X*;     //Pruning rule 3
#           if (U == S *Union* S*) then
#           {
#               delete S from C_k;  //Pruning rule 4
#               break;
#           }
#   }
# return (C_k);

import binaryRepr, Apriori_Gen

def f(C_k, E, Closure, df, U):

    # Define empty list to store sets to remove from C_k
    SetsToRemove = []
    
    # Iterate through k-level candidates
    for S in C_k:

        # Iterate through all candidates at k-1-level, pruned and unpruned
        for X in [x for x in Apriori_Gen.oneDown(C_k) if len(Closure[binaryRepr.toBin(x,U)]) > 1]:
            
            # Check if X is subset of S
            if set(X).issubset(set(S)):

                # Put exclusive closure of X in union with inclusive closure of S; S^{+} = S^{+} U X^{*}
                Closure[binaryRepr.toBin(S, U)] = Closure[binaryRepr.toBin(S,U)].union(Closure[binaryRepr.toBin(X, U)].difference(set(X)))
                
                # Check if X is a consequent in any of the equivalences in E
                if any(set(X) == set(E[EQ][1]) for EQ in range(len(E))):
                    # Remove S from C_k
                    SetsToRemove.append(S)
                    
                    if len(X) == 1: 
                        try:
                             # Drop column if in the relation
                             df = df.drop(X, 1)
                        except (KeyError, ValueError, TypeError) as e:
                            # Pass if attribute does not appear in the relation
                            pass;
                    
                    continue;
                
                # Check if S is contained in X^{+}
                if set(S).issubset(Closure[binaryRepr.toBin(X, U)]):
                    # Remove S from C_k
                    SetsToRemove.append(S)
                    continue;                
                
                # Check if S^{+} is equal to U
                if set(U) == Closure[binaryRepr.toBin(S, U)]:
                    # Remove S from C_k
                    SetsToRemove.append(S)
                    continue;

    # Return sets in C_k that are not to be removed
    return [Candidate for Candidate in C_k if Candidate not in SetsToRemove], Closure, df;

