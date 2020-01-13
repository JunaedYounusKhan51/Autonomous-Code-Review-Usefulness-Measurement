from Classification.Classifier import Classifier
from ReviewExtractor import ReviewExtractor
from collections import Counter
import sqlite3

'''
connection=sqlite3.connect('Gerrit2.db')
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS reviewTable(review_id TEXT,reviewer TEXT, review_date DATE, reviewData TEXT, usefulness TEXT)")
'''

clf = Classifier()
#clf.feedReview(file)
reviewExtractor=ReviewExtractor()
reviewExtractor.query('iotivity')

print(reviewExtractor.getChangeListSubjects())

'''
ownerList=reviewExtractor.getOwnerList()
print("Project Owners: ")
for name in ownerList:
    print (name)
'''

changeList=reviewExtractor.getChangeList()


def showUsefulness(clf, changeList):
    for index,change in enumerate(changeList,start=1):
        file = open("change"+str(index)+".txt", 'w')

        file.write("Change Id: %s\n" % str(reviewExtractor.getChangeId(change)))
        file.write("Change Subject: " + reviewExtractor.getChangeSubject(change)+"\n")
        file.write("______________________________________________________________________\n\n")
        reviewInfo = reviewExtractor.getReviewInfo(change)

        owner=reviewExtractor.getChangeOwner(change)

        for review in reviewInfo:
            reviewer = reviewExtractor.getReviewer(review)
            if ((reviewer.startswith("jenkin")) or reviewer.endswith("jenkin") or (reviewer==owner)):
                continue
            reviewId=reviewExtractor.getReviewId(review)
            file.write("Review Id: " + reviewId+"\n")
            file.write("Reviewer: " + reviewer+"\n")
            reviewDate=reviewExtractor.getReviewDate(review)
            file.write("Date: " + reviewDate+"\n")
            reviewData = reviewExtractor.getReview(review)
            file.write("Review: " + reviewData+"\n")
            isLast=reviewExtractor.isLast(change,review)
            #file.write("isLast: " + str(isLast)+str(review['_revision_number']))
            clf.feedReview(reviewData,isLast)
            usefulness=clf.getPrediction()
            file.write("\nUSEFULNESS: " + usefulness+"\n")
            file.write("\n#################################################\n\n")

            '''
            cursor.executemany("INSERT INTO reviewTable(review_id,reviewer, review_date, reviewData , usefulness)"
                           " VALUES(?,?,?,?,?)",[(reviewId,reviewer.decode('utf-8'),reviewDate,reviewData.decode('utf-8'),usefulness)])
            connection.commit()
            '''


showUsefulness(clf,changeList)





'''
    for change in changeList:
        print("Change Id: %s" % str(reviewExtractor.getChangeId(change)))
        print("Change Subject: " + reviewExtractor.getChangeSubject(change))
        print("______________________________________________________________________")
        reviewInfo = reviewExtractor.getReviewInfo(change)

        for review in reviewInfo:
            reviewer = reviewExtractor.getReviewer(review)
            if (reviewer == "jenkins-iotivity"):
                continue

            print("Review Id: " + reviewExtractor.getReviewId(review))
            print("Reviewer: " + reviewer)
            print("Date: " + reviewExtractor.getReviewDate(review))
            print("Review: " + reviewExtractor.getReview(review))
            print("isLast: " + str(reviewExtractor.isLast(change)))
            print("")

'''



