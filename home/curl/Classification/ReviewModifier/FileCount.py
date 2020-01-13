from File_List import File_List


class FileCount:

    def __init__(self,review):
        self.review=review
        self.count=0

    def getFileCount(self):

        str=self.review.lower()

        fileList=File_List()
        wordList=fileList.getList()

        for word in wordList:
            calc=str.count(word)
            if(calc>0):
                pass#print(word,calc)

            self.count=self.count+ calc
        #print("Total ProgWordCount: %s" % self.count)
        return self.count
