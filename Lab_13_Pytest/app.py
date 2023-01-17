from textblob import TextBlob
from typing import List,Tuple

def hello(name):
    output = f'Hello {name}'
    return output


def extract_sentiment(text):
    text = TextBlob(text)

    return text.sentiment.polarity

def text_contain_word(word: str, text: str):
    return word in text


def bubblesort(lst: List[int]) -> Tuple[List[int], int]:
    l = lst[:]
    n = len(lst)
    k = 0
    change = True
    while n > 1 and change:
        change = False
        for i in range (1,n):
            k += 1
            if l[i-1] > l[i]:
                l[i-1] , l[i] = l[i] , l[i-1]
                change = True
        n -= 1
    return l

