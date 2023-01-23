#HELPER FUNCTIONS
import math

def calculate_time(x,v,i,T):     #O(1) time
    #The following function calculates time in which collision will take place
    #If time is non-positive or infinite, then it makes it 2T i.e. 2 times the maximum time valid for collision.
    x_i = x[i]
    x_i_1 = x[i+1]
    v_i = v[i]
    v_i_1 = v[i+1]
    if v_i == v_i_1:
        T_i = 2*T
    else:
        T_i = (x_i_1-x_i)/(v_i-v_i_1)
    if T_i <= 0:
        T_i = 2*T
    return T_i

def calculate_time_all(x,v,T):    #O(len(x)) time
    #The following function calculates the time for all the particles given and retruns a list where T_i represents the collision time between ith and (i+1)th particle
    T_i = []
    for i in range (0,len(x)-1):
        T_i.append((calculate_time(x,v,i,T),i))
    return T_i

def calculate_position(x,v,i,t):    #O(1) time
    #The function calculates the position of collision between the ith and (i+1)th particle.
    x_i = x[i]
    v_i = v[i]
    return x_i + t*v_i

def update_velocity(M,v,i):           #O(1) time
    #The function calculates the velocity of the particles after collision , updates the list of velocities of the particles and returns it
    u1 = v[i]
    u2 = v[i+1]
    m1 = M[i]
    m2 = M[i+1]
    v1 = ((m1-m2)/(m1+m2))*u1 + ((2*m2)/(m1+m2))*u2
    v2 = ((2*m1)/(m1+m2))*u1 + ((m2-m1)/(m1+m2))*u2
    v[i] = v1
    v[i+1] = v2
    return v

def update_location(x,x_updated,i):    #O(1)
    #The function updates the position of the particles in the position array to the new position passed in the function
    x[i] = x_updated
    x[i+1] = x_updated
    return x

#IMPLEMENTING A HEAP USING ALMOST COMPLETE BINARY TREE
class AlmostCompleteBinaryTree:

    def __init__(self):
        self.keys = []
        self.num_nodes = 0
        self.height = 0

    def children(self,i):       #O(1)  time
        #This function returns the left and right child as a tuple and the child is None if it doesnt exist
        n = len(self.keys)
        if ((2*i)+1) >= n:
            left_child = None
        else:
            left_child = self.keys[(2*i)+1] 
        if ((2*i)+2) >= n:
            right_child = None
        else:
            right_child = self.keys[(2*i)+2] 
        return (left_child,right_child)
        
    def parent(self,i):               #O(1) time
        #This function returns the parent and None if it doesnt exist
        if i == 0:
            return None
        return self.keys[(i-1)//2]

    def add(self,e):                  #O(1) time
        #This function adds an element to the almost complete binary tree
        self.keys.append(e)
        self.num_nodes += 1
        self.height = int(math.log2(self.num_nodes+1)) + 1

class MinHeap:

    def __init__(self,keys):
        Heap_initial = AlmostCompleteBinaryTree()   #initiates a heap using an almost complete binary tree
        indices = []
        for i in range (0,len(keys)):           #O(len(keys))
            Heap_initial.add(keys[i])
            indices.append(i)
        self.Heap_initial = Heap_initial
        self.track_indices = indices            #an attribute defined from the perspective of main function which keeps track of the position of the element in MinHeap, w.r.t added initially in the Almost Complete Binary tree

    def heapdown(self,u,i):                     #O(log(number of elements in heap))
        u_i = u[0]
        children = self.Heap_initial.children(i)
         
        while ((children[0] != None) and u_i >= children[0][0]) or ((children[1] != None) and (u_i >= children[1][0])):
            if (children[1] == None or children[0][0] < children[1][0] or (children[0][0] == children[1][0] and children[0][1] < children[1][1])) and (u_i > children[0][0] or u[1] > children[0][1]):
                self.track_indices[self.Heap_initial.keys[i][1]] = (2*i)+1
                self.track_indices[self.Heap_initial.keys[(2*i)+1][1]] = i
                self.Heap_initial.keys[i],self.Heap_initial.keys[(2*i)+1] = self.Heap_initial.keys[(2*i)+1],self.Heap_initial.keys[i]
                i = (2*i)+1 
                u_i = self.Heap_initial.keys[i][0]
                u = self.Heap_initial.keys[i]
            elif (children[1] != None and children[0][0] >= children[1][0]) and (u_i > children[1][0] or (u_i == children[1][0] and u[1] > children[1][1])):
                self.track_indices[self.Heap_initial.keys[i][1]] = (2*i)+2
                self.track_indices[self.Heap_initial.keys[(2*i)+2][1]] = i
                self.Heap_initial.keys[i],self.Heap_initial.keys[(2*i)+2] = self.Heap_initial.keys[(2*i)+2],self.Heap_initial.keys[i]
                i = (2*i)+2
                u_i = self.Heap_initial.keys[i][0]
                u = self.Heap_initial.keys[i]
            else:
                break
            children = self.Heap_initial.children(i)

    def construct_heap(self):                  #O(number of elements in heap)
        i = len(self.Heap_initial.keys) - 1
        while i >= 0:
            self.heapdown(self.Heap_initial.keys[i],i)
            i -= 1

    def heapup(self,u,i):                      #O(log(number of elements in heap))
        u_i = u[0]

        while self.Heap_initial.parent(i) != None and self.Heap_initial.parent(i)[0] >= u_i:
            if self.Heap_initial.parent(i)[0] > u_i or self.Heap_initial.parent(i)[1] > u[1]:
                self.track_indices[self.Heap_initial.keys[i][1]] = (i-1)//2
                self.track_indices[self.Heap_initial.keys[(i-1)//2][1]] = i
                self.Heap_initial.keys[i],self.Heap_initial.keys[(i-1)//2] = self.Heap_initial.keys[(i-1)//2],self.Heap_initial.keys[i]
            else:
                break
            i = (i-1)//2
            u_i = self.Heap_initial.keys[i][0]
            u = self.Heap_initial.keys[i]

    def change_key(self,u,i,x):                #chamges the key of element u in heap to x and then performs heap up or heapdown accordingly.
        x_i = u[0]
        self.Heap_initial.keys[i] = (x,u[1])
        
        if x_i > x:
            self.heapup(self.Heap_initial.keys[i],i)
        if x_i < x:
            self.heapdown(self.Heap_initial.keys[i],i)


#MAIN FUNCTION
def listCollisions(M, x, v, m, T): 
    n = len(M)

    list_of_collisions = []
    position_update_time = [0] * n    #O(n)                 #an array which keeps track of the time at which the position of ith particle is updated

    T_i = calculate_time_all(x, v, T)  # O(n) time          #calculating the time of collision between (i) and(i+1)th particle
    T_i_list = MinHeap(T_i)                                 #Initiating a heap of the above array
    T_i_list.construct_heap()  # O(n) time                  #Operating on heap to make it a min-heap

    time_passed = 0
    num_collisions = 0

    while (time_passed < T) and (num_collisions < m):  # O(m) 

        i = T_i_list.Heap_initial.keys[0][1]               #The index of the particle whose collision takes place with the particle after it
        if T_i_list.Heap_initial.keys[0][0] >= T:          #not counting collisions tsking place beyond time T
            break

        list_of_collisions.append((T_i_list.Heap_initial.keys[0][0], i, calculate_position(x, v, i, T_i_list.Heap_initial.keys[0][0] - position_update_time[i])))

        time_passed = T_i_list.Heap_initial.keys[0][0]

        x = update_location(x, calculate_position(x, v, i, T_i_list.Heap_initial.keys[0][0] - position_update_time[i]), i)  # O(1)
        position_update_time[i] = time_passed
        position_update_time[i + 1] = time_passed
        v = update_velocity(M, v, i)  # O(1)

        T_i_list.change_key(T_i_list.Heap_initial.keys[0], 0, 2 * T)       #O(logn)

        if i != 0:                     #updating the location of the (i-1)th particle along with updating the time updation of collision between (i-1)th and ith particle
            x[i - 1] = x[i - 1] + v[i - 1] * (time_passed - position_update_time[i - 1])
            position_update_time[i - 1] = time_passed
            loc_1 = T_i_list.track_indices[i - 1]
            new_time_1 = calculate_time(x, v, i - 1, T) + time_passed
            T_i_list.change_key(T_i_list.Heap_initial.keys[loc_1], loc_1, new_time_1)  # O(logn)

        if i <= n - 3:                 #updating the location of (i+2)th particle temporarily
            x_old = x[i + 2]
            x[i + 2] = x[i + 2] + v[i + 2] * (time_passed - position_update_time[i + 2])

        if i != n - 2:                 #updating the time of collision of (i+1)th and (i+2)th particle and changing the location of (i+2)th particle back to previous position
            loc_2 = T_i_list.track_indices[i + 1]
            new_time_2 = calculate_time(x, v, i + 1, T) + time_passed
            if i <= n - 3:
                x[i + 2] = x_old
            T_i_list.change_key(T_i_list.Heap_initial.keys[loc_2], loc_2, new_time_2)  # O(logn)

        num_collisions += 1

    return list_of_collisions

#TIME COMPLEXITY ANALYSIS :- O(n + mlogn)