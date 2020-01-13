
class QuestionMark:

    def __init__(self,review):
        self.review=review
        self.count=0

    def getQuestionMark(self):

        file=self.review
        str=file.lower()
        count=str.count('?')
        #print("Total QuestionMark: %s" % count)
        return count

'''
if __name__=='__main__':
    q=QuestionMark("asd")
    print(q.getQuestionMark())
'''
