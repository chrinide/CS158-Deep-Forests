import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest

from gcForest.GCForest import gcForest

from load_data import load_data
from baseline import TitleFinder
from baseline_author import AuthorFinder

def main():
    if len(sys.argv) < 2:
        print("Please specify a model to run")
        sys.exit(1)

    X,y,tfidf = load_data()

    # feature selection to make the problem tractable for gcforest
    fs = SelectKBest(k=100)
    X = fs.fit_transform(X,y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=1337, stratify=y)
    
    model = None
    if sys.argv[1] == "baseline":
        model = TitleFinder(tfidf.get_feature_names())
    elif sys.argv[1] == "author":
        model = AuthorFinder(tfidf.get_feature_names()) 
    elif sys.argv[1] == "forest":
        model = RandomForestClassifier()
    elif sys.argv[1] == "deepforest":
        model = gcForest(shape_1X=100)

    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)   
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

if __name__ == '__main__':
    main()