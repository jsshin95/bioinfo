import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

def createRandomAnnotation(nRow):
    newCol = []
    for _ in range(nRow):
        n = random.randint(1,100)
        if n < 41:
            newCol.append('syn')
        elif n < 80:
            newCol.append('non')
        else:
            newCol.append('other')
    return newCol

df = pd.read_csv('data.tsv',sep='\t')
df['ANNOTATION'] = createRandomAnnotation(len(df.index))
df['GENOTYPE'] = ['']*len(df.index)

varFreq=[0]*12
for i in range(len(df.index)):
    if df['REF'].iloc[i] == 'A':
        if df['ALT'].iloc[i] == 'T':
            varFreq[0] += 1
        elif df['ALT'].iloc[i] == 'G':
            varFreq[1] += 1
        elif df['ALT'].iloc[i] == 'C':
            varFreq[2] += 1
    elif df['REF'].iloc[i] == 'T':
        if df['ALT'].iloc[i] == 'A':
            varFreq[3] += 1
        elif df['ALT'].iloc[i] == 'G':
            varFreq[4] += 1
        elif df['ALT'].iloc[i] == 'C':
            varFreq[5] += 1
    elif df['REF'].iloc[i] == 'G':
        if df['ALT'].iloc[i] == 'A':
            varFreq[6] += 1
        elif df['ALT'].iloc[i] == 'T':
            varFreq[7] += 1
        elif df['ALT'].iloc[i] == 'C':
            varFreq[8] += 1
    elif df['REF'].iloc[i] == 'C':
        if df['ALT'].iloc[i] == 'A':
            varFreq[9] += 1
        elif df['ALT'].iloc[i] == 'T':
            varFreq[10] += 1
        elif df['ALT'].iloc[i] == 'G':
            varFreq[11] += 1
    
    gt=df['../output/test230322'].iloc[i].split(':')[0]
    if gt[0]==gt[2]:
        df['GENOTYPE'].iloc[i] = 'homo'
    else:
        df['GENOTYPE'].iloc[i] = 'hetero'

mutClass=['A>T','A>G','A>C','T>A','T>G','T>C','G>A','G>T','G>C','C>A','C>T','C>G']
colors = sns.color_palette('hls', len(mutClass)).as_hex()
data = go.Bar(x=mutClass, y=varFreq, marker = {'color':colors,'line':{'color':'black', 'width':3}}, width=0.5,)
layout = go.Layout(title='Fig1', font={'size':20})
fig1 = go.Figure(data=data, layout=layout)
fig1.update_xaxes(title_text='Mutation Class')
fig1.update_yaxes(title_text='Variant Frequency')
fig1.show() # to_html로 내보냄
fig1.write_html('fig1.html')
fig1.write_image('fig1.png')

fig2 = px.sunburst(df, path=['ANNOTATION', 'GENOTYPE'], )
fig2.update_layout(title='Fig2', font=dict(size=20))
fig2.update_traces(textinfo="label+percent root")
fig2.show()
fig2.write_html('fig2.html')
fig2.write_image('fig2.png')
