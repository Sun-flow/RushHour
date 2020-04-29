from rushhour import *
def test(los):
    for i in range(2):
        rushhour(i, los)

#test(["--B---","--B---","XXB---","--AA--", "------","------"])
#test(["---O--","---O--","XX-O--","PQQQ--", "P-----","P-----"])
test(["OOOP--","--AP--","XXAP--","Q-----", "QGGCCD","Q----D"])
test(["--OPPP","--O--A","XXO--A","-CC--Q", "-----Q","--RRRQ"])
test(["-ABBO-","-ACDO-","XXCDO-","PJFGG-", "PJFH--","PIIH--"])
test(["OOO--P","-----P","--AXXP","--ABCC", "D-EBFF","D-EQQQ"])
#test(["MMMDEF", "ANNDEF", "A-XXEF", "PPC---", "-BC-QQ", "-BRRSS"])
#test(["GBB-L-", "GHI-LM", "GHIXXM", "CCCK-M", "--JKDD", "EEJFF-"])
