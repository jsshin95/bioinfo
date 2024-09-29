from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

import mglearn

import urllib.request
import json

def isNan(value):
    return value != value

def searchRSID(sRSID):
    sURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&amp;id="+sRSID+"&amp;rettype=json&amp;retmode=text"
    dRSID = json.loads(urllib.request.urlopen(sURL).read().decode('utf-8'))
    return dRSID
"""
def readRSNumToEnsembl(sRSNum):
    sURL = "http://grch37.rest.ensembl.org/variation/human/"+sRSNum+"?content-type=application/json"
    dRSNum = json.loads(urllib.request.urlopen(sURL).read().decode('utf-8'))
    return dRSNum
"""
"""
#########################
# Step 1 : alt 분할 -> X
#########################
df = pd.read_csv('raw.tsv', delimiter='\t')
df2 = pd.DataFrame(columns=df.columns)

for i in range(len(df.index)):
    alts = df.loc[i,'observed'].split('/')
    for alt in alts:
        df.loc[i,'observed'] = alt
        df2.loc[len(df2.index)] = df.loc[i]

#print(df2)
#df2.to_csv("step1.tsv", sep='\t', index=False)
"""
"""
##############################
# Step 2 : 불필요한 col 제거
################################
df3 = pd.read_csv('raw.tsv', delimiter='\t')
df4 = df3.drop(columns=['#bin','chrom','chromStart','chromEnd','score','refNCBI','refUCSC','valid','weight','exceptions','submitterCount','submitters','alleles','alleleFreqs','bitfields'])
df4.to_csv("step2.tsv", sep='\t', index=False)

#########################
# Step 3 : SNP 필터링
#######################
df5 = pd.read_csv('step2.tsv', delimiter='\t')
df6 = df5[(df5['class'] == 'single')]
df6.to_csv("step3.tsv", sep='\t', index=False)
"""
"""
#####################
# Step 4 : rsID 검색 후 MAF 정보 가져오기
#####################
df7 = pd.read_csv('step3.tsv', delimiter='\t')
df8 = pd.DataFrame(columns=['name'])

#dRS = searchRSID(df7.loc[22,'name'])
#print(len(dRS['primary_snapshot_data']['allele_annotations'][0]['frequency']))
#print(dRS['primary_snapshot_data']['allele_annotations'][2]['frequency'][0]['observation']['inserted_sequence'])

for i in range(len(df7.index)):
    sRSID = df7.loc[i,'name']
    try:
        dRS = searchRSID(sRSID)
        ddRS = dRS['primary_snapshot_data']['allele_annotations']
    except:
        continue
    if len(ddRS) == 0 :
        continue
    err_flag=0
    for j in range(len(ddRS)):
        if len(ddRS[j]['frequency']) == 0 :
            err_flag=1
    if err_flag==1:
        continue
    for j in range(len(ddRS)):
        alts = ddRS[j]['frequency']
        df8.loc[len(df8.index),'name'] = sRSID + '_' + alts[0]['observation']['inserted_sequence']
        for k in range(len(alts)):
            cname = alts[k]['study_name'] + '_' + str(alts[k]['study_version'])
            df8.loc[len(df8.index)-1,cname] = alts[k]['allele_count']
    

#print(df8)
df8.to_csv("step4.tsv", sep='\t', index=False)
"""
"""
df9 = pd.read_csv('step4.tsv', delimiter='\t')


for i in range(len(df9.index)):
    sum = 0
    for j in range(1,len(df9.columns)):
        if isNan(df9.iloc[i,j]):
            df9.iloc[i,j] = 0 
        sum += int(df9.iloc[i,j])
    df9.loc[i,'sum'] = sum

df9.to_csv("step5.tsv", sep='\t', index=False)
"""
"""
"""
"""
df10 = pd.read_csv('step5.tsv', delimiter='\t')
df11 = df10[df10['sum'] != 0]
df11.to_csv("step6.tsv", sep='\t', index=False)

df12 = pd.read_csv('step6.tsv', delimiter='\t')
n=len(df12.index)
i=0
while(i<n):
    cnt=0
    if df12.iloc[i,0].split('_')[0] != df12.iloc[i+1,0].split('_')[0]:
        cnt = 1
    elif df12.iloc[i+1,0].split('_')[0] != df12.iloc[i+2,0].split('_')[0]:
        cnt = 2
    elif df12.iloc[i+2,0].split('_')[0] != df12.iloc[i+3,0].split('_')[0]:
        cnt = 3
    elif df12.iloc[i+3,0].split('_')[0] != df12.iloc[i+4,0].split('_')[0]:
        cnt = 4
    
    temp = [0] * len(df12.columns)
    for j in range(1,len(df12.columns)):
        for k in range(cnt):
            temp[j] += df12.iloc[i+k,j]
        for k in range(cnt):
            if temp[j] == 0 : df12.iloc[i+k,j] = 0
            else : df12.iloc[i+k,j] = round(df12.iloc[i+k,j] / temp[j], 5)
    
    if cnt > 1:
        min = 1e9
        min_index = 0
        for k in range(cnt):
            if df12.loc[i+k,'sum'] < min:
                min = df12.loc[i+k,'sum']
                min_index = i+k
        df12.loc[min_index,'sum'] = -1
    
    i += cnt
    if i >= n-4 : break # 수정 필요 -> index 초과 error

df12.to_csv("sstep7.tsv", sep='\t', index=False)
"""
"""
df13 = pd.read_csv('sstep7.tsv', delimiter='\t')
df14 = df13[df13['sum'] != -1]
df14 = df14.drop(columns='sum')
df14.to_csv("sstep8.tsv", sep='\t', index=False)

df15 = pd.read_csv('sstep8.tsv', delimiter='\t')
df16 = df15.T
df16.to_csv("sstep9.tsv", sep='\t') # column 위에 index number 제거 필요
"""

