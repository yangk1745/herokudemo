#!/usr/bin/env python
# coding: utf-8

# 
# 
# 
# Kuo Yang
# Modified 5/21
# FAERS
# data source: FDA Adverse Events Reporting System (FAERS, from FDA.gov)
# filtered for dulaglutide, exenatide, liraglutide, semaglutide, tirzapetide, all cases, accessed 5/19/25

# Disclaimer: This is for academic coursework ONLY. Do not use for clinical decision making; no causations implied in analysis. See end of document for full disclosure/disclaimer.

# In[2]:


import numpy as np
import pandas as pd
import hvplot.pandas
import holoviews as hv
import panel as pn
hv.extension('bokeh')
pn.extension('tabulator')
from bokeh.models.formatters import NumeralTickFormatter
#pn.extension(sizing_mode='stretch_width')


# In[3]:


#read csv
#glp1dfa = pd.read_csv('glp1dfa.csv')
glp1dfa = pd.read_csv('https://raw.githubusercontent.com/yangk1745/GLP1/refs/heads/main/glp1dfa.csv')


# In[59]:


#glp1dfa.head()


# In[60]:


#frqt = glp1dfa['Serious'].value_counts()
#print(frqt,'\n*******')

#Using groupby to count frequencies across all combinations; this is data pipeline
#frqt2 = glp1dfa.groupby(['Serious', 'Sex']).size().reset_index(name='Count')
#print(frqt2)
#print(frqt2.columns)


#Multi-level cross-tabulation
#print("\nMulti-level cross-tabulation (Susp Pro API, Serious, Sex, Compounded Flag)")
#frqt_mt = pd.crosstab([glp1df2['Sex'],glp1df2['Compounded Flag'],glp1df2['Suspect Product Active Ingredients']], glp1df2['Serious'])
#print(frqt_mt)


#frqt2_multi_index = frqt2.query("yr<=80").groupby(['yr', 'origin']).mean(numeric_only=True)
#autompg_multi_index.head()

#frqt3 = frqt2.reset_index()
#print(frqt3)
#print(frqt3.columns)
#frqt3.head()
#frqt3m = frqt3.melt(id_vars=['Serious'],value_vars=['Female','Male','Not Specified'],var_name='Sex',value_name='Counts')
#print(frqt3m)


# In[4]:


#Plot1
#Data for plot1
plot1df = glp1dfa[['Serious','Sex','api1']]

#make data pipeline interactive (make frqt2 interactive)
idf = plot1df.interactive()

#Define Panel Widgets
api_w = pn.widgets.ToggleGroup(widget_type='box',name='Select GLP-1:',
                               options={'dulaglutide':1,'exenatide':2,'liraglutide':3,'semaglutide':4,'tirzepatide':5}, value=[1,2,3,4,5])
#combine pipeline and widgets
ipipeline = (
    idf[
    (idf.api1.isin(api_w))
    ]
    .groupby(['Serious','Sex']).size().reset_index(name='Count')
)

ibarplot1 = ipipeline.hvplot.bar(x='Serious',y='Count',by='Sex',stacked=True,color=['hotpink','lightskyblue','mediumpurple'],
                                 xlabel='Seriousness',ylabel='Number of Events',title='All Adverse Events',
                                yformatter=NumeralTickFormatter(format="0,0"))
#ibarplot1


# In[5]:


pn.extension('tabulator')
itable = ipipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, show_index=False)
#itable


# In[6]:


#Plot2
#Data for plot2
plot2df = glp1dfa[['died','Sex','api1','cpdf','age2','age3']]
plot2dfb = plot2df[plot2df['died'] == 1]
api_dict={1:'dulaglutide',2:'exenatide',3:'liraglutide',4:'semaglutide',5:'tirzepatide'}
plot2dfc = plot2dfb.copy()
plot2dfc['api2'] = plot2dfc['api1'].map(api_dict)
#plot2dfc.head()


# In[7]:


#plot2dfc.info()


# In[65]:


# Describe a numeric column
#print(plot2dfb['age3'].describe())


# In[66]:


#print(plot2dfc['api1'].unique())
#print(plot2dfc['api1'].dtype)


# In[7]:


#make data pipeline interactive (make frqt2 interactive)
idf2 = plot2dfc.interactive()

#Define Panel Widgets
cpd_w = pn.widgets.ToggleGroup(name='0=no, 1=yes',options=[0,1],
                               value=[0,1],button_type='success')

age_slider = pn.widgets.IntRangeSlider(name='Age Range (-1=missing; include to see all data)',start=-1,end=100,value=(18,90),step=1)

