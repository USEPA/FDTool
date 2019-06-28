# FD Mine(r(U))

# Input: A relation r(U) over U = {v_1, ... ,v_m}

# Output: A set F of functional dependences over r(U)

# F = Null_Set

# E = Null_Set

# C_1 = U

# k = 1

#

# C_k = CalculatePartition(C_k, r(U))

# C_k = InitialClosure(C_k)

# while Cardinality(C_k) > 0:

#{

#   k += 1

#   C_k = Apriori_Gen(C_km1)

#   C_k = CalculatePartition(C_k, r(U))

#   C_k = InitialClosure(C_k)

#   F = F *Union* ObtainFDs(C_km1)

#   E = E *Union* ObtainEquivalences(C_km1, F)

#   C_k = Prune(C_km1, C_k, E)

#}



__version__="0.1.7"





import pandas as pd

import sys, time, argparse, ntpath, pickle, csv

from .modules import *

from string import ascii_letters, ascii_uppercase

from .config import MAX_K_LEVEL



def main():



    # Define filePath

    filePath = sys.argv[1]

    letters = ascii_uppercase + u"ÄÖÜÇÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛËÏ"



    # Print reading file

    print("\n" + "Reading file: \n" + str(filePath) + "\n"); sys.stdout.flush();

    # Define file extension from path

    fileExtension = ntpath.basename(filePath).split('.')[-1]



    if not fileExtension == "pkl":

        # Read in file, determine whether a pkl or txt/csv

        try:

            

            # Detect delimiter

            sniffer = csv.Sniffer()

            sniffer.preferred=[',','|',';',':','~']            

            csvFile=open(filePath, 'r', encoding='utf-8')

            for row in csv.reader(csvFile, delimiter="\t"):

                row1=row

                break;

            csvFile.close()

            dialect=sniffer.sniff(str(row1))

            sepType = dialect.delimiter



            if sepType not in {",", "|", ";", ":", "~"}:

                print("Invalid delimiter")

                sys.stdout.flush()

                return;



            # Read in pandas data frame from csv file

            df = pd.read_csv(filePath, sep = ";");

        except pd.errors.ParserError:

            print("Invalid file")

            sys.stdout.flush()

            return;

        except IOError:

            print("File not found")

            sys.stdout.flush()

            return;

    else:

        try:

            # Read in pandas data fram pkl file

            df = pd.read_pickle(filePath);

        except IOError:

            print("File not found")

            sys.stdout.flush()

            return;



    # Define start time

    start_time = time.time()

    

    # Create default name for outFile if one is not chosen on command

    if len(sys.argv) > 2: file  = open(sys.argv[2], 'w+')

    else: file = open(str(ntpath.basename(filePath)).split('.')[0] + '.FD_Info.txt', 'w+')

    

    # Add name of file , row count, columns to info string

    file.write(str("Table : " + str(ntpath.basename(filePath)).split('.')[0] + "\n" + "Columns : " 

        + str(", ".join(list(df.head(0)))) + "\n\n" + "Functional Dependencies: \n"))



    # Print line

    print("Functional Dependencies: "); sys.stdout.flush();

    # Define header; Initialize k; 

    U = list(df.head(0)); k = 0;

    

    try:

        # Create dictionary to convert column names into alphabetical characters

        Alpha_Dict = {U[i]: letters[i] for i in list(range(len(U)))}

    except IndexError:

        print("Table exceeds max column count")

        sys.stdout.flush()

        return;

    

    # Initialize lattice with singleton sets at 1-level

    C = [[[item] for item in U]] + [None for level in range(len(U) - 1)]

    # Create Generator to find next k-level attribute subsets

    Subset_Gen = ([x for x in Apriori_Gen.powerset(U) if len(x) == k] for k in range(1, len(max(Apriori_Gen.powerset(U), key=len))+1))

    # Initialize Closure as Python dict

    Closure = {binaryRepr.toBin(Subset, U) : set(Subset) for Subset in next(Subset_Gen)}

    # Initialize Cardinality as Python dict

    Cardinality = {element : None for element in Closure}

    # Create counter for number of Equivalences and FDs; initialize list to store FDs; list to store equivalences;

    Counter=[0,0]; FD_Store = []; E_Set = [];



    while True:

        try:

        

            # Increment k; initialize C_km1

            k += 1; C_km1 = C[k-1];

            # Initialize Closure at next next k-level; update dict accordinaly

            Closure_k = {binaryRepr.toBin(Subset, U) : set(Subset) for Subset in next(Subset_Gen)}; 
            Closure.update(Closure_k);

            # Update Cardinality dict with next k-level

            Cardinality.update({element: None for element in Closure_k})



            if k > 1:

                # Dereference Closure and Cardinality at (k-2)-level

                for Subset in C[k-2]: del Closure[binaryRepr.toBin(Subset, U)], Cardinality[binaryRepr.toBin(Subset, U)];

                # Dereference (k-2)-level

                C[k-2] = None;



            # Run Apriori_Gen to get k-level Candidate row from (k-1)-level Candidate row

            C_k = Apriori_Gen.oneUp(C_km1)

            # Run GetFDs to get closure and set of functional dependencies

            Closure, F, Cardinality = GetFDs.f(C_km1, df, Closure, U, Cardinality)

            # Run Obtain Equivalences to get set of attribute equivalences

            E = ObtainEquivalences.f(C_km1, F, Closure, U)

            # Run Prune to reduce next k-level iterateion and delete equivalences; initialize C_k

            C_k, Closure, df = Prune.f(C_k, E, Closure, df, U); C[k] = C_k;

            #Increment counter for the number of Equivalences/FDs added at this level

            Counter[0] += len(E); Counter[1] += len(F); E_Set += E

            

            # Print out FDs

            for FunctionalDependency in F:

                # Store well-formatted FDs in empty list

                FD_Store.append(["".join(sorted([Alpha_Dict[i] for i in FunctionalDependency[0]])), Alpha_Dict[FunctionalDependency[1]]]);

                # Create string for functional dependency

                String = "{" + ", ".join(FunctionalDependency[0]) + "} -> {" + str(FunctionalDependency[1]) + "}"

                # Print FD String

                print(String); sys.stdout.flush();

                # Write string to TXT file

                file.write(String + "\n")

            

            # Break while loop if cardinality of C_k is 0

            if not len(C_k) > 0: break;

            # Break while loop if k-level reaches level set in config

            if k is not None and MAX_K_LEVEL ==k: break;

        except StopIteration:
            break




    # Print equivalences

    file.write("\n" + "Equivalences: " + "\n")

    print("\n" + "Equivalences: "); sys.stdout.flush();

    # Iterate through equivalences returned

    for Equivalence in E_Set:

        # Create string for functional dependency

        String = "{" + ", ".join(Equivalence[0]) + "} <-> {" + ", ".join(Equivalence[1]) + "}"

        # Print equivalence string

        print(String); sys.stdout.flush();

        # Write string to TXT file

        file.write(String + "\n")



    # Print out keys 

    file.write("\n" + "Keys: " + "\n")

    print("\n" + "Keys: "); sys.stdout.flush();

    # Get string of column names sorted to alphabetical characters

    SortedAlphaString = "".join(sorted([Alpha_Dict[item] for item in Alpha_Dict]))

    # Run required inputs through keyList module to determine keys with

    keyList = keyRun.f(U, SortedAlphaString, FD_Store);

    # Iterate through keys returned

    for key in keyList:

        # Write keys to file

        file.write(str(key) + "\n")

        # Print keys

        print(str(key)); sys.stdout.flush();

    

    # Create string to give user info of script

    checkInfoString = str("\n" + "Time (s): " + str(round(time.time() - start_time, 4)) + "\n"

            + "Row count: " + str(df.count()[0]) + "\n" + "Attribute count: " + str(len(U)) + "\n"

            + "Number of Equivalences: " + str(Counter[0]) + "\n" + "Number of FDs: " + str(Counter[1]) + "\n"

            "Number of FDs checked: " + str(GetFDs.CardOfPartition.calls))

    

    # Write info at bottom

    file.write(checkInfoString)

    #Print elapsed time

    print(checkInfoString); sys.stdout.flush();

    # Close file

    file.close()