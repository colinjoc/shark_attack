import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data=pd.read_csv('attacks.csv', sep=',') # load the csv file using pandas

data = data.drop(['Case Number','Investigator or Source'], axis=1) # get rid of colums with boring data


def sex_comp():
    #comparison of the sexes
    NAN_sexes = data[data['Sex ']=='Nan']; NAN_len = float(len(NAN_sexes)) # entries where the sex isnt recorded
    male = data[data['Sex ']=='M']; male_len = float(len(male)) # males
    female = data[data['Sex ']=='F']; female_len = float(len(female)) # females
    total = len(data) 

    print("Total number of attacks: %s \nPercent Males: %s\nPercent Females: %s\nPercent unknown: %s"%(total, male_len/total,female_len/total,NAN_len/total))


def Age_comp():
    #Age comparison
    age_data = data['Age'] # only ages
    age_list = []
    # Could try fix a bit better!
    for x in range(len(age_data)):
        try: # this tries to turn the data into a number
            float(age_data[x])
            age_list.append(float(age_data[x]))
        except ValueError: # if it cant be turned into a number, it must be a string. We should break the data up into the different ways its recorded
            split = age_data[x].split(",")
            for age in split:
                if 'or' in age: # sometimes the data says stuff like "20 or 21"
                    age_list.append(float(age[0:2]))
                elif age[-1] == 's' and len(age)<5: # sometimes data says 30s. remove the s and put in 30
                    age_list.append(float(age[0:2]))
                elif age.lower()=='teen' : 
                    age_list.append(15)
                elif '&' in age: # might be more than one age 
                    num_list = age.split("&")
                    for num in num_list:
                        try: # try turn the individual entries into a number
                            float(num)
                            age_list.append(float(num))
                        except ValueError:
                            print "Error, listed entry:" num # print what it is so we can try add some code to analise it
                
                else:
                    print age # print what it is so we can try add some code to analise it


    age_float = pd.DataFrame(age_list, columns = ['Age']).dropna()
    age_float.hist() # plot a histogram
    plt.show()




def times():
    # Try figure out times of day
    day=0; night=0
    times={"morning":0,"evening":0,"afternoon":0,"night":0, 'hour list':[]} # this is a directory and we will use this to store data
    nan_count = 0
    time_dropna = data['Time'].dropna() # this gets rid of all NAN entries in the data column
    other=0

    for x in time_dropna.index:
        split = str(time_dropna[x]).split() # split the entries into the different words
        for word in split:    
            if word.lower()=='midday' or 'noon' in word.lower():
                times['afternoon']+=1
            elif 'night' in word.lower():
                times['night']+=1
            elif word.lower() in times.keys():
                times[word.lower()]+=1
            
            elif len(word)>=5 and word[2]=='h': # most of the data is stored as 01h30 for example. 
                hour = word[0:2] # just look at the hour
                try:
                    hour = float(hour)
                    
                    if hour<=6:
                        times['night']+=1
                    elif hour>6 and hour<=12:
                        times['morning']+=1
                    elif hour>12 and hour<=18:
                        times['evening']+=1
                    elif hour>18 and hour<=24:
                        times['night']+=1
                    else:
                        print hour 
                    times['hour list'].append(hour) # list of all hours processed
                except ValueError:
                    print word
                        
        
            else:
                print "Error: ",word
                other+=1
    plt.hist(times['hour list'],bins=range(0,25))# histogram of times
    plt.show()        
    
def year_hist(start_year=1900):
    # look at years
    years = list(data['Year'].dropna())
    new_years=[]
    for y in years:
        try:
            y = float(y)
            if y>start_year:
                new_years.append(y)            
        except ValueError:    
            print y
    plt.hist(new_years,bins=range(start_year,2017))
    plt.ylabel("Number of attacks")
    plt.xlabel("Year")
    plt.show()

def activity_plot(top_number):
    # look at what activity the victim was doing before they were attacked
    #top_number = 10
    from collections import Counter
    activity_counts = dict(Counter(data['Activity'].dropna()).most_common(top_number))
    df = pd.DataFrame.from_dict(activity_counts, orient='index')
    df=df.sort(columns=0,ascending=False)
    df.plot(kind='bar')
    plt.show()