df17 = pd.read_csv('sstep999.tsv', delimiter='\t')
#print(df17)
nrow = len(df17.index)
temp_m1=[]
for j in range(1,len(df17.columns)):
    
    summ=0
    for i in range(nrow):
        summ += df17.iloc[i,j]
    if summ < 0.0001:
        summ = -1
    temp_m1.append(summ)
list_col_name=[]
for j in range(len(temp_m1)):
    if temp_m1[j] == -1:
        list_col_name.append(df17.columns[j+1])
df18 = df17.drop(columns=list_col_name)
#print(list_col_name)
df18.to_csv("sstep10.tsv", sep='\t',index=False)

xx = df18.iloc[:,1:].values
yy = df18.iloc[:,0].values
print(xx)
print(yy)

m_sc = StandardScaler()
x_sc = m_sc.fit_transform(xx)

m_pca2 = PCA(n_components = 2)
x_pca2 = m_pca2.fit_transform(x_sc)
print(x_pca2)

mglearn.discrete_scatter(x_pca2[:,0], x_pca2[:,1], y = yy)
plt.legend(yy, loc=4)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()
"""
"""
"""
for i in range(len(df.index)):
    sRSNum = df['name'].iloc[i]
    try:
        dRSNum = readRSNumToEnsembl(sRSNum)
        #sPos = dRSNum['mappings'][0]['location']
        sCon = dRSNum['most_severe_consequence']
    except:
        sCon = ''
    #print(sCon)
    targetset.add(sCon)
    df.loc[i,'consequence'] = sCon

"""
"""
print(df)
df = df.dropna(axis = 0)
print(df)

for i in range(len(df.index)):
    if df.iloc[i,0] == '-':
        df.iloc[i,0] = 0
    elif df.iloc[i,0] == '+':
        df.iloc[i,0] = 1
    
    if df.iloc[i,1] == 'single':
        df.iloc[i,1] = 1
    elif df.iloc[i,1] == 'insertion':
        df.iloc[i,1] = 2
    elif df.iloc[i,1] == 'in-del':
        df.iloc[i,1] = 3
    elif df.iloc[i,1] == 'deletion':
        df.iloc[i,1] = 4
    elif df.iloc[i,1] == 'mnp':
        df.iloc[i,1] = 5
    
    if df.iloc[i,4] == 'between':
        df.iloc[i,4] = 1
    elif df.iloc[i,4] == 'exact':
        df.iloc[i,4] = 2
    elif df.iloc[i,4] == 'range':
        df.iloc[i,4] = 3
    elif df.iloc[i,4] == 'rangeSubstitution':
        df.iloc[i,4] = 4
    elif df.iloc[i,4] == 'rangeDeletion':
        df.iloc[i,4] = 5
    
    list_consq = ['intron_variant', '5_prime_UTR_variant', 'missense_variant', 'splice_acceptor_variant', 'regulatory_region_variant', 'splice_donor_variant', 'splice_region_variant', 'non_coding_transcript_exon_variant', 'TF_binding_site_variant', '3_prime_UTR_variant', 'intergenic_variant', 'synonymous_variant', 'splice_polypyrimidine_tract_variant', 'splice_donor_5th_base_variant']
    for j in range(len(list_consq)):
        if df.iloc[i,5] == list_consq[j]:
            df.iloc[i,5] = (j+1)
            break

print(df)
df.to_csv("test2.tsv",sep='\t')

"""
"""
df2 = pd.read_csv('test2.tsv', delimiter='\t')
x = df2.iloc[:,0:5]
y = df2.iloc[:,5]
print(x)
print(y)

m_sc = StandardScaler()
x_sc = m_sc.fit_transform(x)

m_pca2 = PCA(n_components = 2)
x_pca2 = m_pca2.fit_transform(x_sc)

mglearn.discrete_scatter(x_pca2[:,0], x_pca2[:,1], y = y)
plt.legend(['intron_variant', '5_prime_UTR_variant', 'missense_variant', 'splice_acceptor_variant', 'regulatory_region_variant', 'splice_donor_variant', 'splice_region_variant', 'non_coding_transcript_exon_variant', 'TF_binding_site_variant', '3_prime_UTR_variant', 'intergenic_variant', 'synonymous_variant', 'splice_polypyrimidine_tract_variant', 'splice_donor_5th_base_variant'], loc=4)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()
"""