from Prog_Word_List import Prog_Word_List


class ProgWordCount:

    def __init__(self,review):
        self.review=review
        self.count=0

    def getProgWordCount(self):

        str=self.review.lower()

        progWordList=Prog_Word_List()
        wordList=progWordList.getList()

        for word in wordList:
            calc=str.count(word)
            if(calc>0):
                pass#print(word,calc)

            self.count=self.count+ calc
        #print("Total ProgWordCount: %s" % self.count)
        return self.count
