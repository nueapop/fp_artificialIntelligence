#%%
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

dataset = pd.read_csv("data\dataset.csv", encoding="utf8")
print(f'dataset\'s column: \n {dataset.columns}')
categorical_columns = ['gender', 'ever_married', 'Residence_type', 'work_type', 'smoking_status']

for category in categorical_columns:
    dataset[category] = dataset[category].astype('category').cat.codes.values

feature = 'stroke'

ax = dataset['' + feature + ''].value_counts()[:10].plot(kind='bar',
                                                         figsize=(16, 12),
                                                         color='cadetblue', linewidth=0.5)
plt.grid(b=True, which='major', axis='both', c='0.95', ls='-', linewidth=1.0, zorder=0)
plt.xlabel('state of ' + feature + '', fontsize=18)
plt.xticks(rotation=45, fontsize=14)
plt.ylabel('Frequency of ' + feature + '', fontsize=18)
plt.title('The Chart of ' + feature + '\'s Top Ten ', fontsize=18)
plt.show()

# model = ols(
#     'stroke ~ C(gender) + C(ever_married)  + C(work_type)  + C(smoking_status)  + C(work_type) + (age) + (hypertension) + (heart_disease) + (avg_glucose_level)',
#     data=dataset).fit()
# # model = ols('Ampere ~ C(Consuming):C(TimeOfDay)+ C(Target):C(TimeOfDay)', data=d).fit()
# # model = ols('Ampere ~ C(Consuming) + C(Target) + C(In_feellike) + C(TimeOfDay) + C(Target):C(TimeOfDay)+ C(Consuming):C(TimeOfDay)', data=d).fit()
# # model = ols('InTemp ~ C(Consuming) + C(Target) + C(In_feellike) + C(TimeOfDay)+ C(Target):C(In_feellike) + C(Target):C(TimeOfDay)+ C(In_feellike):C(TimeOfDay)', data=d).fit()
# anova_table = sm.stats.anova_lm(model, typ=3)
# print(anova_table)
# for i in range(len(anova_table)):
#     print(f'p value of {anova_table.index[i]} is {np.format_float_positional(anova_table.values[i][3])}')
#
# X = dataset.iloc[:, 0:10]
# print(f'X sample: \n {X.head().to_string()}')

# Y = dataset.stroke
# print(f'Y sample: \n {Y.head().to_string()}')
# #
# validation_size = 0.4
# seed = 1
# X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
# #
# # Test options and evaluation metric
# scoring = 'accuracy'
#
# Spot Check Algorithms
# models = []

# models.append(('DecisionTree', DecisionTreeClassifier()))
# models.append(('KNN', KNeighborsClassifier()))
# #
# # mlp = MLPClassifier(solver='adam', activation='relu', max_iter=300, verbose=50, learning_rate_init=.001, hidden_layer_sizes=(400, 200, 100))
# # # mlp = MLPClassifier(solver='adam', activation='relu', max_iter=500, verbose=50, learning_rate_init=.001, hidden_layer_sizes=800)
# # # models.append(('NN', mlp))
# models.append(('SVM', SVC(kernel='linear')))
#
# # evaluate each model in turn
# results = []
# names = []
# print("Evaluation - Cross Validation")
# for name, model in models:
#     kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
#     history = model.fit(X_train, Y_train)

#     # evaluate the model
#     cv_results_train = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
#     print('%s: %.3f (sd: %.3f)' % (name, cv_results_train.mean(), cv_results_train.std()))

#     predictions = model.predict(X_test)

#     print(name)
#     # arrayTarget = {0: 'not stroke', 1: 'stroke', 2: 'System Overwork', 3: 'System Work'}
#     arrayTarget = {0: 'not stroke', 1: 'stroke'}
#     print(arrayTarget)
#     from sklearn.metrics import classification_report
#     from sklearn.metrics import confusion_matrix
#     from sklearn.metrics import accuracy_score
#     from sklearn.metrics import f1_score, precision_score, recall_score

#     print("F1-score: ", f1_score(Y_test, predictions, average=None))
#     print("Precision: ", precision_score(Y_test, predictions, average=None))
#     print("Recall: ", recall_score(Y_test, predictions, average=None))
#     print("Confusion_matrix: \n", confusion_matrix(Y_test, predictions))
#     print("Classification_report: \n", classification_report(Y_test, predictions))
#     print("Accuracy_score: \n", accuracy_score(Y_test, predictions))
#     print()

# test = SelectKBest(score_func=chi2, k=5)
# features = test.fit_transform(X,Y)

# # finding selected column names
# feature_idx = test.get_support(indices=True)
# feature_names = dataset.columns[feature_idx]
# print(feature_names)
# %%
