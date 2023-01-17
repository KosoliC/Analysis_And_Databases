from app import hello
from app import extract_sentiment
from app import text_contain_word
from app import bubblesort
import pytest


# def test_hello():
#     got = hello("Aleksandra")
#     want = "Hello Aleksandra"

#     assert got == want

# testdata1 = ["I think today will be a great day"]

# @pytest.mark.parametrize('sample', testdata1)
# def test_extract_sentiment(sample):

#     sentiment = extract_sentiment(sample)

#     assert sentiment > 0


# testdata2 = [
#     ('There is a duck in this text', 'duck', True),
#     ('There is nothing here', 'duck', False)
#     ]

# @pytest.mark.parametrize('sample, word, expected_output', testdata2)
# def test_text_contain_word(sample, word, expected_output):

#     assert text_contain_word(word, sample) == expected_output




testdata = [([4,6,2,1,7],[1,2,4,6,7])]

@pytest.mark.parametrize('list_to_sort , expected_output', testdata)
def test_bubblesort(list_to_sort, expected_output):

    assert bubblesort(list_to_sort) == expected_output