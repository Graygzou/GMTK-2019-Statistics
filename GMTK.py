# Reading an excel file using Python
# In order to export graph into images
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import chart_studio.plotly as py
import plotly.tools as tls
# Others
import urllib.request, json
with urllib.request.urlopen("https://itch.io/jam/10205/results.json") as url:

###### Actual code #########
    # raw score mean
    mean_raw_score = 0
    # rating count mean
    total_nb_rating = 0
    mean_rating_count = 0
    # score mean
    mean_score = 0
    
    games = json.loads(url.read().decode())['results']
    number_of_rating = {}
    ratings_top_100 = {}
    for game in games:
        nbRating = game['rating_count']
        mean_raw_score += game['raw_score']
        total_nb_rating += game['rating_count']
        
        mean_score += game['score']
        # Group by the number of rating
        if not nbRating in number_of_rating.keys():
            number_of_rating[nbRating] = 1
        else:
            number_of_rating[nbRating] += 1
            
        if game['rank'] < 100:
            #print(game['title'])
            if game['rating_count'] < 20:
                if not "below 20" in ratings_top_100.keys():
                    ratings_top_100["below 20"] = 1
                else:
                    ratings_top_100["below 20"] = ratings_top_100["below 20"] + 1
            elif game['rating_count'] >= 20 and game['rating_count'] < 40:
                if not 'between 20 included and 40 excluded' in ratings_top_100.keys():
                    ratings_top_100['between 20 and 40'] = 1
                else:
                    ratings_top_100['between 20 and 40'] += 1
            elif game['rating_count'] >= 40 and game['rating_count'] < 60:
                if not 'between 40 included and 60 excluded' in ratings_top_100.keys():
                    ratings_top_100['between 40 and 60'] = 1
                else:
                    ratings_top_100['between 40 and 60'] = ratings_top_100['between 40 and 60'] + 1
            elif game['rating_count'] >= 60:
                if not 'above 60' in ratings_top_100.keys():
                    ratings_top_100['above 60'] = 1
                else:
                    ratings_top_100['above 60'] = ratings_top_100['above 60'] + 1

    # Fill not existing cumulated rating with 0
    print(max(number_of_rating.keys()))
    for existing_rating in range(0, max(number_of_rating.keys())):
        if not existing_rating in number_of_rating.keys():
            number_of_rating[nbRating] = 0

      
    mean_raw_score /= len(games)
    mean_rating_count = total_nb_rating / len(games)
    mean_score /= len(games)

    ##################################################
    ## General basic information
    ##################################################
    print("===================================")
    print("Number of submissions : " + str(len(games)))
    print("===================================")
    print("Total number of ratings : " + str(total_nb_rating))
    print("===================================")
    print("raw score mean = " + str(mean_raw_score))
    print("rating count mean = " + str(mean_rating_count))
    print("score mean = " + str(mean_score))

    ##################################################
    ####### Number of games per ratings number #######
    ##################################################
    fig, ax = plt.subplots()
    
    height = []
    bars = []
    for rating_num in range(max(number_of_rating.keys())):
        if not rating_num in number_of_rating.keys():
            height.append(0)
        else:
            #print(str(rating_num) + " => " + str(number_of_rating[rating_num]))
            height.append(number_of_rating[rating_num])
        bars.append(rating_num)
    y = np.arange(len(bars))

    plt.bar(y, height, color = (0.5,0.1,0.5,0.6))
    plt.title('Number of games per ratings number')
    plt.xlabel('number of ratings received')
    plt.ylabel('number of games')
    plt.xticks(y, bars) 
    plt.show()
    fig.savefig('nb_games_per_rating.png')


    ##########################################################
    ####### Number of games per ratings number percent #######
    ##########################################################
    x = []
    y = []
    cumulate_y = 0.0
    for rating_num in range(max(number_of_rating.keys())):
        if not rating_num in number_of_rating.keys():
            cumulate_y += 0.0
        else:
            print(number_of_rating[rating_num] * rating_num / total_nb_rating)
            cumulate_y += (number_of_rating[rating_num] * rating_num) / total_nb_rating
        x.append(rating_num)
        y.append(cumulate_y)
        
    plt.plot(x,y)
    plt.title('Number of games per ratings number in percentage')
    plt.xlabel('number of ratings received')
    plt.ylabel('number of games')
    plt.show()
    fig.savefig('cumulated_number_of_rating.png')
