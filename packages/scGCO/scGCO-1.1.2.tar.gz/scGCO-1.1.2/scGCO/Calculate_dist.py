import multiprocessing as mp
from sklearn.cluster import DBSCAN,KMeans
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, hamming
import math
import parmap
import random
import parmap
import itertools
from itertools import repeat
from scipy.spatial import distance
import operator
from tqdm import tqdm
from functools import reduce
from sklearn import mixture
import statsmodels.stats.multitest as multi
import networkx as nx
from .Preprocessing import *
from .Graph_cut import *
from .Visualization import *
    
    
def calc_distance_com_single(geneID,nodes,model_labels, locs, data_norm,tissue_mat):
    genelist = []
    recal_genelist = []
    ham_dist_list = []
    ham_new_dist_list = []
    jac_dist_list = []
    haus_dist_list = []
    
    if True:
        if geneID in data_norm.columns:
            node = nodes
            model_label = model_labels
            if len(node)==1 and len(node[0])==locs.shape[0]:
                recal_genelist.append(geneID)
            else:
                # print(geneID)
                genelist.append(geneID)
                target_mat = list()
                target_class = []
                for nn in range(len(node)):
                    pred_com = model_label[np.array(node[nn])]  
                    unique_com, counts_com = np.unique(pred_com, return_counts=True)
                    major_label = unique_com[np.where(counts_com == counts_com.max())[0][0]]
                    temp_target = np.zeros(locs.shape[0])
                    temp_target[node[nn]] = 1
                    if sum(temp_target)< (1/2)*locs.shape[0]+10:
                        # print(nn, len(node[nn]))
                        target_mat.append(temp_target)
                        target_class.append(major_label)

                overlap = cdist(tissue_mat, target_mat,compute_inclusion_min)
                
                # merge these best matched target whose are one group gmmLabels.
                if len(target_mat)>1:  # target mat matching one tissue mat were merged
                    if sum(np.max(overlap, axis = 0)>0)>0:
                        maxInd = np.argmax(overlap, axis=0)
                        Ind, num = np.unique(np.argmax(overlap.T[np.max(overlap, axis= 0)>0].T, axis=0),
                                            return_counts=True)
                        if np.any(np.max(overlap, axis = 0) == 0):
                            np.place(maxInd, np.max(overlap, axis = 0) == 0, -1)  ## just Exclude those that don't match at all
                        total_targe_mat = []
                        if np.any(np.array(num)==1):
                            inds = np.array(Ind)[np.array(num)==1]
                            for ind in inds:
                                temp_targe_mat = np.array(target_mat)[maxInd == ind]
                                total_targe_mat.append(temp_targe_mat[0])
                                # print('Rank{} No need merge targe: {}'.format(ind, np.where(maxInd == ind)[0]))

                        if np.any(np.array(num)>1):
                            inds = np.array(Ind)[np.array(num)>1]
                            for ind in inds:
                                for cl in np.unique(target_class):
                                    merge_ind = set(np.where(np.array(target_class) == cl)[0])& set(np.where(maxInd == ind)[0])
                                    # print('Rank{} & Labels{} Need merge targe:{}'.format(ind, cl, merge_ind))
                                    if len(merge_ind)>0:
                                        temp_targe_mat = sum(np.array(target_mat)[np.array(list(merge_ind))])
                                        if sum(temp_targe_mat>1)>0:
                                            np.place(temp_targe_mat, temp_targe_mat>1, 1)
                                        if sum(temp_targe_mat) > locs.shape[0]/2+10:
                                            temp_targe_mat = abs(1 - temp_targe_mat)
                                        total_targe_mat.append(temp_targe_mat)
                #             print(inds, len(total_targe_mat))
                    else:
                        total_targe_mat = target_mat
                else:
                    total_targe_mat = target_mat

                # merge tissue 
                if len(tissue_mat)>1:  # tissue mat matching one targe mat were merged
                    maxInd = np.argmax(overlap, axis=1)
                    if sum(np.max(overlap, axis = 1)>0)>0:
                        Ind_tis, num_tis = np.unique(np.argmax(overlap[np.max(overlap, axis = 1)>0],axis=1),
                                                    return_counts=True)
                        if np.any(np.max(overlap, axis = 1) == 0):
                            np.place(maxInd, np.max(overlap, axis = 1) == 0, -1)  ## just Exclude those that don't match at all
                        total_tissue_mat = []
                        if np.any(np.array(num_tis)==1):
                            inds = np.array(Ind_tis)[np.array(num_tis)==1]
                            for ind in inds:
                                temp_tissue_mat = np.array(tissue_mat)[maxInd == ind]
                                total_tissue_mat.append(temp_tissue_mat[0])
                                # print('Rank{} No need merge tissue: {}'.format(ind, np.where(maxInd==ind)[0]))

                        if np.any(np.array(num_tis)>1):
                            inds = np.array(Ind_tis)[np.array(num_tis)>1]
                            for ind in inds:
                                temp_tissue_mat = sum(np.array(tissue_mat)[maxInd == ind])
                                if sum(temp_tissue_mat>1)>0:
                                    np.place(temp_tissue_mat, temp_tissue_mat>1, 1)
                                total_tissue_mat.append(temp_tissue_mat)
                                # print('Rank{} Need merge tissue: {}'.format(ind, np.where(maxInd==ind)[0]))
                    else:
                        total_targe_mat = tissue_mat
                else:
                    total_tissue_mat = tissue_mat


                ham_dist = cdist(total_tissue_mat, total_targe_mat, compute_diff_vs_common_const10)
                ham_dist_list.append(np.min(ham_dist))

                ham_new_dist = cdist(total_tissue_mat, total_targe_mat, compute_diff_vs_common)
                ham_new_dist_list.append(np.min(ham_new_dist))

                jac_dist = cdist(total_tissue_mat, total_targe_mat, jaccard_dist)
                jac_dist_list.append(np.min(jac_dist))

                haus_dist = []
                for tar in total_targe_mat:
                    target_locs = locs[tar==1]
                    for tis in total_tissue_mat:
                        tissue_locs = locs[tis==1]
                        haus_dist.append(compute_hausdorff(tissue_locs, target_locs))
                haus_dist_list.append(np.min(haus_dist))

    return genelist, ham_dist_list, jac_dist_list,haus_dist_list, ham_new_dist_list

