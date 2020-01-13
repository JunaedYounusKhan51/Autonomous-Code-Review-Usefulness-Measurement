

class File_List:
    wordList=[]

    def __init__(self):
        self.wordList = ['.c', '.h', '.java', '.py', '.php',

                    '.html', '.css', '.xml', '.tcp', 'sqlite3.o',

                    'sqlite.o', 'sqlite2.o', '.sh', '.dat', '.josn',

                    'http', 'www', 'sconscript',

                    ]

    def getList(self):
        return self.wordList