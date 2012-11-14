'''
Created on 2012-11-13

@author: jackliu
'''
import random
import math
class NotImplementError(Exception):
    pass
class BaseCF:
    def __init__(self,datafile = None):
        self.datafile = datafile
        self.readData()
        self.splitData(3,47)
    def readData(self,datafile = None):
        """
        read the data from the data file which is a data set
        """
        self.datafile = datafile or self.datafile
        self.data = []
        for line in open(self.datafile):
            userid,itemid,record,_ = line.split()
            self.data.append((userid,itemid,int(record)))
    def splitData(self,k,seed,data=None,M = 8):
        """
        split the data set
        testdata is a test data set
        traindata is a train set 
        test data set / train data set is 1:M-1
        """
        self.testdata = {}
        self.traindata = {}
        data = data or self.data
        random.seed(seed)
        for user,item, record in self.data:
            if random.randint(0,M) == k:
                self.testdata.setdefault(user,{})
                self.testdata[user][item] = record 
            else:
                self.traindata.setdefault(user,{})
                self.traindata[user][item] = record
    def recallAndPrecision(self,train = None,test = None,k = 8,nitem = 10):
        """
        Get the recall and precision, the method you want to know is listed 
        in the page 43
        """
        train  = train or self.traindata
        test = test or self.testdata
        hit = 0
        recall = 0
        precision = 0
        for user in train.keys():
            tu = test.get(user,{})
            rank = self.recommend(user, train = train,k = k,nitem = nitem) 
            for item,_ in rank.items():
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += nitem
        return (hit / (recall * 1.0),hit / (precision * 1.0))
    def coverage(self,train = None,test = None,k = 8,nitem = 10):
        train = train or self.traindata
        test = test or self.testdata
        recommend_items = set()
        all_items  = set()
        for user in train.keys():
            for item in train[user].keys():
                all_items.add(item)
            rank = self.recommend(user, train, k = k, nitem = nitem)
            for item,_ in rank.items():
                recommend_items.add(item)
        return len(recommend_items) / (len(all_items) * 1.0)
    def popularity(self,train = None,test = None,k = 8,nitem = 10):
        """
        Get the popularity
        the algorithm on page 44
        """
        train = train or self.traindata
        test = test or self.testdata
        item_popularity = dict()
        for user ,items in train.items():
            for item in items.keys():
                item_popularity.setdefault(item,0)
                item_popularity[item] += 1
        ret = 0
        n = 0
        for user in train.keys():
            rank = self.recommend(user, train, k = k, nitem = nitem)
            for item ,_ in rank.items():
                ret += math.log(1+item_popularity[item])
                n += 1
        return ret / (n * 1.0)