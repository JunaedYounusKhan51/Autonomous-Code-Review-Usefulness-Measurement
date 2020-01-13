

class Pos_Neg_Word_List:
    posWordList=[]
    negWordList=[]

    def __init__(self):
        self.posWordList = ['assert', 'big', 'expand', 'least',

                            'log', 'fix', 'match', 'action',

                            'rather', 'please', 'correct', 'should',

                            'remove', 'move', 'make sure', 'great',

                            'check',

                    ]
        self.negWordList = ['leave', 'yes', 'yea', 'doesn\'t','don\'t', 'which', 'why',

                            'how', 'what', 'fail', 'already',

                            'really', 'good', 'bad', 'nice', 'worst',

                            'poor', 'actually', 'but', 'not', 'not sure', 'doubt',

                            'guess', 'may be',

                            ]

    def getPosList(self):
        return self.posWordList

    def getNegList(self):
        return self.negWordList