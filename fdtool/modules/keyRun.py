from dbschema import dbschema
from string import ascii_lowercase
# This function
# takes in well-formatted FDs
# and passes them through certain
# dbschemacmd functions to return keys

def f(U, alphaString, FD_Store):

    # Change format of FDs so they can be passed through dbschema
    FD_Str = ",".join(["".join([str(k[0]), "->", str(k[1])]) for k in FD_Store])

    # Follow path given in dbschema to obtain keys with FDs
    dbschemaNotation = (alphaString, FD_Str)
    (attrastxt, abhastxt) = dbschemaNotation
    (attrs,abhh) = dbschema.ScanAttrAbh(attrastxt, abhastxt)
    abhh=dbschema.mincoverage(abhh)
    (primattr, keys) = dbschema.keysTreeAlg(attrs, abhh, 2)
    KeyList = map(dbschema.attr2str, keys)

    # Create column_dict
    Column_Dict = {ascii_lowercase.upper()[i]: U[i] for i in range(len(U))}

    # Reformat key list
    KeyList = [str("{" + ", ".join([Column_Dict[char] for char in KeyList[k]]) + "}") for k in range(len(KeyList))]

    return KeyList;