def calc_distance_com(geneList,nodes,model_labels, locs, data_norm,tissue_mat):
    genelist = []
    recal_genelist = []
    ham_dist_list = []
    ham_new_dist_list = []
    jac_dist_list = []
    haus_dist_list = []
    
    for geneID in geneList:
        if geneID in data_norm.columns:
            node = nodes[geneID]
            model_label = np.array(model_labels[geneID])
            if len(node)==1 and len(node[0])==locs.shape[0]:
                recal_genelist.append(geneID)
            else:
                # print(geneID)
                genelist.append(geneID)
                target_mat = list()
                target_class = []
                for nn in range(len(node)):
                    pred_com = model_label[np.array(node[nn])]  
                    unique_com, counts_com = np.unique(pred_com, return_counts=True)
                    major_label = unique_com[np.where(counts_com == counts_com.max())[0][0]]
                    temp_target = np.zeros(locs.shape[0])
                    temp_target[node[nn]] = 1
                    if sum(temp_target)< (1/2)*locs.shape[0]+10:
                        # print(nn, len(node[nn]))
                        target_mat.append(temp_target)
                        target_class.append(major_label)

                overlap = cdist(tissue_mat, target_mat,compute_inclusion_min)
                
                # merge these best matched target whose are one group gmmLabels.
                if len(target_mat)>1:  # target mat matching one tissue mat were merged
                    if sum(np.max(overlap, axis = 0)>0)>0:
                        maxInd = np.argmax(overlap, axis=0)
                        Ind, num = np.unique(np.argmax(overlap.T[np.max(overlap, axis= 0)>0].T, axis=0),
                                            return_counts=True)
                        if np.any(np.max(overlap, axis = 0) == 0):
                            np.place(maxInd, np.max(overlap, axis = 0) == 0, -1)  ## just Exclude those that don't match at all
                        total_targe_mat = []
                        if np.any(np.array(num)==1):
                            inds = np.array(Ind)[np.array(num)==1]
                            for ind in inds:
                                temp_targe_mat = np.array(target_mat)[maxInd == ind]
                                total_targe_mat.append(temp_targe_mat[0])
                                # print('Rank{} No need merge targe: {}'.format(ind, np.where(maxInd == ind)[0]))

                        if np.any(np.array(num)>1):
                            inds = np.array(Ind)[np.array(num)>1]
                            for ind in inds:
                                for cl in np.unique(target_class):
                                    merge_ind = set(np.where(np.array(target_class) == cl)[0])& set(np.where(maxInd == ind)[0])
                                    # print('Rank{} & Labels{} Need merge targe:{}'.format(ind, cl, merge_ind))
                                    if len(merge_ind)>0:
                                        temp_targe_mat = sum(np.array(target_mat)[np.array(list(merge_ind))])
                                        if sum(temp_targe_mat>1)>0:
                                            np.place(temp_targe_mat, temp_targe_mat>1, 1)
                                        if sum(temp_targe_mat) > locs.shape[0]/2+10:
                                            temp_targe_mat = abs(1 - temp_targe_mat)
                                        total_targe_mat.append(temp_targe_mat)
                #             print(inds, len(total_targe_mat))
                    else:
                        total_targe_mat = target_mat
                else:
                    total_targe_mat = target_mat

                # merge tissue 
                if len(tissue_mat)>1:  # tissue mat matching one targe mat were merged
                    maxInd = np.argmax(overlap, axis=1)
                    if sum(np.max(overlap, axis = 1)>0)>0:
                        Ind_tis, num_tis = np.unique(np.argmax(overlap[np.max(overlap, axis = 1)>0],axis=1),
                                                    return_counts=True)
                        if np.any(np.max(overlap, axis = 1) == 0):
                            np.place(maxInd, np.max(overlap, axis = 1) == 0, -1)  ## just Exclude those that don't match at all
                        total_tissue_mat = []
                        if np.any(np.array(num_tis)==1):
                            inds = np.array(Ind_tis)[np.array(num_tis)==1]
                            for ind in inds:
                                temp_tissue_mat = np.array(tissue_mat)[maxInd == ind]
                                total_tissue_mat.append(temp_tissue_mat[0])
                                # print('Rank{} No need merge tissue: {}'.format(ind, np.where(maxInd==ind)[0]))

                        if np.any(np.array(num_tis)>1):
                            inds = np.array(Ind_tis)[np.array(num_tis)>1]
                            for ind in inds:
                                temp_tissue_mat = sum(np.array(tissue_mat)[maxInd == ind])
                                if sum(temp_tissue_mat>1)>0:
                                    np.place(temp_tissue_mat, temp_tissue_mat>1, 1)
                                total_tissue_mat.append(temp_tissue_mat)
                                # print('Rank{} Need merge tissue: {}'.format(ind, np.where(maxInd==ind)[0]))
                    else:
                        total_targe_mat = tissue_mat
                else:
                    total_tissue_mat = tissue_mat


                ham_dist = cdist(total_tissue_mat, total_targe_mat, compute_diff_vs_common_const10)
                ham_dist_list.append(np.min(ham_dist))

                ham_new_dist = cdist(total_tissue_mat, total_targe_mat, compute_diff_vs_common)
                ham_new_dist_list.append(np.min(ham_new_dist))

                jac_dist = cdist(total_tissue_mat, total_targe_mat, jaccard_dist)
                jac_dist_list.append(np.min(jac_dist))

                haus_dist = []
                for tar in total_targe_mat:
                    target_locs = locs[tar==1]
                    for tis in total_tissue_mat:
                        tissue_locs = locs[tis==1]
                        haus_dist.append(compute_hausdorff(tissue_locs, target_locs))
                haus_dist_list.append(np.min(haus_dist))

    return genelist, ham_dist_list, jac_dist_list,haus_dist_list, ham_new_dist_list

        

