import random
from itertools import islice
import time
import statistics
from matplotlib import pyplot as plt

class Problem:

    global no_elements , no_clusters , cluster_type , cluster_limit , node_w, distance_matrix
    
    def GetData(self, file):
        """
        Used to read values from txt file, returns number of elements and clusters, the cluster type and limit, finally the node weights and edge weights 
        """
        with open(file) as f:
            for line in f:
                line = line.split(" ")
                space_index = [i for i, e in enumerate(line) if e == '']
                for index in sorted(space_index, reverse=True):
                    del line[index]
                break_index = [i for i, e in enumerate(line) if e == '\n']
                for index in sorted(break_index, reverse=True):
                    del line[index]
                no_elements = int(line[0])
                no_clusters = int(line[1])
                cluster_type = line[2]
                cluster_limit = list()
                for i in range(no_clusters):
                    if (i%2) == 0:
                        cluster_limit.append(line[i+3:i+5])
                    else:
                        cluster_limit.append(line[i+2:i+4])
                cluster_limit = [[int(num) for num in lst[:]] for lst in cluster_limit]
                w_index = [i for i, e in enumerate(line) if e == 'W']
                node_w = line[w_index[0]+1:]
                for i in range(0, len(node_w)):
                    node_w[i] = int(node_w[i])
                break
    
        distance_matrix = [[0 for i in range(no_elements)] for i in range(no_elements)]
        with open(file) as f:
            for line in islice(f, 1, None):
                line = line.split(" ")
                line[2] = line[2].replace("\n","")
                node_1 = int(line[0])
                node_2 = int(line[1])
                edge_weight = float(line[2])
                distance_matrix[node_1][node_2] = edge_weight

        return no_elements , no_clusters , cluster_type , cluster_limit , node_w, distance_matrix
    
    def Constraint(self, Cluster, Cluster_Size):
        """
        returns true if cluster has capacity, false otherwise 
        """
        Lower_limit =  cluster_limit [Cluster][0] 
        Upper_limit =  cluster_limit [Cluster][1]

        if(Cluster_Size <=Lower_limit):# first try to achive the Lowest limit 
            return True  
        elif (Cluster_Size <= Upper_limit):
            return True
        else:
            return False
    
    def Constraint_1Nodes(self,node,Cluster1,Cluster2,Clusters_Size):
        """
        returns true if node fits new cluster, false otherwise 
        """
        node_weigth = node_w[node]
        c1_size=Clusters_Size[Cluster1]
        c2_size=Clusters_Size[Cluster2]
        
        c1_size = c1_size-node_weigth
        c2_size = c2_size + node_weigth        

        #check Constraint 
        if(self.Constraint(Cluster1,c1_size) and self.Constraint(Cluster2,c2_size)):
            return True  
        else:
            return False    
    
    def Constraint_2Nodes(self,node1,node2,Cluster1,Cluster2,Clusters_Size):
        """
        returns true if two nodes sent fit constraint of each others clusters, false otherwise  
        """
        n1_weigth = node_w[node1]
        n2_weigth = node_w[node2]
        c1_size=Clusters_Size[Cluster1]
        c2_size=Clusters_Size[Cluster2]
        
        c1_size = c1_size-n1_weigth
        c1_size = c1_size + n2_weigth
        c2_size = c2_size-n2_weigth
        c2_size = c2_size + n1_weigth        

        #check Constraint 
        if(self.Constraint(Cluster1,c1_size) and self.Constraint(Cluster2,c2_size)):
            return True  
        else:
            return False     



