#CalculatePartition.py Apriori_Gen (C_km1) - generates all
#                       possible candidates in C_k
#                       from the candidates in C_km1


# Create function to calculate power set
def powerset(s):
    x = len(s)
    # Create list for powerset contents
    Powerset = []
    for i in range(1 << x):
        Powerset.append([s[j] for j in range(x) if (i & (1 << j))])
    return Powerset;

def oneUp(C_km1):
    
    # Flatten list to unique values
    flat_list = list(set([item for sublist in C_km1 for item in sublist]))

    # Create generator containing all subsets of unique attributes
    AttributeSubsets = (Subset for Subset in powerset(flat_list))

    # Generate list of subsets at one level up from input
    return [Subset for Subset in AttributeSubsets if len(Subset) == (len(next(iter(C_km1))) + 1)];
    
def oneDown(C_k):
    
    # Flatten list to unique values
    flat_list = list(set([item for sublist in C_k for item in sublist]))
	
    # Create generator containing all subsets of unique attributes
    AttributeSubsets = (Subset for Subset in powerset(flat_list))

    # Generate list of subsets at one level down from input
    return [Subset for Subset in AttributeSubsets if len(Subset) == (len(next(iter(C_k))) - 1)]; 

