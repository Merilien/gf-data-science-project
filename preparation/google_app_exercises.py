#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np
import pandas as pd

db = pd.read_csv("C://ws/googleplaystore.csv")


# In[15]:


# fix skewed row
#db.loc[10472]
db.loc[10472] = db.loc[10472].shift(periods=1, freq=None, axis=0)
db.loc[10472, "Rating"] = np.float64(db.loc[10472, "Rating"])
db.loc[10472, "App"] = "Life Made WI-Fi Touchscreen Photo Frame"
db.loc[10472, "Category"] = np.nan
#db.loc[10472]


# In[16]:


# cleanings
db= db.drop_duplicates()


# In[17]:


#db.loc[db.duplicated(["App","Current Ver"], keep=False)].sort_values(by="App")


# In[18]:


def clean_installs(row):
    installs = row.Installs.replace(",","")
    if installs[-1] == "+":
        row.Installs = installs[0:-1]
    return row

db = db.apply(clean_installs, axis="columns")
db.Installs = db.Installs.astype(int)


# In[19]:


db.Reviews = db.Reviews.astype(int)
db.Rating.map(lambda r: np.float64(r))
db["Last Updated Readable"] = pd.to_datetime(db["Last Updated"])


# In[21]:


# least reviewed apps
db.loc[db.Reviews == db.Reviews.min()]
# mingroup = db.loc[db.Reviews == db.Reviews.min()]
# mingroup.loc[:,"App"].head()


# In[8]:


# rating descriptions
print("Mean: " + str(db.Rating.mean()) + "\nMedian: " + str(db.Rating.median()) + "\nMode: " + str(db.Rating.mode()))


# In[9]:


# size descriptions
import re

def calculate_bytes(row):
    size = row.Size.lower()
    if not re.match(r'^\d*\.?\d+[km]*$', size):
        row.Size = np.nan
    elif "k" in size:
        row.Size = np.float64(size[:-1]) * 1024
    elif "m" in size:
        row.Size = np.float64(size[:-1]) * 1024**2
    else:
        row.Size = np.float64(size)
    return row

db = db.apply(calculate_bytes, axis="columns")


# In[10]:


print(str(db.Size.mean()) + "\n" + str(db.Size.median()) + "\n" + str(db.Size.mode()))


# In[11]:


dict_list = [] #[{key:np.nan for key in db.columns}]

# genres with most installs
def make_dicts(row):
    global dict_list
    d = row.to_dict()
    if type(d["Genres"]) is str:
        cats = set(d["Genres"].split(';'))
        for cat in cats:
            newrow_dict = d.copy()
            newrow_dict["Genres"] = cat
            dict_list.append(newrow_dict)
    else:
        dict_list.append(d)
    return row

db.apply(make_dicts, axis="columns")
db2 = pd.DataFrame(dict_list)
db2 = db2.drop_duplicates()
db2.head(100)


# In[24]:


db.iloc[::-1].reset_index(drop=True).to_csv("reversed_app_data")


# In[ ]:




