
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


data = pd.read_csv('dog_rates_tweets.csv')
data


# In[3]:


datanew = data['text'].str.contains(r'(\d+(\.\d+)?)/10')
datanew


# In[4]:


data = data[datanew]


# In[5]:


dates = pd.to_datetime(data['created_at'])
dates


# In[6]:


ratings = data['text'].str.extract(r'(\d+(\.\d+)?)/10')[0]


# In[8]:


plt.scatter(dates.values, ratings)
plt.ylim(0,25)
plt.xticks(rotation=25)
plt.show()

