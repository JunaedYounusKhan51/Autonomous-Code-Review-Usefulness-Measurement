import re

class LineNo:

    def __init__(self,review):
        self.review=review

    def getLineNo(self):

        line = r'line [0-9]+:'

        lineNo = re.findall(line, self.review, re.IGNORECASE | re.MULTILINE)
        if not lineNo:
            #print(" No LineNo Found")
            return 0
        else:
            #print("Total Line no: %s" % len(lineNo))
            return len(lineNo)