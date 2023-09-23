# Movie Semantic search engine
In this file I will briefly explain how this library works as well as how to use it!
## The AI
This search engine uses pretrained LLMs . The chosen LLM for this system is based on the BERT model.
### All-MiniLM-L6-v2
This is a BERT based [sentence-transformers](https://www.sbert.net/) model: It maps sentences & paragraphs to a 384 dimensional dense vector space and can be used for tasks like clustering or semantic search. 
#### Why choose this model?
Our goal is to use a bert based model for semantic search, and this is the best performing model for this task, especially compared to its base model that isn't specialized in this task.
#### What is the size of this model? 
This model is way smaller than the basic bert model bert-base-uncased(1.5 gb), with only 90mb of size.
#### What is our task? 
The task that we are treating right now is sentence similarity, that is why using a proper sentence bert model will give better results.<br>
The sentence similarity is calculated through cosine similarity between the embeddings of 2 sentences.<br>
Using this sbert model, we will be iterating through a dataset and calculate the cosine similarity between the input query (input movie plot) and all the values in our dataset (plots of the dataset) and return the k highest scores.

### The dataset
As a dataset, we used the [Wikipedia Movie Plots](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots). It is a dataset with 34886 instances of different movies from the year 1901 to 2017 with their according title, release year, plot and other informations such as directors, casts, wiki pages etc...

## Folder structure
This project has been organized in order to keep all files separate in their proper folders, here is how to navigate it:

 - data:
	 - data.csv: the raw wikipedia movie plots dataset as is from kaggle.
	 - preprocessed_data.csv: the preprocessed version of the dataset, cleaned from columns we do not need.
	 - preprocess.py: the preprocessing python script to generate the preprocessed dataset csv file.
 - documentation: 
	 - ReadMe.md: this current file you're reading!
	 - references.bib: bibtex file containing all the references used to develop this system
 - models:
	 - sentence-transformers_all-MiniLM-L6-v2: the folder containing our model.
 - src: 
	 - setup:
		 - .env: environment file with all sensitive info and variables such as paths for easy modification.
		 - requirements.txt: contains all the dependencies and versions of the different modules used.
		 - runtime.txt: in case of deployment, knows which python version works.
	 - utils.py: contains all the helper functions and all the code needed to make the system function.
	 - main.py: the file to run and pass the arguments to, in order to use the search engine, executes the code and creates a json file of the output in the same folder.
	 - output.json: the output file with the search results, it will be generated after the main.py file is run and a search is executed.
## How to use

1. Open Command prompt console in the src folder (same as main.py).
2. Type the following command: <br>
<code>python main.py k plot release_year genre</code>
3. Replace the argument names with your values, make sure that strings should be in between quotes ("").
4. The output will be saved in the output.json file in the same folder.

##### Note: the arguments should NOT be separated by a comma, make sure to use double quotes for strings not apostrophes ('').
<br>

#### Example prompt:
<code>python main.py 5 "a father is too busy with his work and neglects his daughter, until the solution to all his work's financial problems is his daughter's imaginary world" 2009 "comedy"</code>
