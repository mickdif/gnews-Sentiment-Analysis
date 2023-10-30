from gnews import GNews
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# google_news = GNews()
google_news = GNews(language='it', country='IT', period='100d', max_results=100)
# pakistan_news = google_news.get_news('Telecom italia')
# print(pakistan_news[0])
q = 'Telecom italia'
json_resp = google_news.get_news(q)

# article = google_news.get_full_article(json_resp[2]['url'])  

# for idx in range(len(json_resp)):
#     article = google_news.get_full_article(json_resp[idx]['url'])
#     text = article.text
#     print(text)

# text = article.text
# print(text)

polarity_tot=0
polarity_verbose = ''
polarity_pos=0
polarity_neg=0
polarity_neutral=0
subjectivity_tot=0
subjectivity_verbose = ''
i = 0

print("ciao")

for idx in range(len(json_resp)):
    article = google_news.get_full_article(json_resp[idx]['url']) # newspaper3k instance, you can access newspaper3k all attributes in article
    
    try:
        text = article.text
        if idx == 0: # ESEMPIO
            print(text)
        analysis = TextBlob(text)
        polarity_tot = analysis.sentiment.polarity + polarity_tot
        subjectivity_tot = analysis.sentiment.subjectivity + subjectivity_tot
        i += 1 
        if analysis.sentiment.polarity < 0:
            polarity_neg += 1
        elif analysis.sentiment.polarity == 0:
            polarity_neutral += 1
        else:
            polarity_pos += 1
        
        print(analysis.sentiment)
    except:
        print("continua")
        continue
    
    


# ricorda: polarity va [-1.0 , +1.0] mentre subjectivity [0.0 , 1.0]
# polarity -1.0 negativa, polarity +1.0 positiva
# subjectivity 0.0 very objective, +1.0 very subjective

try:
    polarity_avg=polarity_tot/i
    
    if polarity_avg < 0:
        polarity_verbose = 'Negative sentiment'
    else:
        polarity_verbose = 'Positive sentiment'

    subjectivity_avg=subjectivity_tot/i
    if subjectivity_avg < 0.5:
        subjectivity_verbose = 'Objective sentiment'
    else:
        subjectivity_verbose = 'Subjective sentiment'

    print('\nTot. Polarity for', q , 'is:' , polarity_tot,
          '\nThe avg polarity is: ', polarity_avg, '(', polarity_verbose, ')')
    
    print('\nTot. Subjectivity for', q , 'is:' , subjectivity_tot,
          '\nThe avg polarity is: ', subjectivity_avg , '(', subjectivity_verbose, ')'
          '\non a number of tweets: ', i)

except:
    print('Zero tweet available... Try another #tag')


# Creazione del grafico a barre
sentiments = ["Positive",  "Negative"]
fig , ax = plt.subplots()

counts = [polarity_pos,  polarity_neg]
bar_colors = ['tab:green',  'tab:red']
ax.bar(sentiments, counts, color=bar_colors)
plt.show()

