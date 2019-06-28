#!/usr/bin/python
# -*- coding: utf8
#
# dbschema v1.0
#  database schema normalization library and test module
#  (c) copyright by Elmar Stellnberger, the original author: Apr 2014 (12.-26.04.2014)
#  This program may be used under the terms of C-FSL v1.0; you need to keep this license as available under https://www.elstel.org/license/C-FSL-v1.0.txt attached to all other files required by dbschemacmd.
#
#  further information: www.elstel.org/com; look here for an actual contact address
#  current email: estellnb@elstel.org; additional email estellnb@gmail.com
#
# v.1.0.5: some mandatory bugfixes + filterabh as global procedure
#          syntesis3NF: subset relation finding, dependency filtering
#          splitBCNF: error resolved: did not split if only one dependency was in relation
#          some functional improvements for splitBCNF: better printing, split by any normal form
#
# v.1.0: initial release including key detection, min/maxclosure, 3NF and BCNF normalization
#

import sys,re,string,math;
from itertools import *

lowercase = string.ascii_lowercase + u"ßäöüçáéíóúàèìòùãẽĩõũâêîôûëï";
uppercase = string.ascii_uppercase + u"ÄÖÜÇÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛËÏ"
letters = lowercase + uppercase;

def upcSplit(s):
  attr = None; attrs = set();
  for c in s:
    if c in uppercase: 
      if attr!=None: attrs.add( attr );
      attr = c;
    else:
      if attr==None: attr=""; # attribute starting with lower case
      attr += c;
  if attr!=None: attrs.add( attr );
  return attrs;

def unionUpcSplit(s):
  return map(set,chain(*map(upcSplit,s)));

sep = re.compile("[ ]*[/, \r\n][ ]*");
intdepsep = re.compile(";");
allsep = re.compile("[ ]*[,; ][ ]*");

global upcsplit; upcsplit = True; # split on upcase

def ScanAttr( attrsastxt ):
  findattr = attrsastxt=="";
  if upcsplit:
    attrs = set(chain(*map(upcSplit,allsep.split(attrsastxt))));
    for a in attrs:
      if len(a)==0: raise NameError("empty string instead of attribute")
      if a[0] not in uppercase: raise NameError("attribute does not start with uppercase letters: "+a)
  else:
    attrs = set(allsep.split(attrsastxt));
  return attrs;

def ScanAbh( abhhastxt ):
  abhh = {};
  for abhtx in sep.split(abhhastxt):
    if abhtx.strip()=="": continue;
    try: (li,re) = abhtx.split("->",1);
    except ValueError: raise ValueError("split by '->' did not succeed for rules: '%s' ('%s')" % (abhtx,abhhastxt) );
    li = frozenset(intdepsep.split(li)); re = set(intdepsep.split(re));
    if upcsplit: 
      li = frozenset(chain(*map(upcSplit, li )));
      re = set(chain(*map(upcSplit, re )));
    if li in abhh:
      abhh[li] = abhh[li].union( re );
    else:
      abhh[li] = re;
  return abhh;

def ScanAttrAbh( attrstxt, abhtxt ):
  return ( ScanAttr(attrstxt), ScanAbh(abhtxt) );

global sort; shouldsort = True; 

def attr2str(attrs,attrsep='' if upcsplit else ';'):
  attrs = list(attrs);
  if shouldsort: attrs.sort();
  return attrsep.join(attrs);

def abh2str(li,re):
  attrsep = '' if upcsplit else ';'
  li = list(li); re = list(re); 
  if shouldsort: li.sort(); re.sort();
  return attrsep.join(li) + '->' + attrsep.join(re);

def abhh2str(abhh,linesep='\n'):
  lii = list(abhh.keys()); 
  def setcmp(set1,set2): return cmp( ''.join(set1), ''.join(set2) )
  if shouldsort: lii.sort(setcmp);
  result="";  
  for li in lii:
    result = result + abh2str(li,abhh[li])+linesep;
  if '\n' not in linesep and '\r' not in linesep:
    result = result[0:-len(linesep)];
  return result;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def closure(attrs,abh):
  # as long as there is any dependency that can derive new attributes use this dependency
  # stop when all dependencies have been considered and no new attribute was added
  try:
    haschanged = True;
    while haschanged:
      haschanged = False;
      for (li,re) in abh.items():
        if li <= attrs and not re <= attrs: 
          attrs = attrs.union(re);
          haschanged = True;
  except Exception as ex:
    print >>sys.stderr, "error in dependency: %s->%s" % (li,re)
    raise ex;
  return attrs;