def calc_distance_com_parallel(geneList, nodes, model_labels, locs, data_norm, tissue_mat):
    num_cores = mp.cpu_count()
    if num_cores > math.floor(len(geneList)/2):
         num_cores=int(math.floor(len(geneList)/2))
    ttt = np.array_split(np.array(list(geneList)),num_cores)
    tuples = [(g, n, m, l, d, t) for g, n, m, l, d, t in zip( 
                                    ttt,
                                    repeat(nodes, num_cores),
                                    repeat(model_labels, num_cores),
                                    repeat(locs, num_cores),
                                    repeat(data_norm, num_cores),
                                    repeat(tissue_mat, num_cores))] 
    
    results = parmap.starmap(calc_distance_com, tuples,
                                pm_processes=num_cores, pm_pbar=True)
    
    g = [results[i][0] for i in np.arange(len(results))]
    genes = reduce(operator.add, g)
    ham = [results[i][1] for i in np.arange(len(results))]
    ham_dist_list = reduce(operator.add, ham)
    jac = [results[i][2] for i in np.arange(len(results))]
    jac_dist_list = reduce(operator.add, jac)
    haus = [results[i][3] for i in np.arange(len(results))]
    haus_dist_list = reduce(operator.add, haus)
    ham2 = [results[i][4] for i in np.arange(len(results))]
    ham_new_dist_list = reduce(operator.add, ham2)
    
    
    df = pd.DataFrame(index=genes, 
        data= {'Hamming':ham_dist_list, 
                'Jaccard':jac_dist_list,
                'Hausdorff':haus_dist_list,
                'Hamming2':ham_new_dist_list})
    return df


