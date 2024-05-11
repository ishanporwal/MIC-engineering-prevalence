"""
Module: pytest

Pytest is a powerful testing framework for Python that provides a simple
and scalable approach to writing tests.

Usage:
import pytest

For detailed documentation and examples, refer to the Pytest documentation:
https://docs.pytest.org/en/stable/
"""

import pytest
from helpers import (
    clean_words_list,
    clean_bullet_list,
    find_keyword_matches,
    filter_links,
)
from keyword_list import military_terminology


word_list_test_cases = [
    # testing citation at the end of a sentence
    (
        ["Some", "example", "text", "has", "citations.[3]"],
        ["Some", "example", "text", "has", "citations"],
    ),
    # testing all puctuation
    (['.,:!?;"-()'], []),
    # testing all citation
    (["[1][2][3][4][5]"], []),
    # testing mix of citation and puctuation as invididual words
    (["[1]", "!", "[3]", "..."], []),
    # testing one word as valid and other as punctuation
    (["Hello", "---"], ["Hello"]),
    # testing citation in the middle of sentence
    (
        ["Citation[3]", "here", "and", "punctuation", "here."],
        ["Citation", "here", "and", "punctuation", "here"],
    ),
]


@pytest.mark.parametrize("words_list, correct", word_list_test_cases)
def test_clean_words_list(words_list, correct):
    """
    Tests that each scraped word is correctly filtered to keep every word with
    punctuation and citations removed. Test is passed if the test case result
    matches the correct result. If it doesn't, an error is thrown.

    Args:
        words_list: a list of strings representing an unfiltered sentence split
            into single words by the space character.
        correct: a list of strings representing correctly filtered words
            without punctuation or citations.
    """
    result = clean_words_list(words_list)
    correct_result = correct
    assert result == correct_result


# No need to test find_bullet_words()

bullet_list_test_cases = [
    # Testing short sentence list with punctuation and citation
    (
        [
            "Sometimes, example text has citations.[3][5]",
            "Tried so hard, but in the end, it doesn't even matter![123]",
        ],
        [
            "Sometimes",
            "example",
            "text",
            "has",
            "citations",
            "Tried",
            "so",
            "hard",
            "but",
            "in",
            "the",
            "end",
            "it",
            "doesn't",
            "even",
            "matter",
        ],
    ),
    # Testing only punctuation in an unordered list
    (['.,:!?;"-()', ".,.,.,.,.,.!", "???????????"], []),
    # Testing an unordered list of just citations
    (["[1][2][3][4][5]", "[1234123412341234]"], []),
    # Testing unoredered list of both exclusively citations and punctuation
    (["[1]", "!", "[3]", "..."], []),
    # Testing where 1 bullet point needs no modification
    (["Hello World", "---", "...", "()()()"], ["Hello", "World"]),
]


# Unit tests for clean_bullet_list()
@pytest.mark.parametrize("bullet_list, correct", bullet_list_test_cases)
def test_clean_bullet_list(bullet_list, correct):
    """
    Tests that each scraped unordered list is correctly filtered to keep every
    word with punctuation and citations removed. Test is passed if the test case
    result matches the correct result. If it doesn't, an error is thrown.

    Args:
        bullet_list: a list of strings representing the words of an unfiltered
            unordered list split by the space character.
        correct: a list of strings representing correctly filtered words with
            no punctuation or citations of all the unordered lists in the
            article.
    """
    result = clean_bullet_list(bullet_list)
    correct_result = correct
    assert result == correct_result


keyword_test_cases = [
    # Testing where the only word is a keyword
    (["aircraft"], 1),
    # Testing where the sentence sentence has all keywords
    (["aircraft", "army", "navy", "war"], 4),
    # Testing where there is only 1 keyword in a sentence
    (["That's", "not", "Patrick,", "that's", "an", "aircraft"], 1),
    # Testing no keywords detected
    (["Hello", "world", "I", "love", "you"], 0),
]


# Unit tests for keyword matches()
@pytest.mark.parametrize("words_list, count", keyword_test_cases)
def test_find_keyword_matches(words_list, count):
    """
    Tests that all keyword detected in the scraped and filtered paragraphs and
    unordered lists are accounted for. Test is passed if the test case result
    matches the correct result. If it doesn't, an error is thrown.

    Args:
        words_list: a list of strings representing individual words of filtered
            paragraphs and unordered lists.
        count: an integer representing the correct amount of keywords in each
            test case.
    """
    result = find_keyword_matches(words_list, military_terminology)[0]
    correct_result = count
    assert result == correct_result


# No need to test find_links()

test_links_cases = [
    # Testing when there is only 1 valid link in a list
    (
        [
            "/wiki/Aerospace-engineering",
            "invalid1",
            "invalid2",
            "invalid3",
            "invalid4",
        ],
        ["/wiki/Aerospace-engineering"],
    ),
    # Testing when theres no valid links
    (["invalid1", "invalid2", "/wiki/Main_page", "/wiki/invalid:"], []),
    # Testing when there is a mix of valid and invalid links
    (
        ["/wiki/test1", "/wiki/test2:", "/wiki/Main_page", "/wiki/test4"],
        ["/wiki/test1", "/wiki/test4"],
    ),
    # Testing when there are all valid links
    (
        [
            "/wiki/test1",
            "/wiki/test2",
            "/wiki/test3",
            "/wiki/test4",
            "/wiki/test5",
        ],
        [
            "/wiki/test1",
            "/wiki/test2",
            "/wiki/test3",
            "/wiki/test4",
            "/wiki/test5",
        ],
    ),
]


# Unit tests for filter_links()
# Testing when there is only 1 valid link in a list
@pytest.mark.parametrize("link_list, correct", test_links_cases)
def test_filter_links(link_list, correct):
    """
    Tests that the filtered link list only includes necessary links that lead
    to relevant subpages within that actual article that can be scraped. Test
    is passed if the test case result matches the correct result. If it
    doesn't, an error is thrown.

    Args:
        link_list: a list of strings containing every link that was scraped in
            the wikipedia article.
        correct: a list of strings containing correctly filtered links.
    """
    result = filter_links(link_list)
    correct_result = correct
    assert result == correct_result
