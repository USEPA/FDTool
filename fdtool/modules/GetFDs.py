import binaryRepr

# Create decorator function to see how many times functions are called
def call_counter(func):
    
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs);
    helper.calls = 0
    helper.__name__= func.__name__
    return helper;

# Calculate Partition (C_k, r(U)) - the partitions
#                                   of each candidate at level k are calculated
# Takes in data frame of relation and a candidate in C_km1
# Outputs partition of Candidate in C_km1 in relation to data frame

@call_counter
def CardOfPartition(Candidate, df):

    # If length is one, find number of unique elements in column
    if len(Candidate) == 1: return df[Candidate[0]].nunique()
    # If length is +1, create groups over which to find number of unique elements
    else: return df.drop_duplicates(Candidate).count()[0];

# Obtain FDs(C_km1) - checks the FDs of each
#                     candidate X in C_k
#                   - FDs of the form X -> v_i, where
#                     v_i *Exists* U - X^{+} are checked by 
#                     comparing *Partition* X and *Partition* X v_i
#
# F = Null_Set
# for each candidate X in C_km1 
#   for each v_i *exists* U - X^{+}     \\Pruning rule 3
#       if (Cardinality(*Partition* X) == Cardinality(*Partition X v_i)) then
#       {
#           X* = X *Union* {v_i}
#           F = F *Union* {X -> v_i}    \\Theorem 2
#       }
#   return (F);

def f(C_km1, df, Closure, U, Cardinality):

    # Set F to null list; Initialize U_c to remaining columns in data frame
    F = []; U_c = list(df.head(0));
    
    # Identify the subsets whose cardinality of partition should be tested
    SubsetsToCheck = [list(Subset) for Subset in set([frozenset(Candidate + [v_i]) for Candidate in C_km1 for v_i in list(set(U_c).difference(Closure[binaryRepr.toBin(Candidate, U)]))])];
    
    # Add singleton set to SubsetsToCheck if on first k-level
    if len(C_km1[0]) == 1: SubsetsToCheck += C_km1;
    
    # Iterate through subsets mapped to the Cardinality of Partition function
    for Cand, Card in zip(SubsetsToCheck, map(CardOfPartition, SubsetsToCheck, [df]*len(SubsetsToCheck))):
        # Add Cardinality of Partition to dictionary
        Cardinality[binaryRepr.toBin(Cand, U)] = Card;

    # Iterate through candidates of C_km1
    for Candidate in C_km1:
        # Iterate though attribute subsets that are not in U - X{+}; difference b/t U and inclusive closure of candidate    
        for v_i in list(set(U_c).difference(Closure[binaryRepr.toBin(Candidate, U)])):
            # Check if the cardinality of the partition of {Candidate} is equal to that of {Candidate, v_i}
            if Cardinality[binaryRepr.toBin(Candidate, U)] == Cardinality[binaryRepr.toBin(Candidate + [v_i], U)]:
                # Add attribute v_i to closure
                Closure[binaryRepr.toBin(Candidate, U)].add(v_i)
                # Add list (Candidate, v_i) to F
                F.append([tuple(Candidate), v_i]);
    
    return Closure, F, Cardinality;
