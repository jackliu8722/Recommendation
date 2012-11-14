'''
Created on 2012-11-13

@author: jackliu
'''
import math
from basecf import BaseCF

class ItemBasedCF(BaseCF):
    def __init__(self,datafile):
        BaseCF.__init__(self, datafile)
    def itemSimilarity(self,train = None):
        train = train or self.traindata
        items_count = dict()
        self.itemSim = dict()
        N = dict()
        for u ,items in train.items():
            for item in items:
                N.setdefault(item,0)
                N[item] += 1
                items_count.setdefault(item,{})
                for j in items:
                    if item == j:continue
                    items_count[item].setdefault(j,0)
                    items_count[item][j] += 1
        for i,related_item in items_count.items():
            self.itemSim.setdefault(i,{})
            for j ,cij in related_item.items():
                self.itemSim[i][j] = cij / math.sqrt(N[i] * N[j] * 1.0)
    def recommend(self,user,train = None, k = 8,nitem = -1):
        rank = dict()
        train = train or self.traindata
        ru = train[user]
        for i,pi in ru.items():
            for j ,wj in sorted(self.itemSim[i].items(),key = lambda x :x[1],reverse = True)[0:k]:
                if j in ru:continue
                rank.setdefault(j,0)
                rank[j] += wj
        return dict(sorted(rank.items(),key = lambda x : x[1],reverse = True)[0:nitem])
def testItemBasedCF():
    cf  =  ItemBasedCF('u.data')
    cf.itemSimilarity()
    print "%3s%20s%20s%20s%20s" % ('K',"recall",'precision','coverage','popularity')
    for k in [5,10,20,40,80,160]:
        recall,precision = cf.recallAndPrecision( k = k)
        coverage = cf.coverage(k = k)
        popularity = cf.popularity(k = k)
        print "%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k,recall * 100,precision * 100,coverage * 100,popularity)
if __name__ == "__main__":
    testItemBasedCF()