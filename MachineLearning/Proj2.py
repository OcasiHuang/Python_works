"""
Input: No input is needed, just use the Makefile and type "make all" :)
Output: Will display the graph of correlating matrix / pair plot / prediction graph, along with the accuracy, best prediction parameters used and method of ML used.
"""
"""
Problem 1 & 2:
Based on our statistics, the parameters mostly related to our result(a1p2) are dest, thal, nmvcf, eia, mhr, opst and cpt as the factors that might help us to predict whether the heart disease is presented.
(Which index is (2,7,8,9,10,11,12))

The best result can be achieved under this condition is

Final result for top 7 correlated factors is:
[0.6172839506172839, 0.837037037037037] [7, 9] 2

Which mean accuracy for training data is 0.62, for a combined accuracy 0.84
The 2 parameter used is mhr and opst, the method used is random forest classifier

Problem 3:
I tried to take two parameters from the tuple of most correlated factors and analysis the best combination.

According to the table above, we would choose thal, nmvcf, eia, mhr, opst and cpt as the factors that might help us to predict whether the heart disease is presented.
(Which index is the same set as previous problem)

The best result can be achieved under this condition is

Final result for top 7 correlated factors is:
[0.4065934065934066, 0.759075907590759] [7, 9] 2

Which mean accuracy for training data is only 0.41, for a combined accuracy 0.76
The 2 parameter used is mhr and opst, the method used is random forest classifier. Which are just the same as previous problem.

"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import cm as cm
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn import datasets
## custom import
from plot_decision_region import plot_decision_regions 

## create covariance for dataframes, reference from lecture code
def mosthighlycorrelated(mydataframe, numtoreport): 
# find the correlations 
    cormatrix = mydataframe.corr() 
# set the correlations on the diagonal or lower triangle to zero, 
# so they will not be reported as the highest ones: 
    cormatrix *= np.tri(*cormatrix.values.shape, k=-1).T 
# find the top n correlations 
    cormatrix = cormatrix.stack() 
    cormatrix = cormatrix.reindex(cormatrix.abs().sort_values(ascending=False).index).reset_index() 
# assign human-friendly names 
    cormatrix.columns = ["FirstVariable", "SecondVariable", "Correlation"] 
    return cormatrix.head(numtoreport)

## Covariance matrix, reference from lecture code
def correl_matrix(X,cols):
    fig = plt.figure(figsize=(7,7), dpi=100)
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet',30)
    cax = ax1.imshow(np.abs(X.corr()),interpolation='nearest',cmap=cmap)
##    ax1.set_xticks(major_ticks)
    major_ticks = np.arange(0,len(cols),1)
    ax1.set_xticks(major_ticks)
    ax1.set_yticks(major_ticks)
    ax1.grid(True,which='both',axis='both')
##    plt.aspect('equal')
    plt.title('Correlation Matrix')
    labels = cols
    ax1.set_xticklabels(labels,fontsize=9)
    ax1.set_yticklabels(labels,fontsize=12)
    fig.colorbar(cax, ticks=[-0.4,-0.25,-.1,0,0.1,.25,.5,.75,1])
    plt.show()
    return(1)

## make pair plots, reference from lecture code
def pairplotting(df):
    sns.set(style='whitegrid', context='notebook')
    cols = df.columns
    sns.pairplot(df[cols],size=2.5)
    plt.title('Pair Plot of Most Related Factors')
    plt.show()
## this creates a dataframe similar to a dictionary
## a data frame can be constructed from a dictionary
## https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html

"""
Part 1
"""
## read argument as the testcase
testcase = sys.argv[1]

## define test set based on argument
if testcase == "2":
    heart = pd.read_csv('heart2_.csv')
    test_data_percentage = 0.3
else:
    heart = pd.read_csv('heart1.csv')
    test_data_percentage = 0.3

## Identify Null values
print(' Identify Null Values ')
print(heart.apply(lambda x: sum(x.isnull()),axis=0) )

##  descriptive statistics
print(' Descriptive Statistics ')
print(heart.describe())

## most highly correlated lists
print("Most Highly Correlated")
print(mosthighlycorrelated(heart,15))

## heat plot of covariance
print(' Covariance Matrix ')
correl_matrix(heart.iloc[:,0:14],heart.columns[0:14])

## Pair plotting, since the original pairplot is too large, I onlt show the correlation of the 6 most related factors and also the a1p2
print(' Pair plotting ')
##heart_plot = pd.concat([heart.iloc[:,2],heart.iloc[:,7:10],heart.iloc[:,11:14]], axis = 1)
heart_plot = pd.concat([heart.iloc[:,2],heart.iloc[:,7:14]], axis = 1)
pairplotting(heart_plot)
##pairplotting(heart)

"""
A statistic about data quality
"""
cnt = [0]*5
for i in heart.iloc[:,13].values:
    cnt[i] += 1
## Showing summary of the result (a1p2) for anaysis
print("Samples for the result",0,"is",cnt[0])
print("Samples for the result",1,"is",cnt[1])
print("Samples for the result",2,"is",cnt[2])
print("Samples for the result",3,"is",cnt[3])
print("Samples for the result",4,"is",cnt[4])

if testcase == "2":
    zero_cnt = 50
    i = len(heart)
    i_index = 0
    while i > 0 or zero_cnt > 0:
        if heart.iloc[i_index][13] == 0:
            heart = heart.drop(i_index+50-zero_cnt)
            zero_cnt -= 1
        else:
            i_index += 1
        i -= 1
"""
Part 2 
"""

candidate_factor = (2,7,8,9,10,11,12) ## Narrowing the factor to be use with by choosing the 7 most highly-related factors
##candidate_factor = tuple(range(13))
temp_max = [0,0]
temp_max_factor = [0,0]
ppn = [0]*7

## Use for loop to find the two parameters with the best result 
for i,ival in enumerate(candidate_factor):
    for j,jval in enumerate(candidate_factor[i+1:]):

        ## split the problem into train and test
        from sklearn.cross_validation import train_test_split
        col_nu = int(len(heart.columns))
        X = pd.concat([heart.iloc[:,ival],heart.iloc[:,jval]], axis = 1).values ## To obtain a new dataframe based on i and j
        ##X = pd.concat([heart.iloc[:,2],heart.iloc[:,7:10],heart.iloc[:,11:13]], axis = 1).values
        y = heart.iloc[:,col_nu-1].values
        ##X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_data_percentage,random_state=0)
        
        ## scale X
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        sc.fit(X_train)
        X_train_std = sc.transform(X_train)
        X_test_std = sc.transform(X_test)
        
        ## perceptron linear
        from sklearn.linear_model import Perceptron
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.svm import SVC
        
        def TrainNAnalysis(ppn):
            ppn.fit(X_train_std, y_train)
            ##print("Accuracy in training: ", ppn.score(X_train_std,y_train))
            
            ##print('Number in test ',len(y_test))
            y_pred = ppn.predict(X_test_std)
            ##print('Misclassified samples: %d' % (y_test != y_pred).sum())
            
            from sklearn.metrics import accuracy_score
            ##print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
            
            X_combined_std = np.vstack((X_train_std, X_test_std))
            y_combined = np.hstack((y_train, y_test))
            ##print('Number in combined ',len(y_combined))
            
            y_combined_pred = ppn.predict(X_combined_std)
            ##print('Misclassified combined samples: %d' % (y_combined != y_combined_pred).sum())
            
            from sklearn.metrics import accuracy_score
            ##print('Combined Accuracy: %.2f' % accuracy_score(y_combined, y_combined_pred))
        
            ##return float(accuracy_score(y_test, y_pred))
            return [float(accuracy_score(y_test, y_pred)),accuracy_score(y_combined, y_combined_pred)]
        
        ## Not sure which method should obtain better result, thus I include and use all of them and choose the one with the best accuracy 
        ppn[0] = Perceptron(max_iter=10, tol=1e-4, eta0=0.001, fit_intercept=True, random_state=0, verbose=True)
        ppn[1] = LogisticRegression(penalty='l2',max_iter=100, tol=1e-4, C=10.0, verbose=True, random_state=0)
        ppn[2] = RandomForestClassifier(criterion='entropy', n_estimators=10 ,random_state=1, n_jobs=2)
        ppn[3] = KNeighborsClassifier(n_neighbors=5,p=2,metric='minkowski')
        ppn[4] = DecisionTreeClassifier(criterion='entropy',max_depth=3 ,random_state=0)
        ppn[5] = SVC(kernel='linear', C=100.0, random_state=0)
        ppn[6] = SVC(kernel='rbf', tol=1e-3, random_state=0, gamma=0.2 , C=100.0, verbose=True)
        
        Accuracy = [TrainNAnalysis(ppn[0]),TrainNAnalysis(ppn[1]),TrainNAnalysis(ppn[2]),TrainNAnalysis(ppn[3]),TrainNAnalysis(ppn[4]),TrainNAnalysis(ppn[5]),TrainNAnalysis(ppn[6])]
        #Accuracy = [TrainNAnalysis(ppn[1]),TrainNAnalysis(ppn[2])] 
        
        ##tmp_max = max(Accuracy,key=lambda x:x[0]) ## Find the method with best Accuracy score
        tmp_max = max(Accuracy,key=lambda x:x[1]) ## Find the method with best Combined Accuracy score
        tmp_index = Accuracy.index(tmp_max) ## Also show the best method
        ##if tmp_max[0] > temp_max[0]: ## To record the parameters used and the ML method
        if tmp_max[1] > temp_max[1]:
            temp_index = tmp_index
            temp_max = tmp_max
            temp_max_factor = [ival,jval]
       
        ## Plot graph for prediction for the specific result concluded from previous experiment based on this Python code
        ##if ([ival,jval] == [2,11] and testcase == "2") or ([ival,jval] == [11,12] and testcase != "2"):
        if ([ival,jval] == [7,9] and testcase == "2") or ([ival,jval] == [7,9] and testcase != "2"):
            for h in range(len(Accuracy)):
                print("Accuracy of [7,9] for method",h,"is :",Accuracy[h])
            X_combined_std = np.vstack((X_train_std, X_test_std))
            y_combined = np.hstack((y_train, y_test))
            plot_decision_regions(X=X_combined_std, y=y_combined,classifier=ppn[tmp_index], test_idx=range(105,150))
            ##plot_decision_regions(X=X_combined_std, y=y_combined,classifier=ppn[1], test_idx=range(105,150))## Plot linear regression decision graph
            plt.title('Plot of Prediction of the Best Accuracy')
            if testcase == "2":
                plt.xlabel('Maximum Heartrate Achieved')
                plt.ylabel('ST Depression Induced by Exercise Related to Rest')
                ##plt.xlabel('Chest Pain Type')
                ##plt.ylabel('Number of Major Vessels Colored by Flourosopy')
            else:
                plt.xlabel('Maximum Heartrate Achieved')
                plt.ylabel('ST Depression Induced by Exercise Related to Rest')
                ##plt.xlabel('Number of Major Vessels Colored by Flourosopy')
                ##plt.ylabel('Thal')

            plt.legend(loc='upper left')
            plt.show()

## Print the result, providing information as [Best Accuracy, Combined Accuracy in this case], Index of parameter chosen, Method used
print("Final result for top 7 correlated factors is:")
print(temp_max,temp_max_factor,temp_index)
print(len(heart))



