import numpy as np
import time  
import matplotlib.pyplot as plt
e=2.718

class BernoulliBandit():
    def __init__(self, K, probas=None):        #n为摇臂的个数，probas为每个摇臂获得奖励的概率
        assert probas is None or len(probas) == K
        self.K = K
        if probas is None:
            np.random.seed(int(time.time()))
            self.probas = [np.random.random() for _ in range(self.K)]
            self.best_proba = max(self.probas)
        else:
            self.probas = probas
            self.best_proba = max(self.probas)
    def generate_reward(self, i):
    # The player selected the i-th machine.
        if np.random.random() < self.probas[i]:
            return 1     #满足发生的概率，就获得奖励1
        else:
            return 0
        
#参数K：摇臂个数，T：试验次数，epsilon：探索概率,r:累积奖励,Q:每个摇臂的估计值,count:每个摇臂的选择次数
def greedy_e_strategy(bandit,K,T,epsilon,r,Q,count):
        r=0
        y=[]
        regret=[]
        for t in range(1,T+1):
            if np.random.random()<epsilon:
                j=np.random.randint(0,K)
            else:
                j=np.argmax(Q)
            reward=bandit.generate_reward(j)
            r+=reward
            y.append(r/t)
            Q[j]=(Q[j]*count[j]+reward)/(count[j]+1)
            regret.append(bandit.best_proba-r/T)
            count[j]+=1
        print("\n贪心-ε策略：\n")
        print("累积奖励：",r)
        print("每个摇臂选择次数： ",count)
        print("每个摇臂的估计值： ",Q)
        print("每个摇臂真实获奖的概率： ",bandit.probas)
        return y,regret

def greedy_strategy(bandit,T,r,Q,count):
        r=0
        y=[]
        regret=[]
        for t in range(1,T+1):
            j=np.argmax(Q)
            reward=bandit.generate_reward(j)
            r+=reward
            y.append(r/t)
            Q[j]=(Q[j]*count[j]+reward)/(count[j]+1)
            regret.append(bandit.best_proba-r/T)   
            count[j]+=1
        print("\n贪心策略:\n")
        print("累积奖励：",r)
        print("每个摇臂选择次数： ",count)
        print("每个摇臂的估计值： ",Q)
        print("每个摇臂真实获奖的概率： ",bandit.probas)
        return y,regret

def softmax(bandit,K,T,epsilon,Q,r,count):
    r=0
    y=[]
    regret=[]
    property_list=np.zeros(K)
    for t in range(1,T+1):
        Probability_accumulation=0
        total_accumulation=sum(pow(e,Q[i]/epsilon) for i in range(K))
        random_value=np.random.random()
        for i in range(K):
            property_list[i]=pow(e,Q[i]/epsilon)/total_accumulation
            Probability_accumulation+=property_list[i]
            if random_value<Probability_accumulation :
                j=i
                break
        reward=bandit.generate_reward(j)
        r+=reward
        y.append(r/t)
        Q[j]=(Q[j]*count[j]+reward)/(count[j]+1)
        regret.append(bandit.best_proba-r/T)
        count[j]+=1
    print("\nsoftmax:\n")
    print("累积奖励：",r)
    print("每个摇臂选择次数： ",count)
    print("每个摇臂的估计值： ",Q)
    print("每个摇臂真实获奖的概率： ",bandit.probas)
    return y,regret

fig,axs=plt.subplots(1,3,figsize=(10,5))
fig1,axs1=plt.subplots(1,3,figsize=(10,5))
k_=5
T_=3000  
bandit = BernoulliBandit(K=k_)
y_ge,regret_ge=greedy_e_strategy(bandit,K=k_,T=T_,epsilon=0.1,r=0,Q=np.zeros(k_),count=np.zeros(k_))
x=[i for i in range(0,T_+1)]
regret_ge
y_ge=[0]+y_ge
axs1[0].plot(x[1:],regret_ge)
axs1[0].set_xlabel('round')
axs1[0].set_ylabel('regret')
axs1[0].set_title('greedy-epsilon strategy')
axs[0].plot(x,y_ge)
axs[0].set_xlabel('round')
axs[0].set_ylabel('average reward')
axs[0].set_title('greedy-epsilon strategy')

y_g,regret_g=greedy_strategy(bandit,T=T_,r=0,Q=np.zeros(k_),count=np.zeros(k_))
x=[i for i in range(0,T_+1)]
regret_g=regret_g
y_g=[0]+y_g
axs1[1].plot(x[1:],regret_g)
axs1[1].set_xlabel('round')
axs1[1].set_ylabel('regret')
axs1[1].set_title('greedy strategy')
axs[1].plot(x,y_g)
axs[1].set_xlabel('round')
axs[1].set_ylabel('average reward')
axs[1].set_title('greedy strategy')

y_sf,regret_sf=softmax(bandit,K=k_,T=T_,epsilon=0.1,r=0,Q=np.zeros(k_),count=np.zeros(k_))
x=[i for i in range(0,T_+1)]
regret_sf=regret_sf
y_sf=[0]+y_sf
axs1[2].plot(x[1:],regret_sf)
axs1[2].set_xlabel('round')
axs1[2].set_ylabel('regret')
axs1[2].set_title('softmax strategy')
axs[2].plot(x,y_sf)
axs[2].set_xlabel('round')
axs[2].set_ylabel('average reward')
axs[2].set_title('softmax strategy')

plt.suptitle("K:%d   T:%d  "%(k_,T_))
plt.show()