def shuffle(lis,num):   # permutates lis according to num
  newlis=[]; positions=1;
  while positions <= len(lis):	  
    item = lis[len(lis)-positions]; 
    newlis.insert( int(num % positions), item );
    num = num / positions;
    positions+=1;
  return newlis;

#
#  the minimum coverage of a ruleset can be found by trying to leave out every individual rule (with singleton right handside)
#  and by trying to reduce each left side by each attribute of a left side
#  this is exactly what the following algorithm does though it bundles rules with the same left side
#  the left side of a functional dependency or rule is called antecedent while the right sides of a rule are called consequent
#

def mincoverage(abh,scramble=0,hints={}):
  # abh contains the functional dependencies (antecedent->consequent-set) as dictionary
  # the keys of the dictionary are antecedents while the nodes of the value set each depict a functional dependency by listing
  # consqeuents which have the common antecedent of the dictionary key.
  # we will call all functional dependencies with common antecedent a dependency/ rule bundle
  
  # collect all antecedent configurations in traverse; put one variable configurations first 
  # finally shuffle all dependency bundles according to scramble

  traverse = [];
  for key in abh.keys():
    if len(key)==1: traverse = [ key ] + traverse;
    else: traverse.append(key);
  traverse = shuffle(traverse,scramble)


  while len(traverse) > 0:
    # now for each rule bundle do:
    li = traverse.pop(); re=abh[li];

    # create a set of reduced dependencies ( E = F \ { X->AB } ) where the current rule bundle is not part of, [[ E ~ redabh, F ~ abh, li ~ X ]]
    redabh = abh.copy(); del redabh[li];

    # now make a course grained test which dependencies can be left out because their right side attributes can also be derived via other rules not being part of the current rule bundle
    # Y´ = AB \ X^+_E, E´ = E \union { X -> Y´ } => E´^+ = F^+       // X^+_E .. closure of X under the rules of E, 
    othersclosure = closure(li,redabh);
    newre = re.difference(othersclosure).difference(li);

    # now try to leave out every individual dependency of the rule bundle while all other dependencies of the same rule bundle are still in place
    # if one dependency can be substituted by other dependencies then this dependency is deleted
    #  G = E \union {  X -> Y´\D[i] },  D[i] \elementof Y´ 
    #  D[i] \elementof X^+_G => Y´´ = Y´\D[i] (otherwise Y´´ = Y´), repeat with Y´ := Y´´; the following condition holds G^+ = F^+  
    # do so by adding the right sides to the input argument of the following closure call instead of adding these as separate dependencies of the rule bundle: 
    #  D[i] \elementof X^+_G <=> D[i] \elementof ( X^+_E \union Z ), Z = X \union Y´ \ D[i],  [[ Z ~ precond ]] because Z \ispartof X+_G

    liset = set(li); precond = liset.union(re);
    newre_list = list(newre); # similar to newre.copy()

    if li in hints:
      # as scramble only permutates rule bundles we have here a possibility to order dependencies listed in hints first
      firsttouch = newre.difference(hints[li]);	  # subtract some values
      lasttouch = newre.difference(firsttouch);	  # re-add them at the end
      newre_list = list(firsttouch)+list(lasttouch);

    for r in newre_list:
      precond.remove(r);
      if r in closure(precond,redabh):   # precond already contains the right sides of the other rules
	      newre.remove(r);                 # this is the same as closure( li, redabh + {li->each other right side} )
      else:
	      precond.add(r);

    if len(newre) == 0:
      abh = redabh; 

    else:
      installed_newre = False;
      if len(li) > 1:
	# minimize the left side: see if the rest can be inferenced out of a part of the left side
	# left side will never fall short as a whole
	# you may believe that there is a possible flaw in the following implementation:
	# it tries to reduce the left side for the whole rule bundle only
	# however if the start set misses one precondition of the other rules those rules could never fire (unless this precondition got inferenced)
	# i.e. if they can never fire the other rules of the rule bundle do not need to be considered  (however if it gets inferenced then leaving it out will already be ok)
        lired = liset;
        for l in li:
          tryred = lired.copy(); 
          tryred.remove(l);
          cls = closure(tryred,redabh)
          if li <= cls:
            lired = tryred;
	
	# now if the left side has been successfully reduced make these changes persistent
        if lired != li:
          abh = redabh; lired = frozenset(lired);  # left sides need to be unchangeable frozensets in order to serve as dictionary keys
          if lired in abh:
            # if there do already exist rules which have a left side being the same as our new reduced left side add the new rules here
            abh[lired] = abh[lired].union(newre);
          else:
            # otherwise add as new rule bundle
            abh[lired] = newre;
            installed_newre = True;

          if not installed_newre:
        # install the reduced right side if the left side has stayed the same
            abh = redabh;
            abh[li] = newre;

  return abh;

