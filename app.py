from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

soup = BeautifulSoup(url_get.content,"html.parser")
list_movie = soup.find("div", attrs={"class","lister-list"})
temp = [] #initiating a tuple
for i in range (50):
#insert the scrapping process here   
    tab = list_movie.find_all("h3")[i]
    judul_film = tab.find_all("a")[0].text
    judul_film = judul_film.strip()
    tahun = list_movie.h3.find('span', class_ = "lister-item-year").text
    imdb_rating = list_movie.find_all("strong")[i].text
    metascore = soup.select(".ratings-bar , .ratings-metascore")
    metascore = [title.text for title in metascore]
    metascore = metascore[i].strip()
    metascore = metascore.replace(metascore[:59],"")
    metascore = metascore[6:8]
    votes = soup.select(".sort-num_votes-visible span:nth-child(2)")
    votes = [title.text for title in votes]
    votes = votes[i].replace(",","")
    temp.append((judul_film,tahun,imdb_rating,metascore,votes))
temp = temp[::-1]

#change into dataframe
import pandas as pd
df = pd.DataFrame(temp, columns = ("Judul","tahun","IMDB Rating","Metascore","Votes"))

#insert data wrangling here
df["Judul"] = df["Judul"].astype("category")
df["tahun"] = df["tahun"].astype("category").replace("– ","")
df["IMDB Rating"] = df["IMDB Rating"].astype("float64")
df["IMDB Rating"] = df["IMDB Rating"].replace("– ","")
df["Metascore"] = df["Metascore"].replace("",0)
df["Metascore"] = df["Metascore"].astype("float64")
df["Votes"] = df["Votes"].astype("float64")
rank_film = df.sort_values('IMDB Rating', ascending=False).head(7) #rank by IMDB Rating
top_film = rank_film.set_index('Judul').sort_values(['Votes'], ascending=False).head(7)


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'Top 7 Film by Votes {top_film.max().round(2)}'

	# generate plot
	ax = top_film[['IMDB Rating','Votes']].sort_values("Votes").plot.barh(figsize = (20,9),title='Top 7 Film 2019 by Votes')
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