class Solution:
    
    def __init__(self,no_elements,no_clusters,cluster_limit,node_w,distance_matrix):
       self.no_clusters = no_clusters
       self.cluster_limit = cluster_limit
       self.node_w = node_w
       self.no_elements = no_elements
       self.distance_matrix = distance_matrix
        
    def SolutionRepresention(self):
        """
        creates vector representing the solution
        """
        Nodes_vector = [-1] * self.no_elements

        return Nodes_vector

    def Lookup_Cluster_Nodes(self,cluster,Nodes_Vector):
        """
        returns a list of nodes in the passed cluster
        """
        NodeListonCluster = []
        for N, C in enumerate(Nodes_Vector):
            if(C==cluster):
                NodeListonCluster.append(N)
    
        return NodeListonCluster 
  
    def clusters_fit_constraint(self,Current_node,Nodes_Vector):
        """
        returns the available clusters and their size
        """
        Avaliable_Constraint = []
        Clusters_Size = []
        for c in range (self.no_clusters):
            Cluster_Size=0
            Cluster_Nodes = self.Lookup_Cluster_Nodes(c, Nodes_Vector) 
            p = Problem() 
            for n in Cluster_Nodes: 
                Cluster_Size =Cluster_Size+ self.node_w[n]                
            Clusters_Size.append(Cluster_Size)
            
            Cluster_Size = Cluster_Size+ self.node_w[Current_node]
            if(p.Constraint(c,Cluster_Size)):
                Avaliable_Constraint.append(c)
	   
        return Avaliable_Constraint,Clusters_Size

    
    def Cluster_NotEmpty(self,C,Nodes):
        """
        returns true if cluster not empty 
        """
        for val in Nodes:
            if (val == C):
                return True
  
    def UnAssigned_Node(self, Nodes_Vector):
        """
        returns a list of nodes that haven't been assigned to a cluster 
        """
        list = []
        for n,c in enumerate(Nodes_Vector):
            if(c==-1):
                list.append(n)
        return list 

    def Greedy_Solution(self,Nodes_Vector):
        """
        returns a solution built using greedy heuristic 
        """
        for n in range(len(Nodes_Vector)):
            ClusterList,a = self.clusters_fit_constraint(n,Nodes_Vector)
            c = random.choice(ClusterList)  
            Nodes_Vector[n]=c      
        return Nodes_Vector 
  
    def Random_Solution(self,Nodes_Vector):
        """
        returns a solution built using random heuristic 
        """
        while True:
            unassigned_n = self.UnAssigned_Node(Nodes_Vector)
            if unassigned_n:
                n = random.choice(unassigned_n)
            else:
                break

            available_clusters ,_= self.clusters_fit_constraint(n,Nodes_Vector)
            c = random.choice(available_clusters)
            Nodes_Vector[n]= c    
        return Nodes_Vector #random solution
              
    def Print_solution(self,Solution):
        """
        prints the clusters and a list of their corresponding assigned nodes 
        """
        for c in range(self.no_clusters):
            cluster=[]
            for n, val in enumerate(Solution):
              if (val == c):
                  cluster.append(n) 
            print('Cluster ',c,"is",cluster)        


class Algorithm:
    
    problem = Problem()

    def __init__(self,no_elements, no_clusters,cluster_limit,node_weight, distance_matrix):
       self.no_elements= no_elements
       self.no_clusters = no_clusters
       self.cluster_limit = cluster_limit
       self.node_weight = node_weight
       self.distance_matrix = distance_matrix
       self.sol = Solution(no_elements,no_clusters,cluster_limit,node_weight, distance_matrix)
   
    def neighborhood (self, solution, clusters_size):
        """
        returns the neighborhood of the passed solution, built using single swap and move 
        returns a list of the operator used to generate each neighbor  
        """
        neighborhood  = []
        operator = []
        #Swap 
        for c1 in range(self.no_clusters):
            c1_nodes = self.sol.Lookup_Cluster_Nodes(c1,solution)
            for index, n1 in enumerate(c1_nodes):
                for c2 in [x for x in range(self.no_clusters) if x != c1]:
                    c2_nodes = self.sol.Lookup_Cluster_Nodes(c2,solution)
                    for index, n2 in enumerate(c2_nodes):
                        copy_solution = solution.copy()
                        copy_solution[n1], copy_solution[n2] = copy_solution[n2], copy_solution[n1]
                        if copy_solution not in neighborhood:
                            if(self.problem.Constraint_2Nodes(n1,n2,c1,c2,clusters_size)):
                                neighborhood.append(copy_solution)
                                operator.append(['swap',n1,n2,c1,c2])
        #Move
        for c1 in range(self.no_clusters):
            c1_nodes = self.sol.Lookup_Cluster_Nodes(c1,solution)
            for index, n1 in enumerate(c1_nodes):
                for c2 in [x for x in range(self.no_clusters) if x != c1]:
                    if(self.problem.Constraint_1Nodes(n1,c1,c2,clusters_size)):
                        copy_solution = solution.copy()
                        copy_solution[n1] = c2
                        neighborhood.append(copy_solution)
                        operator.append(['move',n1,-1,c1,c2])

        return neighborhood, operator 
    
    def local_search(self,init_solution):
        """
        returns the local optima and its corresponding objective function 
        """
        objF = []
        for c in range(self.no_clusters):
            objF.append(self.Objective_Function_Cluster(init_solution,c))
        _,cluster_size = self.sol.clusters_fit_constraint(0,init_solution)
        neighbors, operators = self.neighborhood(init_solution,cluster_size)
        best_solution = init_solution.copy()
        bestObjF = objF.copy()
        for index, neighbor in enumerate(neighbors):
            if operators[index][0] == "move":
                new_objF1 = self.Objective_Function_Cluster(init_solution, operators[index][-2])
                new_objF2 = self.Objective_Function_Cluster(init_solution, operators[index][-1])
                new_objF = objF.copy()
                new_objF[operators[index][-2]] = new_objF1
                new_objF[operators[index][-1]] = new_objF2
                if sum(new_objF) > sum(objF):
                    best_solution = neighbor.copy()
                    bestObjF = new_objF.copy()
            if operators[index][0] == "swap":
                new_objF1 = self.Objective_Function_Cluster(init_solution, operators[index][-2])
                new_objF2 = self.Objective_Function_Cluster(init_solution, operators[index][-1])
                new_objF = objF.copy()
                new_objF[operators[index][-2]] = new_objF1
                new_objF[operators[index][-1]] = new_objF2
                if sum(new_objF) > sum(objF):
                    best_solution = neighbor.copy()
                    bestObjF = new_objF.copy()
        
        if sum(objF) >= sum(bestObjF):
            return init_solution, objF
        else:
            self.local_search(best_solution)
    
    def multistart(self, init_solution):
        """
        returns the global optima using random multistart heuristic and its corresponding objective function 
        """
        init_objF = []
        for c in range(self.no_clusters):
            init_objF.append(self.Objective_Function_Cluster(init_solution,c))
        bestObjF = init_objF.copy()
        best_solution = init_solution.copy()

        local_optima, local_objF = self.local_search(init_solution)

        search_memory = []
        while (True):
            if(sum(local_objF) >= sum(bestObjF)):
                bestObjF = local_objF.copy()
                best_solution = local_optima.copy()
                search_memory.append(best_solution)
                Nodes = self.sol.SolutionRepresention()
                Random_Solution = self.sol.Random_Solution(Nodes)
                local_optima, local_objF = self.local_search(Random_Solution)
            else:
                break
        
        return best_solution, bestObjF
    
    def Objective_Function_Cluster(self, solution, cluster):
        """
        calculates the objective function of the passed cluster 
        """
        cluster_nodes = [cluster]
        for index, node in enumerate(solution):
            if node == cluster:
                cluster_nodes.append(index)
        
        edge_w = 0    
        for index, node1 in enumerate(cluster_nodes[1:]):
            for index, node2 in enumerate(cluster_nodes[index+1:]):
                if self.distance_matrix[node1][node2]:
                    edge_w += self.distance_matrix[node1][node2]                
        objF = edge_w
    
        return objF 