#combine pipeline and widgets
ipipeline2 = (
    idf2[
    (idf2.age3 >= age_slider.param.value_start) &
    (idf2.age3 <= age_slider.param.value_end)
    ]
    .groupby(['api2','Sex']).size().reset_index(name='Count')
)

ibarplot2 = ipipeline2.hvplot.bar(x='api2',y='Count',by='Sex',stacked=True,color=['hotpink','lightskyblue','mediumpurple'],
                                 xlabel='GLP-1',ylabel='Number of Events',title='Deaths',
                                yformatter=NumeralTickFormatter(format="0,0"))
#ibarplot2


# In[8]:


itable2 = ipipeline2.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, show_index=False)
#itable2


# In[10]:


#glp1dfa.head()


# In[9]:


#Plot3 Age violin plots
plot3df = glp1dfa[['api1','sex2','serious2','died','age3']].copy()

#serious3 column: 0=nonserious, 1=serious, 2=death
plot3df = plot3df[plot3df['age3'] > 0]
plot3df['serious3'] = plot3df['serious2'] + plot3df['died']
plot3dfa = plot3df[['api1','sex2','age3','serious3']]
#plot3dfa.head()


# In[10]:


#make data pipeline interactive (make frqt2 interactive)
idf3 = plot3dfa.interactive()

#Define Panel Widgets
srs_w3 = pn.widgets.ToggleGroup(widget_type='box',name='Outcomes:',
                               options={'Non-Serious':0,'Serious (excluding death)':1,'Death':2}, value=[0,1,2])

sex_w3 = pn.widgets.ToggleGroup(widget_type='box',name='Gender:',
                               options={'Male (=1)':1,'Female (=0)':0,'Unknown (=3)':3}, value=[0,1,3])

api_w3 = pn.widgets.ToggleGroup(widget_type='box',name='Select GLP-1:',
                               options={'dulaglutide (=1)':1,'exenatide (=2)':2,'liraglutide (=3)':3,'semaglutide (=4)':4,'tirzepatide (=5)':5}, value=[1,2,3,4,5])

grp_w3 = pn.widgets.ToggleGroup(widget_type='button',behavior='radio',name='Group By:',
                               options={'GLP-1':'api1','Gender':'sex2'}, value='api1')


#combine pipeline and widgets
ipipeline3 = (
    idf3[
    (idf3.serious3.isin(srs_w3) & (idf3.sex2.isin(sex_w3)) & (idf3.api1.isin(api_w3)))
    ]
)

vlnplot3 = ipipeline3.hvplot.violin(y='age3',by=grp_w3, c=grp_w3, xlabel=grp_w3 ,ylabel='Age (years)',title='Age Distributions')
#vlnplot3


# In[13]:


#Layout using Template
#template = pn.template.FastListTemplate(
#    title='GLP-1 Adverse Events', 
#    sidebar=["GLP-1:",api_w,'Age (age=-1: NA)',age_slider, 'Group by:',grp_w3,'Outcomes:', srs_w3, 'Gender:', sex_w3, 'GLP-1:',api_w3], 
#    main=[ibarplot1.panel(),itable.panel(), ibarplot2.panel(), itable2.panel(),vlnplot3.panel()]
#)
#template.servable()


# In[11]:


#Layout using Template
ldsc = "Please note that this dashboard was developed for academic coursework, and is intended for educational purposes ONLY. The information provided does NOT imply causation, safety, or efficacy. This tool does not provide medical advice and should not be used to diagnose, treat, cure, or prevent any disease. Always consult a qualified healthcare professional for any health-related concerns. No guarantees are made regarding the completeness, accuracy, or timeliness of the information provided. Full disclaimer: (https://www.fda.gov/drugs/fdas-adverse-event-reporting-system-faers/fda-adverse-event-reporting-system-faers-public-dashboard)"

template2 = pn.template.FastListTemplate(
    title='GLP-1 Adverse Events', 
    sidebar=['\u00A9 2025 Kuo Yang', 'CS 119 (Python), SP 2025, East Los Angeles College','Data source: FDA Adverse Events Reporting System (FAERS).', 'Variables Defined:','GLP-1: 1=dulaglutide, 2=exenatide, 3=liraglutide, 4=semaglutide, 5=tirzepatide','Gender: 1=M, 2=F, 3=Unknown', ldsc],
    main=[ pn.Row(api_w,ibarplot1.panel(),itable.panel()),
            pn.Row(pn.Column(age_slider,ibarplot2.panel()),itable2.panel()),
            pn.Row(pn.Column('X-axis Grouping:',grp_w3,'Filters:',srs_w3,sex_w3,api_w3),vlnplot3.panel())])
            
template2.servable()


# In[ ]:




