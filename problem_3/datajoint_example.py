#!/usr/bin/env python
# coding: utf-8

# # An example of a data pipeline written in datajoint

# Datajoint is a tool to describe relational databases in python or matlab. It allows scientists, who are often not very experienced with databases, to communication with a SQL database. Some more info can be found here:
# 
# https://tutorials.datajoint.io/
# 
# https://docs.datajoint.io/python/

# In[1]:


import datajoint as dj
import pylab as pl
import numpy as np
from scipy import stats


# After installing a local SQL server [like MariaDB] you should be able to connect to it.

# In[2]:


dj.conn()


# ## 1) Defining the relational structure of the database

# Define the schema to work in

# In[25]:


schema = dj.schema('manuel_test')


# And the relational structure of the database. This database contains users that run experiments. Every experiment contains a data set with datapoints; these datapoints are analyzed and the result saved back in the database.
# 
# There are four allowed types of tables: Lookup, Manual, Imported and Part. The construction of the database is done by the definitions in the definition string. Lookup and Manual allow to specify all relevant components. Imported and computed run a function to populate the database automatically

# In[26]:


@schema
class User(dj.Lookup):
    definition = """
    # users in the lab
    username : varchar(20)      # user in the lab
    ---
    first_name  : varchar(20)   # user first name
    last_name   : varchar(20)   # user last name
    """
    contents = [
        ['Angus', 'Angus', 'Macguyver'],
        ['John', 'John', 'Doe'],
    ]

@schema
class Experiment(dj.Manual):
    definition = """ # A simple experiment.
    -> User
    experiment : int    # allowed here are sql datatypes.
    ----
    """
    
@schema
class Set(dj.Imported):
    definition = """
    # A set of datapoints
    -> Experiment
    -----
    """

    class DataPoint(dj.Part):
        definition = """
        # Collected data.
        -> Set
        datapoint : int
        -----
        x : float
        y : float
        """

    def _make_tuples(self, key):
        # Note that Imported and Computed (below) have a function _make_tuples
        # This allows to call a method s.populate() to automatically populate the data with content.
        n = 10
        mu = 0
        sigma = .1
        self.insert1(key)
        # Insert all of our datapoints
        b = []
        for i in range(n):
            b.append(dict(key, datapoint=i, x=i + np.random.normal(mu, sigma), y=2*i + np.random.normal(mu, sigma)))
        self.DataPoint().insert(b)


# Datajoint allows to plot an entity relationship diagram. This shows explicitly what we have just described:

# In[27]:


dj.ERD(schema)


# The different colors indicate different table types. Gray is lookup, green is manual, blue is Imported and red (which we will see below) is computed. This entity relationship diagram describes how data is ultimately organized in the relational database. The next step is the population of the database with data.

# ## 2) Generate content for the database

# The first think to enter into the databse are two experimenters, and their first experiment. With datajoint, we use the method .insert()

# In[28]:


Experiment().insert((['Angus',1],['John',1]), skip_duplicates = True)


# In[29]:


Experiment() #Shows the current content of the database


# Now that we have two experiments defined, we can populate the datasets for the experiment. This is done with the .populate() command.

# In[30]:


Set().populate()


# In[31]:


Set() # Now there are two datasets in the database


# In[32]:


Set().DataPoint() # With a set of datapoints


# One of the reasons that datajoint is popular is that it allows users to make SQL queries without even noticing it, e.g.

# In[33]:


Experiment() & 'username = "Angus"'


# # 3) Compute in the database.

# First, we add a new table to the database that fits a line

# In[34]:


@schema
class Fitparameters(dj.Computed):
    definition = """
    # calculates the fitparameters
    -> Set
    -----
    slope : float
    offset: float
    """
    def _make_tuples(self, key):
        data  = (Set().DataPoint() & key)
        x, y = data.fetch('x','y')
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        self.insert1(dict(key, slope = slope, offset = intercept))


# Check that it appeared in the entity relationship diagram:

# In[36]:


dj.ERD(schema)


# After the definition we can call the populate function and read out the results

# In[23]:


Fitparameters().populate()
Fitparameters()


# If you use a database management tool, like Sequel Pro, or you connect to the database, you should be able to see the data directly.

# In[ ]:




