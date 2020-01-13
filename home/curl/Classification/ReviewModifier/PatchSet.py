import re

class PatchSet:

    def __init__(self,review):
        self.review=review

    def getPatch(self):

        firstLine = self.review.splitlines()[0]
        #print(firstLine)

        patchSet = r'Patch Set [0-9]+:'
        patch = re.findall(patchSet, firstLine, re.IGNORECASE)

        if patch:
            #print(patch)

            digit = r'\d+'
            patchNo = re.findall(digit, patch.__str__(), re.IGNORECASE)

            if patchNo:
                #print("PatchSet : %s" % patchNo)
                return int(patchNo[0])

            else:
                #print("Patch Number NOT Found")
                return 0

        else:
            print("Please Mention Patch Set First")
            return -99999