def keyBaseSets(attr,abh):
  # group attributes in 4 different base setes: 
  #  0.) attributes that do not occur in rules 
  #  1.) attributes found on the left side only 
  #  2.) attrs found on the right side only 
  #  3.) attributes found on both sides of a rule
  attrch = dict( [ (a,0) for a in attr ] )
  for (li,re) in abh.items():
    for l in li: attrch[l] = attrch[l] | 1;
    for r in re: attrch[r] = attrch[r] | 2;
  sets = ( set(), set(), set(), set() )
  for (a,ch) in attrch.items():
    sets[ch].add(a);
  return sets;

#
#  a key is a minimal set of attributes whose closure is the whole set of attributes
#  construct keys by successively adding singleton attributes to an existing attribute set
#  as soon as a superkey is discovered check whether a key with smaller attribute number is already part of this superkey; if so dismiss the current attribute set
#  otherwise a new key has been found
#

def keysTreeAlg( attr, abh, verbty=None ):
  global verbosity; verbty = verbosity if verbty==None else verbty;
  (ua,li,re,mi) = keyBaseSets(attr,abh);
  # attributes only occuring on the right side can be inferenced by other attributes which are part of at least on left side
  # they do not need to be considered for key candidates as they do not derive other attributes but can be derived by some left side
  # ua and li attributes need to be part of any key as they can otherwise never be derived
  subkey = frozenset( li.union(ua) );

  if closure(subkey,abh) == attr:  # if the minimum subkey is already a key return it
    finalkey = subkey;
    return (finalkey,{finalkey}); 

  keys = set(); curlvl = dict(); primattr = set(); lvl=1; lpad='';
  for m in mi:  # search for keys by adding one attribute of the middle set (attrs of the middle can derive new attributes but are not yet part of subkey)
    csk = subkey.union(frozenset(m));  
    if closure(csk,abh) == attr: 
      for p in csk: primattr.add(p);
      keys.add( csk );
    else: # if adding one attribute to the set does not produce a key remember this attribute set
      curlvl[ csk ] = m;


  while len(curlvl) > 0:
    # at the entrance of this loop curlevel contains all key candidates with len(subkey) + lvl attributes
    prevlvl = curlvl; curlvl = dict(); lvl+=1; lpad+=' ';

    for subkey, maxm in prevlvl.items():
      # pick one of the not yet selected attributes that is listed alphabetically after the alphabetically highest attribute that already is part of the set
      # this ensures that the same attribute configuration is only considered once in ascending order of the individual attributes
      missingattr = set();
      for a in mi: 
	      if a > maxm and a not in subkey: missingattr.add(a);

      for m in missingattr:
	      newattr = subkey.union(frozenset(m));   # do pick the attribute
	      ispartofkey = False;
    for key in keys:
      if key <= newattr:
        ispartofkey = True;
        break;
    if not ispartofkey:
      if closure(newattr,abh) == attr:
        keys.add(newattr);
        for p in newattr: primattr.add(p);
      else: # if neither a new key was found nor has the new attribute configuration been a superset of an existing key 
            # then remember this configuration and add one more attribute in the next step
        curlvl[newattr] = max(maxm,m);
	
  return (primattr,keys);