##################################################  MAIN  ###########################################################################

X = Problem()   

no_elements , no_clusters , cluster_type , cluster_limit , node_w, distance_matrix = X.GetData("RanReal240/RanReal240_01.txt")
solution = Solution(no_elements, no_clusters,cluster_limit,node_w, distance_matrix)
alg = Algorithm(no_elements,no_clusters,cluster_limit,node_w, distance_matrix)


#Initial Solution
Nodes = solution.SolutionRepresention()
# Initial_Solution = solution.Random_Solution(Nodes)
Initial_Solution = solution.Greedy_Solution(Nodes)

# 10 Iterative on Local search
curveObj_Local = []
curveTime_Local = []
solutions_local = []
print("Initial Solution: ", Initial_Solution)
for i in range(10):
    start_time = time.time()
    optimum , objf = alg.local_search(Initial_Solution)
    end_time = time.time()
    curveObj_Local.append(sum(objf))
    solutions_local.append(optimum)
    elapsed_time = end_time - start_time
    curveTime_Local.append(elapsed_time)

print("-----------------------------------")
print("Results - Local Search")
print("Iteration number ", "Objective Function ", 'Time')

for index, sec in enumerate(curveTime_Local):
    print(index+1, '\t\t\t',curveObj_Local[index],'\t\t', sec) 
print("Average Time: ",sum(curveTime_Local)/len(curveTime_Local))
print("Average Objective Function: ",sum(curveObj_Local)/len(curveObj_Local))
print("Best Solution and Objective Function: ", solutions_local[curveObj_Local.index(max(curveObj_Local))], max(curveObj_Local))
local_stdev = f'{statistics.stdev(curveObj_Local):.9f}'
print("Standard Deviation Objective Function: ", local_stdev)

# 10 Iterative on Multi Start search
curveObj_multi = []
curveTime_multi = []
solutions_multi = []
for i in range(10):
    start_time = time.time()
    global_solution , global_objf = alg.multistart(Initial_Solution)
    end_time = time.time()
    curveObj_multi.append(sum(global_objf))
    solutions_multi.append(global_solution)
    elapsed_time = end_time - start_time
    curveTime_multi.append(elapsed_time)
print("-----------------------------------")
print("Results - Multistart local Search")
print("Iteration number ", "Objective Function ", 'Time')

for index, sec in enumerate(curveTime_multi):
    print(index+1, '\t\t\t',curveObj_multi[index],'\t\t', sec) 
print("Average Time: ",sum(curveTime_multi)/len(curveTime_multi))
print("Average Objective Function: ", sum(curveObj_multi)/len(curveObj_multi))
print("Best Solution and Objective Function: ", solutions_multi[curveObj_multi.index(max(curveObj_multi))], max(curveObj_multi))
multi_stdev = f'{statistics.stdev(curveObj_multi):.9f}'
print("Standard Deviation Objective Function: ", multi_stdev)


#  Plotting
plt.figure()
print(curveObj_multi)
plt.plot(range(10),curveObj_Local,'r', label='Local Search') 
plt.plot(range(10), curveObj_multi,'b',label='Multistart Search')
plt.ylabel('Objective Function')
plt.xlabel('Iteration')
plt.legend()
plt.show()