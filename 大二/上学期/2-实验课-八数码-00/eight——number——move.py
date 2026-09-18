import queue

state=[]
enqueued={}#log the state have judged

#calculate the reverse number
def reverse_number(state):
    state.remove('0')
    re_numbers=0
    for current in state:
        current_index=state.index(current)
        for after in state[current_index:]:
            if after>current:
                re_numbers+=1
        
    if re_numbers%2==0:
        return 0
    else:
        return 1
    
#judge the question has slove or not by reserse,if same,it can be sloved;    
def is_solved(start,end):
    start_number=reverse_number(start)
    end_number=reverse_number(end)
    if start==end:
        print("start is the goal!")
        exit(0)
    elif start_number==end_number:
        print("can't find solution!")
        exit(0)
    #the case like up stop right now
        
#judge     
def is_visited(state):
    state_key=''.jion(state)
    if enqueued.get(state_key):
        return True
    else:
        enqueued[state_key]=1
        return False
    
def find_next_state(state):
    global Open,creat_point
    zero_index=state.index('0')
    if zero_index-3>=0:
        temp=state.copy()
        #exchange the zero with up
        temp[zero_index],temp[zero_index-3]=temp[zero_index-3],temp[zero_index]
        if not is_visited(temp[:9]):
            temp.append("up")
            Open.put(temp)
            creat_point+=1
        
    if zero_index+3<=8:
        temp=state.copy()
        #exchange the zero with down
        temp[zero_index],temp[zero_index-3]=temp[zero_index-3],temp[zero_index]
        if not is_visited(temp[:9]):
            temp.append("down")
            Open.put(temp)
            creat_point+=1
        
    if zero_index%3!=0:
        temp=state.copy()
        #exchange the zero with left
        temp[zero_index],temp[zero_index-3]=temp[zero_index-3],temp[zero_index]
        if not is_visited(temp[:9]):
            temp.append("left")
            Open.put(temp)
            creat_point+=1
    if (zero_index+1)%3!=0:
        temp=state.copy()
        #exchange the zero with right
        temp[zero_index],temp[zero_index-3]=temp[zero_index-3],temp[zero_index]
        if not is_visited(temp[:9]):
            temp.append("right")
            Open.put(temp)
            creat_point+=1
 
def bfs(start,goal):

    is_solved(start.copy(),goal.copy())  #avoid changing original state
    Open=queue.Queue()
    Open.put(start)
    enqueued[''.join(start)]=1    #change into string and,key's size is 1

    while True:
        if Open.empty():
            print("can't find")
            exit(0)
        open_head=Open.get()
        if open_head[:9]==goal:
            print("succed")
            print("the way to get goal is: ")
            for i in open_head[9:]:
                print(i,end='->')
            exit(0)
        find_next_state(open_head.copy())






start=list(input("please input initial state: ").split())
goal=list(input("please input goal state: ").split()) 
bfs(start,goal)
    




