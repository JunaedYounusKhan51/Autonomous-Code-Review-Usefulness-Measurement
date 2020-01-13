from Nit_Picking_List import Nit_Picking_List


class NitPickingCount:

    def __init__(self,review):
        self.review=review
        self.count=0

    def getNitCount(self):

        str=self.review.lower()

        nitPickingList=Nit_Picking_List()
        wordList=nitPickingList.getList()

        for word in wordList:
            calc=str.count(word)
            if(calc>0):
                pass#print(word,calc)

            self.count=self.count+ calc
        #print("Total ProgWordCount: %s" % self.count)
        return self.count
