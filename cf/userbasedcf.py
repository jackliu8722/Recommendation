'''
Created on 2012-11-8

@author: jackliu
'''

import random
import math
from basecf import BaseCF
class UserBasedCF(BaseCF):
    def __init__(self,datafile = None):
        BaseCF.__init__(self, datafile)
    def userSimilarity(self,train = None):
        """
        One method of getting user similarity matrix
        """
        train = train or self.traindata
        self.userSim = dict()
        for u in train.keys():
            for v in train.keys():
                if u == v:
                    continue
                self.userSim.setdefault(u,{})
                self.userSim[u][v] = len(set(train[u].keys()) & set(train[v].keys()))
                self.userSim[u][v] /=math.sqrt(len(train[u]) * len(train[v]) *1.0)
    def userSimilarityBest(self,train = None):
        """
        the other method of getting user similarity which is better than above
        you can get the method on page 46
        In this experiment, we use this method
        """
        train = train or self.traindata
        self.userSim = dict()
        item_users = dict()
        for u,item in train.items():
            for i in item.keys():
                item_users.setdefault(i,set())
                item_users[i].add(u)
        user_item_count = dict()
        count = dict()
        for item,users in item_users.items():
            for u in users:
                user_item_count.setdefault(u,0)
                user_item_count[u] += 1
                for v in users:
                    if u == v:continue
                    count.setdefault(u,{})
                    count[u].setdefault(v,0)
                    count[u][v] += 1
        for u ,related_users in count.items():
            self.userSim.setdefault(u,dict())
            for v, cuv in related_users.items():
                self.userSim[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v] * 1.0)

    def userSimilarityIIF(self,train = None):
        """
        the other method of getting user similarity which is better than above
        you can get the method on page 49
        """
        train = train or self.traindata
        self.userSim = dict()
        item_users = dict()
        for u,item in train.items():
            for i in item.keys():
                item_users.setdefault(i,set())
                item_users[i].add(u)
        user_item_count = dict()
        count = dict()
        for item,users in item_users.items():
            for u in users:
                user_item_count.setdefault(u,0)
                user_item_count[u] += 1
                for v in users:
                    if u == v:continue
                    count.setdefault(u,{})
                    count[u].setdefault(v,0)
                    count[u][v] += 1/ math.log(1+len(users))
        for u ,related_users in count.items():
            self.userSim.setdefault(u,dict())
            for v, cuv in related_users.items():
                self.userSim[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v] * 1.0)

    def recommend(self,user,train = None,k = 8,nitem = 40):
        train = train or self.traindata
        rank = dict()
        interacted_items = train.get(user,{})
        for v ,wuv in sorted(self.userSim[user].items(),key = lambda x : x[1],reverse = True)[0:k]:
            for i , rvi in train[v].items():
                if i in interacted_items:
                    continue
                rank.setdefault(i,0)
                rank[i] += wuv
        return dict(sorted(rank.items(),key = lambda x :x[1],reverse = True)[0:nitem])
    
    
def testRecommend():
    ubcf = UserBasedCF('u.data')
    ubcf.readData()
    ubcf.splitData(4,100)
    ubcf.userSimilarity()
    user = "345"
    rank = ubcf.recommend(user,k = 3)
    for i,rvi in rank.items():
        
        items = ubcf.testdata.get(user,{})
        record = items.get(i,0)
        print "%5s: %.4f--%.4f" %(i,rvi,record)
def testUserBasedCF():
    cf  =  UserBasedCF('u.data')
    cf.userSimilarityBest()
    print "%3s%20s%20s%20s%20s" % ('K',"recall",'precision','coverage','popularity')
    for k in [5,10,20,40,80,160]:
        recall,precision = cf.recallAndPrecision( k = k)
        coverage = cf.coverage(k = k)
        popularity = cf.popularity(k = k)
        print "%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k,recall * 100,precision * 100,coverage * 100,popularity)
def testUserBasedIIF():
    cf  =  UserBasedCF('u.data')
    k = 80
    print "%20s%20s%20s%20s%20s" % ('Method',"recall",'precision','coverage','popularity')
    cf.userSimilarityBest()
    recall,precision = cf.recallAndPrecision( k = k)
    coverage = cf.coverage(k = k)
    popularity = cf.popularity(k = k)
    print "%20s%19.3f%%%19.3f%%%19.3f%%%20.3f" % ("UserCF",recall * 100,precision * 100,coverage * 100,popularity)
    cf.userSimilarityIIF()
    recall,precision = cf.recallAndPrecision( k = k)
    coverage = cf.coverage(k = k)
    popularity = cf.popularity(k = k)
    print "%20s%19.3f%%%19.3f%%%19.3f%%%20.3f" % ("UserIIF",recall * 100,precision * 100,coverage * 100,popularity)
if __name__ == "__main__":
    testUserBasedIIF()
        