from mpi4py import MPI
from math import ceil
import random
from classic import CPN_Gen, childrenNode, DAG, InitialSchedule, FAST, ScheduleLength
import time
start_time = time.time()

# DAG = {'a': [1, []], 'b': [6, ['a']], 'c': [8, ['a', 'b', 'e']], 'd': [1, ['b']], 'e': [1, ['a']]}
def retourne(liste):
    l = []
    for n in range(len(liste)):
        l.append(liste.pop())
    return l

def PP_Topo(CPN, DAG, listeSommets, n, tabCouleur):
    tabCouleur[n] = 1
    for nn in childrenNode(n, DAG):
        if tabCouleur[nn] == 0:
            PP_Topo(CPN, DAG, listeSommets, nn, tabCouleur)
    tabCouleur[n] = 2
    if not(n in CPN): #on veut que les blocking nodes pas les critical
        listeSommets.append(n)

def tri_topo(CPN, DAG=DAG):
    listeSommets = []
    tabCouleur = {}
    for n in DAG:
        tabCouleur[n] = 0
    for n in tabCouleur:
        if tabCouleur[n] == 0:
            PP_Topo(CPN, DAG, listeSommets, n, tabCouleur)
    return retourne(listeSommets)

def divide_list(list, q):
    l=[]
    a = len(l)//q
    for i in range(q-1):
        l.append(list[i*a:(i+1)*a])
    l.append(list[(q-1)*a:])

MAXSTEP=5
MAXCOUNT=3
MARGIN=2
p=2 # number of processeurs for our tasks
def PFAST(MAXSTEP, MAXCOUNT, MARGIN, p, DAG=DAG):

    comm = MPI.COMM_WORLD
    q = comm.Get_size() #number of processeurs for our algo
    Me = comm.Get_rank()

    CPN = CPN_Gen(DAG)
    BestSchedule = InitialSchedule(p, DAG, CPN)
    if Me == 0: # master
        tri = tri_topo(CPN, DAG)
        lists = divide_list(tri, q)
        list_transition = []
    list = None
    comm.scatter(lists, list, root=0)
    total_searchcount = 0
    while total_searchcount < MAXCOUNT:
        i = 2
        NewSchedule, searchcount = FAST(MAXSTEP, ceil(MAXCOUNT/(i*q)), MARGIN, p, DAG, CPN, BestSchedule, list)
        length = ScheduleLength(NewSchedule)
        comm.allgather(length, list_transition)
        bestindex = 0
        best = list_transition[0]
        for j in range(1, len(list_transition)):
            lengthi = list_transition[i]
            if lengthi < best:
                bestindex = j
                best = lengthi
        BestSchedule = comm.bcast(NewSchedule, root=bestindex)
        i *= 2
        temp = comm.allreduce(searchcount, op=MPI.SUM)
        total_searchcount += temp

print("resultat du Pfast : ",PFAST(5,3,2,2))
print("temps d'ex du Pfast : ","--- %s seconds ---" % (time.time() - start_time))