from FileCount import FileCount
from LineNo import LineNo
from NitPickingCount import NitPickingCount
from PatchSet import PatchSet
from PosNegWordCount import PosNegWordCount
from QuestionMark import QuestionMark
from WordCount import WordCount
from ProgWordCount import ProgWordCount


class ReviewModifier:

    def __init__(self,review,isLast=0):
        self.review=review.lower()
        self.isLast=isLast

        self.wordCount=WordCount(self.review)
        self.lineNo=LineNo(self.review)
        self.progWordCount=ProgWordCount(self.review)
        self.fileCount=FileCount(self.review)
        self.questionMark=QuestionMark(self.review)
        self.patchSet=PatchSet(self.review)
        self.posNegWordCount=PosNegWordCount(self.review)
        self.nitCount=NitPickingCount(self.review)

    def getReviewModifier(self):

        wc=self.wordCount.getWordCount()
        ln=self.lineNo.getLineNo()
        pwc=self.progWordCount.getProgWordCount()
        fm=self.fileCount.getFileCount()
        qm=self.questionMark.getQuestionMark()
        pWord,nWord=self.posNegWordCount.getPosNegWordCount()
        nc=self.nitCount.getNitCount()

        sampleList=[[fm,wc,ln,pwc,qm,pWord,nWord,nc,self.isLast]]
        #print("Sample List: %s" % sampleList)
        return sampleList

'''
if __name__=='__main__':
    print(rm.getReviewModifier())

'''