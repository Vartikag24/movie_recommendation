from flask import (Flask,render_template,request,redirect,url_for,g,flash)
import difflib
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app=Flask(__name__,template_folder='templates')

df2=pd.read_csv('./model/tmdb.csv')

count=CountVectorizer(stop_words='english')
count_matrix=count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix,count_matrix)

df2=df2.reset_index()
indices=pd.Series(df2.index,index=df2['title'])
all_titles=[df2['title'][i] for i in range(len(df2['title']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['release_date'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','Year'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return return_df

#setup main route
@app.route('/',methods=['GET','POST'])

def main():
    if request.method=='GET':
        flag=0
        return (render_template('index.html',flag=flag))
    
    if request.method=='POST':
        m_name=request.form['movie_name']
        #print(m_name)
        m_name=m_name.title()
        check=difflib.get_close_matches(m_name,all_titles,cutoff=0.50,n=1)
        if m_name not in all_titles:
            flag=1
            return(render_template('index.html',name=m_name,flag=flag))
        else:
            flag=2
            result_final=get_recommendations(m_name)
            names=[]
            dates=[]
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                dates.append(result_final.iloc[i][1])
            #print(names)
            return render_template('index.html',flag=flag,movie_names=names,movie_date=dates,search_name=m_name)

if __name__=='__main__':
    app.run(debug=True)