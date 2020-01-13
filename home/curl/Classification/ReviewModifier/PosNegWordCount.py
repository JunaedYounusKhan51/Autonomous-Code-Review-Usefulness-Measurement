from Pos_Neg_Word_List import Pos_Neg_Word_List


class PosNegWordCount:

    def __init__(self,review):
        self.review=review
        self.pCount=0
        self.nCount=0

    def getPosNegWordCount(self):

        str=self.review.lower()

        posNegList=Pos_Neg_Word_List()
        posWordList=posNegList.getPosList()
        negWordList=posNegList.getNegList()

        for pWord in posWordList:
            calc=str.count(pWord)
            if(calc>0):
                pass#print(pWord,calc)

            self.pCount=self.pCount+ calc

        for nWord in negWordList:
            calc=str.count(nWord)
            if(calc>0):
                pass#print(nWord,calc)

            self.nCount=self.nCount+ calc
        #print("Total ProgWordCount: %s" % self.count)
        return self.pCount, self.nCount


'''
    if __name__=='__main__':
        review=("Patch Set 4: Yea I noticed you did the merge afterwards, yours can go in I gave +1 about the difference I just assumed it was better but I actually don't know")
        p,n=getPosNegWordCount(review)
'''