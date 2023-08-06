import webbrowser
import requests
from bs4 import BeautifulSoup


def random_dad_joke():
    url = "https://icanhazdadjoke.com/"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('p').text)

def programming_joke():
    url = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"
    response = requests.request("GET", url)
    print(response.text)

class HelpNFeedBack:
    def Give_FeedBack(name, message):
        webbrowser.open(f"mailto:hahacoolguystaco@gmail.com?subject=FEEDBACK&body={message}%0D%0A%0D%0AFrom%20{name}")

    def Help(self):
        webbrowser.open("https://readthedocs.org/projects/joking/")

def chuck_norris_jokes():
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    print(response.json().get('value'))

def random_joke():
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"
    response = requests.request("GET", url)
    print(response.text)

def JOD():
    url = "https://jokes.one/joke-of-the-day/jod"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('p').text)
    return soup.find('p').text

def Multiple_Jokes(n):
    for i in range(n):
        url = "https://icanhazdadjoke.com/"
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "html.parser")
        print(soup.find('p').text)

def sjoke(Joke_id):
    url = f"https://icanhazdadjoke.com/j/{Joke_id}"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('p').text)
    return soup.find('p').text

def search_for_joke(Search_term):
    url = f"https://icanhazdadjoke.com/search?term={Search_term}"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('td').text)
    return soup.find('td').text

def Random_knock_knock_joke():
    import random
    ran_int = random.randint(1, 148)
    url = f"http://www.jokes4us.com/knockknockjokes/random/knockknock{ran_int}.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('font').text)

def skkjoke(Joke_id):
    url = f"http://www.jokes4us.com/knockknockjokes/random/knockknock{Joke_id}.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('font').text)
    return soup.find('font').text

def DarkJoke():
    url = "https://v2.jokeapi.dev/joke/Dark?format=txt"
    response = requests.request("GET", url)
    print(response.text)

def Pun():
    url = "https://v2.jokeapi.dev/joke/Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"
    response = requests.request("GET", url)
    print(response.text)

def Submit_joke(Q, Punchline, Your_name="Anonymous", twitter="@Null"):
    url = "https://backend-omega-seven.vercel.app/api/addjoke"
    payload = {
        "name": Your_name,
        "twitter": twitter,
        "question": Q,
        "punchline": Punchline
    }
    response = requests.request("POST", url, json=payload)
    print(response.text)
    return response.text

def yo_mama_joke_slash_insults():
    import random
    Joke_id = random.randint(1, 1000)
    url = f"http://www.jokes4us.com/yomamajokes/random/yomama{Joke_id}.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.find('font').text)
    return soup.find('font').text

def animal_joke():
    import random
    idtouse = random.randint(1, 29)
    idtouse = f"https://retoolapi.dev/NyRMHE/anijokes/{idtouse}"
    response = requests.get(idtouse)
    print(response.json().get(' Jokes'))

def Meme(Subreddit=""):
    url = f"https://meme-api.herokuapp.com/gimme/{Subreddit}"
    print(url)
    response = requests.request("GET", url)
    dict = response.text
    import json
    test_string = dict 
    dict = json.loads(test_string)
    Meme_url = dict.get('url')
    print(Meme_url)
    return Meme_url

__version__ = '3.0.0'