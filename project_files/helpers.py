"""
Module: bs4.BeautifulSoup

Beautiful Soup is a Python library for pulling data out of HTML and XML files.
It provides simple methods and Pythonic idioms for navigating, searching,
and modifying the parse tree.

Usage:
from bs4 import BeautifulSoup

For detailed documentation and examples, refer to the Beautiful Soup
documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""

from bs4 import BeautifulSoup
import requests
from keyword_list import military_terminology


def scrape_page(title):
    """
    Scrapes the Wikipedia page of the specified title.

    Args:
        title: A string representing the title of the Wikipedia page to scrape.

    Returns:
        A BeautifulSoup object containing the parsed HTML content.
    """
    timeout = 60
    try:
        page = requests.get(
            f"https://en.wikipedia.org/wiki/{title}", timeout=timeout
        )
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
    except requests.exceptions.HTTPError as error:
        print(f"Failed to retrieve Wikipedia page: {error}")
        return None
    except requests.exceptions.Timeout:
        print("Timeout error: The request took too long to complete.")
        return None
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")
        return None


def get_words_from_paragraphs(soup):
    """
    Generates a list of words extracted from the paragraphs of HTML content
    of a page.

    Args:
        soup: A BeautifulSoup object containing the parsed HTML content.

    Returns:
        A list of strings containing the words extracted from the paragraphs
    """
    paragraphs = soup.find_all("p")
    words_list = []
    for paragraph in paragraphs:
        words = paragraph.get_text().split()
        words_list.extend(words)
    return words_list


def clean_words_list(words_list):
    """
    Filters out the punctation and citation from a list of words so that
    the words themselves can directly be accessed without interferences.

    Args:
        words_list: A list of words containign the words extracted from
        the content of a Wikipedia page

    Returns:
        A list of strings containing the words extracted from the paragraphs
        but this time without punctuation and citations.
    """
    # filters out punctuation and citations in the text of paragraphs
    cleaned_words_list = []
    filter_out = [".", ",", ":", "!", "?", ";", '"', "-", "(", ")"]
    skip_next = False

    for word in words_list:
        cleaned_characters = []
        skip_next = False  # Reset skip_next for each word
        i = 0  # Track the current position within the word
        while i < len(word):
            character = word[i]
            if skip_next:
                skip_next = False
                i += 1
                continue
            if character in filter_out:
                i += 1
                continue
            if character == "[":
                # Skip over the citation
                while i + 1 < len(word) and word[i + 1] != "]":
                    i += 1
                skip_next = True  # Skip the closing bracket ']'
                i += 1
                continue
            cleaned_characters.append(character)
            i += 1
        cleaned_word = "".join(cleaned_characters)
        if cleaned_word:
            cleaned_words_list.append(cleaned_word)
    return cleaned_words_list


def find_bullet_words(soup):
    """
    Finds and organizes text content of items in bulleted lists on pages into
    a list of words so that they can be analyzed without problems in formatting.

    Args:
        soup: A BeautifulSoup object containing the parsed HTML content.

    Returns:
        A list of strings containing the organized words from bulleted lists
        included in unordered lists.

    """
    bullet_lists = soup.find_all("ul")
    bullet_lists_organized = []
    for bullet in bullet_lists:
        if bullet.find_previous_sibling("p") and bullet.find_next_sibling("p"):
            for item in bullet.find_all("li"):
                cleaned_item = item.get_text().replace("\xa0–", "")
                bullet_lists_organized.append(cleaned_item)
    return bullet_lists_organized


def clean_bullet_list(bullet_lists_organized):
    """
    Cleans the list of organized words from bulleted lists by removing
    punctuation and citations.

    Args:
         soup: A BeautifulSoup object containing the parsed HTML content.

    Returns:
        A list of strings containing the words extracted from the paragraphs
    """
    # Convert to individual bullet words
    individual_bullet_words = []
    for bullet in bullet_lists_organized:
        words = bullet.split()
        individual_bullet_words.extend(words)
    # filter out punctuation and citations in the text of bullet lists
    cleaned_bullet_list = clean_words_list(individual_bullet_words)
    return cleaned_bullet_list


def find_keyword_matches(words_list, keyword_list):
    """
    Finds matches between a list of words and a list of keywords.

    Args:
        words_list: A list of words to search for matches.
        keyword_list: A list of keywords to match against.

    Returns:
        A tuple containing an integer representing the number of keyword
        matches found and a list of matched words found.
    """
    match_count = 0
    matched_words = []
    # searching for matches
    for word in words_list:
        lowercase_word = word.lower()
        if lowercase_word in keyword_list:
            match_count += 1
            matched_words.append(lowercase_word)
    return match_count, matched_words


def find_links(soup):
    """
    Finds all of the links within the content of a page.

    Args:
        soup: A BeautifulSoup object containing the parsed HTML content.

    Returns:
        A list of strings containing the found links.
    """
    # Find all links in the content
    list_links = []
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href:
            list_links.append(href)
    return list_links


def filter_links(list_links):
    """
    Filters out links that aren't subpages of the Wikipedia page.

    Args:
        list_links: A list of strings contianing the found links of potential
        subpages of the page.

    Returns:
        A filtered list of links containing only subpages of the Wikipedia
        page.
    """
    # Filter out links that don't start with "/wiki/"
    list_links_filtered = []
    for item in list_links:
        if item.startswith("/wiki/"):
            list_links_filtered.append(item)
    second_round_filter = ["/wiki/Main_page", ":"]
    filtered_list_links = []
    for item in list_links_filtered:
        should_keep = True
        for filter_item in second_round_filter:
            if filter_item in item:
                should_keep = False
                break
        if should_keep:
            filtered_list_links.append(item)
    return filtered_list_links


def find_all_matches(title):
    """
    Finds all matches of keywords within military terminology in a
    singular Wikipedia page.

    Args:
        title: A string representing the title a Wikipedia page.

    Returns:
        A tuple containing two lists of strings, one storing the
        matched words and the other storing all of the words
        parsed through. It also contains two integers, one representing
        the count of matched words and the other storing the count
        of all words parsed through.
    """
    all_matched_words = []
    total_match_count = 0
    total_words = []
    # scrape main page to create initial list of words
    soup = scrape_page(title)
    words_list = get_words_from_paragraphs(soup)

    # clean this list of words to filter punctuation and citations
    cleaned_words_list = clean_words_list(words_list)
    total_words += cleaned_words_list

    # bulleted words aren't included in paragraphs within wikipedia
    # these are handled separately

    bullet_lists = find_bullet_words(soup)
    cleaned_bullet_lists = clean_bullet_list(bullet_lists)
    total_words += cleaned_bullet_lists

    # finding matches for normal words list
    match_count_1, matched_words_1 = find_keyword_matches(
        cleaned_words_list, military_terminology
    )
    all_matched_words += matched_words_1
    total_match_count += match_count_1

    # finding matches for bullet words lists
    match_count_2, matched_words_2 = find_keyword_matches(
        cleaned_bullet_lists, military_terminology
    )
    all_matched_words += matched_words_2
    total_match_count += match_count_2
    total_word_count = len(total_words)

    return all_matched_words, total_match_count, total_words, total_word_count


def search_subpages(
    title,
    initial_matched_words,
    initial_match_count,
    initial_words,
    initial_word_count,
):
    """
    Searches all subpages of a Wikipedia page for matches of keywords within
    military terminology.

    Args:
        title: A string representing the title a Wikipedia page.
        initial_matched_words: A list containing words already matched
        in the main page.
        initial_match_count: An integer representing the count of matched words
        from the main page.
        initial_words: A list of words parsed through from the main page.
        initial_word_count: An integer representing the count of all words
        parsed through from the main page.

    Returns:
        A tuple containing two lists of strings, one storing the
        matched words and the other storing all of the words
        parsed through. It also contains two integers, one representing
        the count of matched words and the other storing the count
        of all words parsed through.
    """
    soup = scrape_page(title)
    links = find_links(soup)
    filtered_links = filter_links(links)
    for link in filtered_links:
        matched_words, match_count, words, word_count = find_all_matches(
            link[6:]
        )
        initial_matched_words += matched_words
        initial_match_count += match_count
        initial_words += words
        initial_word_count += word_count
    return (
        initial_matched_words,
        initial_match_count,
        initial_words,
        initial_word_count,
    )
