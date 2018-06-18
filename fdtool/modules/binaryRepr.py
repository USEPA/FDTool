# Replaces candidates with binary representation, 1 where attribute exists, 0 otherwise

def toBin(Candidate, U):
    
    # Create generator to fill in '1' for slots in U that candidate fills; '0' otherwise
    Gen = (['1' if k in {U.index(element) for element in Candidate} else '0' for k in range(len(U))])
    # Join generator to string
    return "".join(Gen);