def compute_inclusion_min(u, v):
#    if len(np.where((u+v) == 2)[0]) == 0:
#        return len(np.where(abs(u-v) == 1)[0])
#    else:
    return len(np.where((u+v) == 2)[0])/min(sum(v),sum(u))


def compute_hausdorff(u,v):
    '''
    Compute norm hausdorff geometry distance between two pattern.
    u: target_mat
    v: tissue_mat
    
    '''
    
    dist_u_v=distance.directed_hausdorff(u,v)[0]
    dist_v_u=distance.directed_hausdorff(v,u)[0]
    
    # if norm_factor:
    #     dist= max(dist_u_v/compute_norm_factor(v),dist_v_u/compute_norm_factor(u))
    # else:     
    return max(dist_u_v,dist_v_u)


def compute_diff_vs_common_const10(u, v):
    return len(np.where((u+v) == 1)[0])/(2*len(np.where((u+v) == 2)[0]) + 10)

def compute_diff_vs_common(u, v):
    return len(np.where((u+v) == 1)[0])/(2*len(np.where((u+v) == 2)[0]) + 1)

def jaccard_dist(u, v):
    return  1 - len(np.where((u+v) == 2)[0])/(len(np.where((u+v) > 0)[0]))


def recalc_distance_com(geneList, models, locs, data_norm,cellGraph, tissue_mat, gmmDict):
    
    
    noise_size_estimate =9 # min(np.min(np.sum(cand_seed_mat, axis=1)), 9)  ## #noise<=9
    size_factor=200
    new_hamming=[]
    new_jaccard=[]
    new_hausdorff=[]  
    new_hamming2= []
    
    genes = []
    p_values = list()
    node_list = list()
    s_factors = list()
    model_list = list()
    model_labels = list()
    pred_labels = list()
            
    for geneID in geneList: #zeor_boundGenes: #de_counts: 
        # print(geneID)
        hamming_dist_list=[]
        jaccard_dist_list=[]
        hausdorff_dist_list=[]
        hamming_new_dist_list = []
        p_min=[]
        smooth_factors = list()
       
        exp = data_norm.loc[:,geneID].values
        if geneID in models.index:
            model = models[geneID]
            gmm = gmmDict[geneID]
        else:
            model = 'gmm'
            gmm = perform_gmm(exp)
          
        temp_factor = 0   # 'Cldn9' need start from sf=0 
        if model == 'gmm':
            p,nodes,newLabels,_,com, label_pred = compute_single_gmm_fixed_sf(
                            locs,exp,cellGraph, gmm, temp_factor)
        else:
            p,nodes,newLabels,_,com, label_pred = compute_single_otsu_fixed_sf(
                                        locs,exp,cellGraph,temp_factor)
        num_isolate = count_isolate(locs,cellGraph, newLabels) 

        noise_size = sum(num_isolate[0:int(2*noise_size_estimate)]) 
        normalized_noise = noise_size*(size_factor/len(exp))
        noise_cutoff=normalized_noise
         
        nodeDict = {}
        nodeDict[geneID] = nodes

        model_labelsDict = {}
        model_labelsDict[geneID] = label_pred
        df_list = calc_distance_com([geneID],nodeDict,model_labelsDict, locs, data_norm,tissue_mat)
        
        if noise_cutoff<6 and noise_cutoff>0:  ## 'Vstm4' have no 0<noise<5 , just skip 5.
            hamming_dist_list.append(df_list[1][0])
            jaccard_dist_list.append(df_list[2][0])
            hausdorff_dist_list.append(df_list[3][0])
            hamming_new_dist_list.append(df_list[4][0])
            p_min.append(min(p))
            smooth_factors.append(temp_factor)
             
        while noise_cutoff >0 and temp_factor<=60:            
            temp_factor = temp_factor+5
            if model == 'gmm':
                p,nodes,newLabels,_,com, label_pred = compute_single_gmm_fixed_sf(
                                locs,exp,cellGraph,gmm, temp_factor)
            else:
                p,nodes,newLabels,_,com, label_pred = compute_single_otsu_fixed_sf(
                                            locs,exp,cellGraph,temp_factor)
            num_isolate = count_isolate(locs,cellGraph, newLabels) 
            
            noise_size = sum(num_isolate[0:int(2*noise_size_estimate)]) 
            normalized_noise = noise_size*(size_factor/len(exp))
            noise_cutoff=normalized_noise
            
            nodeDict = {}
            nodeDict[geneID] = nodes

            model_labelsDict = {}
            model_labelsDict[geneID] = label_pred
            df_list = calc_distance_com([geneID],nodeDict,model_labelsDict, locs, data_norm,tissue_mat)
            
            if noise_cutoff<6 and noise_cutoff>0:
                hamming_dist_list.append(df_list[1][0])
                jaccard_dist_list.append(df_list[2][0])
                hausdorff_dist_list.append(df_list[3][0])
                hamming_new_dist_list.append(df_list[4][0])
                p_min.append(min(p))
                smooth_factors.append(temp_factor)

        if len(hausdorff_dist_list)>0:
            genes.append(geneID)
            best_p=min(p_min)  ## multiple min(p) select min(jaccard_dist) amony
            best_p_index=np.where(np.array(p_min)==best_p)[0]
            min_p_haus=[hausdorff_dist_list[i] for i in best_p_index]
            min_inde=np.where(np.array(hausdorff_dist_list)==min(min_p_haus))[0][0]
            #min_inde=np.argmin(p_min)  #jaccard_dist_list)   ## min(p) as selection standard.
            #min_inde_haus=np.argmin(hausdorff_dist_list)
            new_hamming.append(hamming_dist_list[min_inde])
            new_jaccard.append(jaccard_dist_list[min_inde])
            new_hausdorff.append(hausdorff_dist_list[min_inde])
            new_hamming2.append(hamming_new_dist_list[min_inde])
            final_sf= smooth_factors[min_inde]

            if model == 'gmm':
                p,nodes,newLabels,_,com, label_pred = compute_single_gmm_fixed_sf(
                                locs,exp,cellGraph,gmm, final_sf)
            else:
                p,nodes,newLabels,_,com, label_pred = compute_single_otsu_fixed_sf(
                                            locs,exp,cellGraph,final_sf)

            p_values.append(p)
            node_list.append(nodes)
            s_factors.append(final_sf)
            pred_labels.append(newLabels)
            model_list.append(model)
            model_labels.append(list(label_pred))
            
    best_p_values=[min(i) for i in p_values]
    labels_array = np.array(pred_labels).reshape(len(genes), pred_labels[0].shape[0])
    data_array = np.array((genes, p_values, best_p_values, s_factors, node_list, model_list , model_labels), dtype=object).T
    t_array = np.hstack((data_array, labels_array))
    c_labels = ['p_value', 'fdr',  'smooth_factor', 'nodes','model','model_labels']
    for i in np.arange(labels_array.shape[1]) + 1:
        temp_label = 'label_cell_' + str(i)
        c_labels.append(temp_label)
    result_df_new = pd.DataFrame(t_array[:,1:], index=t_array[:,0], 
                      columns=c_labels)
    
    dist_df_new = pd.DataFrame([new_hamming, new_jaccard,new_hausdorff, new_hamming2]).T        ### no norm dist
    dist_df_new.columns = ['Hamming', 'Jaccard','Hausdorff','Hamming2']
    dist_df_new.index =  genes
            
    return result_df_new, dist_df_new

