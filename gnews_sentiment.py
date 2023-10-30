from gnews import GNews # scrape
from deep_translator import GoogleTranslator # translate
from textblob import TextBlob # evaluate
import matplotlib.pyplot as plt # plot
import numpy as np
from textblob.en import subjectivity

# -----------------------------------------
# SETUP
query = 'Telecom Italia'
language = 'it'


google_news = GNews(language=language, country='IT', period='10d', max_results=30)
json_resp = google_news.get_news(query)

polarity_tot = 0
polarity_verbose = ''
polarity_pos = 0
polarity_neg = 0
polarity_neutral = 0
subjectivity_tot = 0
subjectivity_verbose = ''
well_read = 0 # articoli aperti senza errori
polarity_array = np.array('')
subjectivity_array = np.array('')


gt=GoogleTranslator(source='it', target='en')

for idx in range(len(json_resp)):
    article = google_news.get_full_article(json_resp[idx]['url']) # newspaper3k instance
    
    try:
        # open and translate
        text = article.text
        text = gt.translate(text=text)
        # print(article.text) # debug
        # print(text)

        # Sentiment Analysis
        # The sentiment property returns a namedtuple of the form Sentiment(polarity, subjectivity). 
        # The polarity score is a float within the range [-1.0, 1.0]. 
        # The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective. (from api reference)
        analysis = TextBlob(text)
        polarity_tot += analysis.sentiment.polarity
        polarity_array = np.append(polarity_array, analysis.sentiment.polarity)
        subjectivity_tot += analysis.sentiment.subjectivity
        subjectivity_array = np.append(subjectivity_array, analysis.sentiment.subjectivity)
        

        if analysis.sentiment.polarity < 0:
            polarity_neg += 1
        elif analysis.sentiment.polarity == 0:
            polarity_neutral += 1
        else:
            polarity_pos += 1
        
        print(analysis.sentiment) # debug
        
        well_read += 1 
    except: 
        continue # ignore exceptions


if well_read == 0:
    print('Error: can not open any news, or no news avaible.')
    print("EXIT")
    exit()
    
polarity_avg = polarity_tot / well_read
if polarity_avg < 0:    polarity_verbose = 'Negative sentiment'
else:   polarity_verbose = 'Positive sentiment'

subjectivity_avg = subjectivity_tot / well_read
if subjectivity_avg < 0.5:    subjectivity_verbose = 'Objective sentiment'
else:    subjectivity_verbose = 'Subjective sentiment'

print('\nTot. Polarity for', query , 'is:' , polarity_tot,
        '\nThe avg polarity is: ', polarity_avg, '(', polarity_verbose, ')')
    
print('\nTot. Subjectivity for', query , 'is:' , subjectivity_tot,
        '\nThe avg polarity is: ', subjectivity_avg , '(', subjectivity_verbose, ')'
        '\non ', well_read, 'news read')


# Creazione del grafico a barre
sentiments = ["Positive",  "Negative"]
fig , ax = plt.subplots()

counts = [polarity_pos,  polarity_neg]
bar_colors = ['tab:green',  'tab:red']
ax.bar(sentiments, counts, color=bar_colors)
plt.show()
