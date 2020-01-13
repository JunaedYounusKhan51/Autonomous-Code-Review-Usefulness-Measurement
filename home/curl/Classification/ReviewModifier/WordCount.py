
class WordCount:

    def __init__(self,review):
        self.review=review

    def getWordCount(self):

        word_list = self.review.split()
        #print("Total Words: %s" % len(word_list))
        return len(word_list)