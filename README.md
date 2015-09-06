# PennApps-F15 : Plaidypus

=============

**Each one of us has a unique personality that shines through in the way we communicate, most freely with our friends and peers. We decided to create Plaidypus, a personalized AI bot that reflects the styles and quirks of each user it meets.**

## What it does
Plaidypus is a fun loving bot that can take on the linguistics style of you or your friends. Pulling from a corpus of a user's past Facebook messages, Plaidypus picks up on many of the subtleties in dialogue that together characterize how each one of speak. In our app, Plaidypus can either take on as you, or any of your Facebook friends who have been with Plaidypus.

## What makes it different
Unlike traditional AI bots, Plaidypus does not just regurgitate random and largely irrelevant comments you made in the past. Rather, Plaidypus take the time to formulate a response, much like the way you do; Plaidypus considers different linguistic mannerisms for incorporating local slang, demonstrating knowledge of pop culture with gifs, and responding to articles you send.

## How we built it
For the backend natural language processing, we used a variety of toolkits such as NLTK for n-gram modeling & POS tagging, Indicoio for sentiment analysis, and coreNLP for named entity recognition. We also adapted algorithms such as tf-idf (term frequency-inverse document frequency) and applied specific knowledge of linguistics (ie. grammar, fillers, contractions, formality, etc.) to customize Plaidypus to take on each person it speaks to. 
On the frontend, our web app provides a clean interface for realtime interaction with Plaidypus, built on Django, react, grunt, browserify, es6, babel, and a number of other libraries. 

## Challenges & Accomplishments
- **Lack of data** : A challenge that came with our selection of Facebook messages for our base corpus was the limitation on quantity of data we could access. Since Plaidypus is built on the traits of individuals, we could not aggregate data from multiple users. As a result, we stepped away from a strictly objective data analysis approach; rather we chose to dive into different aspects of linguistics to build our own unique models for optimization.
- **Building an identity** : Another challenge was determining what role we would want our AI bot to play, and the personality we would instill. Throughout development, we kept the 4 qualities of humor, intelligence, practicality, and human-ness in mind, so we think Plaidypus has what it takes to be the second best version of you.

## What's next for Plaidypus?
To grow and learn.

# Development
- Running the web app development server is as simple as running `npm start`.
- To compile the source and watch for changes, run `grunt dev`.

Team
-----------------------------
```
Felipe Vargas
Animesh Ramesh
Ariel Rao
```
