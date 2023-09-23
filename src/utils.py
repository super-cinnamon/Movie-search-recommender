# Imports

import os
import re

import pandas as pd
import numpy as np
import dotenv
import torch

from sentence_transformers import SentenceTransformer, util

'''
init -> no arguments
this function initializes the various variables this package file will be using
all variables are set as global so they can be used across all methods

no output
'''
def init():
        # Get paths and variables from .env file
        dotenv.load_dotenv('setup/.env')

        global data_path
        data_path = os.getenv('DATA_PATH')
        global model_path
        model_path = os.getenv('MODEL_PATH')
        
        global df
        df = pd.read_csv(data_path) # setting up the correct dataset

        global model
        if torch.version.cuda:
                model = SentenceTransformer(model_path, device='cuda')
        else:
                model = SentenceTransformer(model_path)
        # 

'''
preprocess_text_input -> input 

this method takes a string as an argument and uses regular expressions to clean it
it removes the symbols and any unwanted extra spaces in the input
the goal is to have a proper and clean string query to send to the model

returns string output
'''
def preprocess_text_input(input):
        input = re.sub(r"[^a-zA-Z0-9\s\.,!?']", "", input) # Only keep punctuation, letters and numbers, get rid of symbols
        input = re.sub(r"\s+", " ", input).strip() # Remove extra spaces
        return input.lower()

'''
format_output -> index, result arguments

this method takes in an int (index) and a float (result) arguments
it formats it into a list of values, the first one is a dict of the information we want to retrieve about the movies
the second is the score it got from the model

returns tuple of dict and result
'''
def format_output(index, result):
        output = ({
            'Title' : df.iloc[index]['Title'],
            'Year' : int(df.iloc[index]['Release Year']),
            'Genre' : df.iloc[index]['Genre']
            },
            result)
        return output

'''
prep_input -> release_year, genre

this method takes in an int or string (release_year) and a string (genre) arguments
the string arguments will be turned into lowercase
the release year argument can be a string, in that case it will processed the same way genre argument is 

returns processed inputs
'''
def prep_input(release_year, genre):
        if isinstance(release_year, str): release_year = release_year.lower()
        genre = genre.lower()
        return release_year, genre
        

'''
get_sub_df -> df, release_year, genre

this method takes in a pandas dataframe (df), int or string (release_year) and a string (genre) arguments
it will create a sub dataframe that only contains movies matching the given release_year and genre
if the relase year or genre are set as 'any' it will take in all the values possible in the dataframe

returns pandas dataframe
'''
def get_sub_df(df, release_year, genre):
        if genre == 'any' and release_year == 'any':
                sub_df = df
        elif genre == 'any':
                sub_df = df[(df['Release Year']==release_year)]
        elif release_year == 'any':
                sub_df = df[(df['Genre'].str.contains(genre))]
        else:
                sub_df = df[(df['Genre'].str.contains(genre)) & (df['Release Year']==release_year)]
        return sub_df

'''
get_moves -> k, plot, release_year, genre

this methoed takes in an int (k), a string (plot), int or string (release_year), and a string (genre) arguments
this is the main method of the util module is to use the model to retrieve the k top movies fitting the query
the plot string is the query itself and will be cleaned before use
the release year and genre are details needed to specify the genre and release year of the movie the user is looking for
once the results are retrieved from the model the function will sort them in a descending order
as the results are sorted, only the k first values are selected, and their score is removed from the output

returns list of dicts
'''
def get_movies(k, plot, release_year="any", genre='any'):
        # run init file to get all the variables
        init()
        # make sure the plot query is well formatted and the other inputs are correct
        plot = preprocess_text_input(plot)
        release_year, genre = prep_input(release_year, genre)

        sub_df = get_sub_df(df, release_year, genre)
        
        # make the embedding of the query
        query_embedding = model.encode(plot, convert_to_tensor=True)

        all_outputs = {}

        # iterating through the entire sub dataset
        for index, row in sub_df.iterrows():
                # creating the embedding of the current movie plot (from the dataset)
                embedding = model.encode(row['Plot'], convert_to_tensor=True)
                # use cosine similarity to compute the sentence similarity between the query and the plot
                result = util.pytorch_cos_sim(query_embedding, embedding)[0][0].item() # Retrieve the score from the tensor list
                # format the output as we need it as
                all_outputs[index] = format_output(index, result)

        # sort the results by score in a descending order and only return the top k
        sorted_movies = [item[1][0] for item in sorted(all_outputs.items(), key=lambda item: item[1][1], reverse=True)]
        return sorted_movies[:k]