## recalculate no cuts genes
def recalc_distance_com_parallel(geneList,model_list,locs, data_norm, cellGraph,
                                 tissue_mat, gmmDict):
    num_cores = mp.cpu_count()
    if num_cores > math.floor(len(geneList)/2):
         num_cores=int(math.floor(len(geneList)/2))
    ttt = np.array_split(np.array(list(geneList)),num_cores)
    tuples = [( g, m, l, d, c, t, mm) for g, m, l, d, c, t,mm in zip(
                                                        ttt, 
                                                        repeat(model_list, num_cores),
                                                        repeat(locs, num_cores),
                                                        repeat(data_norm, num_cores),
                                                        repeat(cellGraph, num_cores),
                                                        repeat(tissue_mat, num_cores),
                                                        repeat(gmmDict, num_cores))]
    dist_results = parmap.starmap(recalc_distance_com, tuples,
                             pm_processes=num_cores, pm_pbar=True)
    
    result_df_new=pd.DataFrame()
    best_dist_df=pd.DataFrame()
    for i in range(len(dist_results)):
        if dist_results[i][0].shape[0]>0 and dist_results[i][1].shape[0]>0:
            result_df_new=pd.concat([result_df_new,dist_results[i][0]])
            best_dist_df=pd.concat([best_dist_df,dist_results[i][1]])
    
    return result_df_new,best_dist_df




### ------------- Kmeans labels --------------------------
def calc_distance_kmeans(genelist,data_norm,tissue_mat, n_cluster = 5):
    ham_dist_list = []
    jac_dist_list = []
    geneList = []
    for geneID in genelist:
        X = data_norm.loc[:,geneID].values
        kmeans=KMeans(n_clusters= n_cluster,n_init=100).fit(X.reshape(-1,1))  #random_state= 0; n_init 更换初始值次数

        target_mat = []
        label,count = np.unique(kmeans.labels_, return_counts=True)
        for i in label:
            temp_vec = np.zeros(len(X))
            temp_vec[kmeans.labels_ == i]=1
            if sum(temp_vec) > len(X)/2+10:
                temp_vec = abs(1 - temp_vec)
            target_mat.append(temp_vec)

        ham_dist = cdist(tissue_mat, target_mat, compute_diff_vs_common_const10)
        ham_dist_list.append(np.min(ham_dist))

        jac_dist = cdist(tissue_mat, target_mat, jaccard_dist)
        jac_dist_list.append(np.min(jac_dist))
        geneList.append(geneID)
    
    # df = pd.DataFrame(index=geneList, 
    #         data= {'Hamming':ham_dist_list, 'Jaccard':jac_dist_list})
    return geneList, ham_dist_list, jac_dist_list

    
def calc_distance_kmeans_multi(genelist,data_norm,tissue_mat, n_cluster = 5):
    num_cores = mp.cpu_count()
    if num_cores > math.floor(len(genelist)/2):
         num_cores=int(math.floor(len(genelist)/2))
    ttt = np.array_split(np.array(list(genelist)),num_cores)
    tuples = [( g,  d,  t,  n) for g,  d,  t,  n in zip(
                                    repeat(ttt, num_cores),
                                    repeat(data_norm, num_cores),
                                    repeat(tissue_mat, num_cores),
                                    repeat(n_cluster, num_cores))]
    results = parmap.starmap(calc_distance_kmeans, tuples,
                                pm_processes=num_cores, pm_pbar=True)
    ggg = [results[i][0] for i in np.arange(len(results))]
    genes = reduce(operator.add, ggg)

    ham = [results[i][1] for i in np.arange(len(results))]
    ham = reduce(operator.add, ggg)

    jac = [results[i][2] for i in np.arange(len(results))]
    jac = reduce(operator.add, ggg)

    distance_df = pd.DataFrame(index= genes, 
            data= {'Hamming':ham, 'Jaccard':jac})

    return distance_df


    