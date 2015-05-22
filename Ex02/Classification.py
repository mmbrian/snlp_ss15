import os
from sklearn import svm
from sets import Set

#The list of words that will be the attributes
#Add inside the words of your choice (lower case). Some examples are already inserted     
attributes=Set(['million'])

#Insert here the full paths of the 4 folders. Don't remove the r before ''
spamTrainPath = r'C:\Users\Administrator\Desktop\courses\SNLP\ex2\Ex2SuppMaterial\dataset\spam-train'   
nonSpamTrainPath = r"C:\Users\Administrator\Desktop\courses\SNLP\ex2\Ex2SuppMaterial\dataset\nonspam-train"   
spamTestPath = r'C:\Users\Administrator\Desktop\courses\SNLP\ex2\Ex2SuppMaterial\dataset\spam-test'   
nonSpamTestPath = r"C:\Users\Administrator\Desktop\courses\SNLP\ex2\Ex2SuppMaterial\dataset\nonspam-test"   

#create the training set. No need to change something
Xtrain=[]
Ytrain=[]

for filename in os.listdir(spamTrainPath):
    with open(spamTrainPath+'\\' +filename, 'r') as document:
        documentAsSet=Set()

        trainingPoint=[]
        for line in document:
            tokens = line.split()
            for token in tokens:
                documentAsSet.add(token.lower())
        for attribute in attributes:
            if attribute in documentAsSet:
                trainingPoint.append(1)
            else:
                trainingPoint.append(-1)
        Xtrain.append(trainingPoint)
        Ytrain.append(0)
 
for filename in os.listdir(nonSpamTrainPath):
    with open(nonSpamTrainPath+'\\' +filename, 'r') as document:
        documentAsSet=Set()
        trainingPoint=[]
        for line in document:
            tokens = line.split()
            for token in tokens:
                documentAsSet.add(token.lower())
        for attribute in attributes:
            if attribute in documentAsSet:
                trainingPoint.append(1)
            else:
                trainingPoint.append(-1)
        Xtrain.append(trainingPoint)
        Ytrain.append(1)

#Train the SVM 
clf = svm.SVC()
clf.fit(Xtrain, Ytrain)  

#create the test set. No need to change something
Xtest=[]
Ytest=[]

for filename in os.listdir(spamTestPath):
    with open(spamTestPath+'\\' +filename, 'r') as document:
        documentAsSet=Set()

        testPoint=[]
        for line in document:
            tokens = line.split()
            for token in tokens:
                documentAsSet.add(token.lower())
        for attribute in attributes:
            if attribute in documentAsSet:
                testPoint.append(1)
            else:
                testPoint.append(-1)
        Xtest.append(testPoint)
        Ytest.append(0)
 
for filename in os.listdir(nonSpamTestPath):
    with open(nonSpamTestPath+'\\' +filename, 'r') as document:
        documentAsSet=Set()

        testPoint=[]
        for line in document:
            tokens = line.split()
            for token in tokens:
                documentAsSet.add(token.lower())
        for attribute in attributes:
            if attribute in documentAsSet:
                testPoint.append(1)
            else:
                testPoint.append(-1)
        Xtest.append(testPoint)
        Ytest.append(1)
 
 

#predict      
predictions=clf.predict(Xtest)
sumOfErrors=0
for i in range(len(Xtest)):
    if(predictions[i]!=Ytest[i]):
        sumOfErrors+=1

print 'Misclassifications: ', sumOfErrors,'/',len(Xtest)

