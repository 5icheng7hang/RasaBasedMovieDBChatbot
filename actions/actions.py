# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import csv
import random

import pandas as pd

from turtle import title
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet



class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []


#改（改变电影的是否看过，改变评分）
class ActionMarkWatched(Action):

     def name(self) -> Text:
         return "action_mark_watched"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            movieTitle = tracker.get_slot('movie_title')
            file = pd.read_csv('moviedb.csv', encoding = 'ISO-8859-1')

            ID = file.index[file['Title'] == movieTitle].tolist()

            print(ID)

            print(file.at[ID[0], 'Title'])

            file.at[ID[0], 'Is_Watched'] = 1

            file.to_csv('moviedb.csv')

            dispatcher.utter_message(text="movie marked!")
             # 此处代码
            

class ActionMarkRate(Action):

     def name(self) -> Text:
         return "action_mark_rate"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            movieTitle = tracker.get_slot('movie_title')
            personalRate = tracker.get_slot('movie_personal_rate')
            file = pd.read_csv('moviedb.csv', encoding = 'ISO-8859-1')

            ID = file.index[file['Title'] == movieTitle].tolist()

            file.at[ID, 'Personal_Rate'] = personalRate

            file.to_csv('moviedb.csv')
            dispatcher.utter_message(text="movie rated!")


class ActionMarkUnWatched(Action):

     def name(self) -> Text:
         return "action_mark_unwatched"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            movieTitle = tracker.get_slot('movie_title')
            file = pd.read_csv('moviedb.csv', encoding = 'ISO-8859-1')

            ID = file.index[file['Title'] == movieTitle].tolist()

            print(ID)

            print(file.at[ID[0], 'Title'])

            file.at[ID[0], 'Is_Watched'] = 0

            file.to_csv('moviedb.csv')

            dispatcher.utter_message(text="movie marked!")
             
class ActionListWatched(Action):

     def name(self) -> Text:
         return "action_list_watched_movies"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            file = pd.read_csv('moviedb.csv', encoding = 'ISO-8859-1')
            ID = file.index[file['Is_Watched'] == 1].tolist()

            reply = f"you have watched {len(ID)} movies so far, and they are: \n"
            for id in ID:
                print(file.at[id, 'Title'])
                reply += file.at[id, 'Title']
                reply += "\n"
            dispatcher.utter_message(reply)


            

         



#查（名字，类别，随机，日期，分数）
class Action_Title(Action):

     def name(self) -> Text:
         return "action_by_title_search"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movieTitle = tracker.get_slot('movie_title')

        with open('moviedb.csv', 'r', encoding = 'mac_roman') as file:
            reader = csv.DictReader(file)
            resultData = [row for row in reader if row['Title'] == movieTitle]
            movieNum = len(resultData)
            movieInfo = []
            for movie in resultData:
                movieInfo.append(movie['Overview'])
            
            

        if resultData: 
            reply  = f"{movieTitle}, yes: there're {movieNum} movies under this name, there's what them about: \n"
            reply += "\n\n".join(movieInfo)
            dispatcher.utter_message(reply)

        else: # the list is empty
            dispatcher.utter_message(f"I could not find {movieTitle}")

         

class Action_Genre(Action):

     def name(self) -> Text:
         return "action_by_genre_search"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movieGenre = tracker.get_slot('movie_genre')
        movieGenreStr = str(movieGenre)

        with open('moviedb.csv', 'r', encoding = 'mac_roman') as file:
            reader = csv.DictReader(file)
            # 此处的resultData是一个字典的列表，即符合条件的多条数据，每一条都为一个字典
            resultData = [row for row in reader if (movieGenre == row['Genre'])]
  


        if resultData: 
            finalAns = random.choice(list(resultData))
            reply  = f"check this {movieGenre} movie out: \n"
            reply += f"{finalAns['Title']}\n"
            reply += f"{finalAns['Overview']}"
            dispatcher.utter_message(reply)

            SlotSet("movie_title", finalAns['Title'])

        else: # the list is empty
            dispatcher.utter_message(f"I could not find {movieGenre} movies")

        


class Action_Random(Action):

     def name(self) -> Text:
         return "action_give_random_movies"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 


        with open('moviedb.csv', 'r', encoding = 'mac_roman') as file:
            reader = csv.DictReader(file)
            resultData = [row for row in reader]
            randomAns = random.choice(list(resultData))

            
        if resultData: 
            reply  = f"here's one random movies:\n {randomAns['Title']}\n "
            reply += f"this {randomAns['Genre']} movie came out in: {randomAns['Release_Date']}\n"
            reply += f"watched by {randomAns['Popularity']} people, and get {randomAns['Vote_Average']} out of 10"
            #reply += "\n\n".join(resultData)
            dispatcher.utter_message(reply)

            SlotSet("movie_title", randomAns['Title'])

        else: # the list is empty
            dispatcher.utter_message(f"I could not find")

         
class Action_check_date(Action):

     def name(self) -> Text:
         return "action_check_date"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movieTitle = tracker.get_slot('movie_title')

        with open('moviedb.csv', 'r', encoding = 'mac_roman') as file:
            reader = csv.DictReader(file)
            resultData = [row for row in reader if row['Title'] == movieTitle]
            movieNum = len(resultData)
            movieInfo = []
            for movie in resultData:
                movieInfo.append(movie['Release_Date'])
            
            

        if resultData: 
            reply  = f"{movieTitle}, there're {movieNum} movies under this name, there's when them came out: \n"
            reply += "\n\n".join(movieInfo)
            dispatcher.utter_message(reply)

        else: # the list is empty
            dispatcher.utter_message(f"I could not find {movieTitle}")
                    
class Action_check_rate(Action):

     def name(self) -> Text:
         return "action_check_rate"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movieTitle = tracker.get_slot('movie_title')

        with open('moviedb.csv', 'r', encoding = 'mac_roman') as file:
            reader = csv.DictReader(file)
            resultData = [row for row in reader if row['Title'] == movieTitle]
            movieNum = len(resultData)
            movieInfo = []
            for movie in resultData:
                movieInfo.append(movie['Vote_Average'])
            
            

        if resultData: 
            reply  = f"{movieTitle},wow there're {movieNum} movies under this name, here's how people rate them: \n"
            reply += "\n\n".join(movieInfo)
            dispatcher.utter_message(reply)

        else: # the list is empty
            dispatcher.utter_message(f"I could not find {movieTitle}")






            