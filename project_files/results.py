"""
Module: matplotlib.pyplot

Matplotlib is a library for creating static, animated, and interactive
visualizations in Python
The `pyplot` module provides a MATLAB-like interface for creating plots
and visualizations.

Usage:
import matplotlib.pyplot as plt

For detailed documentation and examples, refer to the Matplotlib documentation:
https://matplotlib.org/stable/contents.html
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import helpers


def process_disciplines(engineering_disciplines):
    """
    Parses through engineering discipline Wikipedia pages and gathers
    the data of matched words against a list of military terminology keywords
    and total words and their counts for the first time. It then stores this
    data in a dictionary.

    Args:
        engineering_disciplines: A list containing the titles of the Wikipedia
        pages to parse through and find matches for.

    Returns:
        A dictionary containing two lists of strings, one storing the
        matched words and the other storing all of the words
        parsed through. It also contains two integers, one representing
        the count of matched words and the other storing the count
        of all words parsed through.
    """
    discipline_matches = {}
    for discipline in engineering_disciplines:
        title = discipline
        (
            initial_matched_words,
            initial_match_count,
            initial_words,
            initial_word_count,
        ) = helpers.find_all_matches(title)
        (
            final_matched_words,
            final_match_count,
            total_words,
            total_word_count,
        ) = helpers.search_subpages(
            title,
            initial_matched_words,
            initial_match_count,
            initial_words,
            initial_word_count,
        )

        discipline_matches[discipline] = {
            "final_matched_words": final_matched_words,
            "final_match_count": final_match_count,
            "total_words": total_words,
            "total_word_count": total_word_count,
        }
    return discipline_matches


def write_to_files(discipline_matches):
    """
    Writes the contents of the created dictionary to text files.

    Args:
        discipline_matches: A dictionary containing two lists of strings,
        one storing the matched words and the other storing all of the
        words parsed through. It also contains two integers, one
        representing the count of matched words and the other storing the
        count of all words parsed through.

    Returns:
        None
    """
    # Write final matched words to a file
    with open("data/final_matched_words.txt", "w", encoding="utf-8") as file:
        for discipline, results in discipline_matches.items():
            file.write(
                f"{discipline}: {' '.join(results['final_matched_words'])}\n"
            )
    # Write total words to a file
    with open("data/total_words.txt", "w", encoding="utf-8") as file:
        for discipline, results in discipline_matches.items():
            file.write(f"{discipline}: {' '.join(results['total_words'])}\n")
    # Write final match counts to a file
    with open("data/final_match_counts.txt", "w", encoding="utf-8") as file:
        for discipline, results in discipline_matches.items():
            file.write(f"{discipline}: {results['final_match_count']}\n")
    # Write total word counts to a file
    with open("data/total_word_counts.txt", "w", encoding="utf-8") as file:
        for discipline, results in discipline_matches.items():
            file.write(f"{discipline}: {results['total_word_count']}\n")


def create_discipline_matches(
    final_matched_words_file,
    total_words_file,
    final_match_counts_file,
    total_word_counts_file,
):
    """
    Creates a dictionary containing data in provided text files.

    Args:
        final_matched_words_file: A string containing the path to the file
        containing final matched words.
        total_words_file: A string containing the path to the file
        containing total words.
        final_match_counts_file: A string containing the path to the file
        containing final match counts.
        total_word_counts_file: A string containing the path to the file
        containing total word counts.

    Returns:
        A dictionary containing the data as described in previous functions.
    """
    final_matched_words = {}
    with open(final_matched_words_file, "r", encoding="utf-8") as file:
        for line in file:
            discipline, words = line.split(": ")
            words = words.strip().split()
            final_matched_words[discipline] = words

    total_words = {}
    with open(total_words_file, "r", encoding="utf-8") as file:
        for line in file:
            discipline, words = line.split(": ")
            words = words.strip().split()
            total_words[discipline] = words

    final_match_counts = {}
    with open(final_match_counts_file, "r", encoding="utf-8") as file:
        for line in file:
            discipline, count = line.split(": ")
            count = int(count.strip())
            final_match_counts[discipline] = count

    total_word_counts = {}
    with open(total_word_counts_file, "r", encoding="utf-8") as file:
        for line in file:
            discipline, count = line.split(": ")
            count = int(count.strip())
            total_word_counts[discipline] = count

    discipline_matches = {}
    for discipline, final_matched in final_matched_words.items():
        discipline_matches[discipline] = {
            "final_matched_words": final_matched,
            "final_match_count": final_match_counts[discipline],
            "total_words": total_words[discipline],
            "total_word_count": total_word_counts[discipline],
        }

    return discipline_matches


def gen_wordcloud(discipline_matches):
    """
    Plots word clouds showing keyword match frequencies.

    Args:
        discipline_matches: A dictionary containing keyword match and total
        word data.

    Returns:
        None
    """
    _, axes = plt.subplots(2, 3, figsize=(8, 5))
    for i, (discipline, results) in enumerate(discipline_matches.items()):
        matched_words = results["final_matched_words"]
        # Convert list to string and generate
        string_convert = " ".join(matched_words)
        wordcloud = WordCloud(
            collocations=False, width=300, height=200
        ).generate(string_convert)
        row = i // 3
        col = i % 3
        axes[row, col].imshow(wordcloud, interpolation="bilinear")
        axes[row, col].set_title(discipline)
        axes[row, col].axis("off")
    plt.tight_layout()
    plt.show()


def display_counts(discipline_matches):
    """
    Displays the final match counts and total word counts for each discipline.
    Mainly used for us to read counts before creating plots.

    Args:
        discipline_matches: A dictionary containing keyword match and total
        word data.

    Returns:
        A string containing a summary of match counts and total word counts
        for all disciplines.
    """
    display = ""
    for discipline, counts in discipline_matches.items():
        display += f"Engineering Discipline: {discipline}\n"
        display += f"Final Match Count: {counts['final_match_count']}\n"
        display += f"Total Word Count: {counts['total_word_count']}\n\n"
    return display


def plot_bar_graph(discipline_matches):
    """
    Plots a bar graph of final match counts for each engineering discipline.

    Args:
        discipline_matches: A dictionary containing keyword match and total
        word data.

    Returns:
        None
    """
    discipline_names = list(discipline_matches.keys())
    match_counts = [
        counts["final_match_count"] for counts in discipline_matches.values()
    ]
    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(discipline_names, match_counts, color="skyblue")
    plt.xlabel("Engineering Discipline")
    plt.ylabel("Match Count (# of words)")
    plt.title("Match Counts for Engineering Disciplines")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    for bars, count in zip(bars1, match_counts):
        plt.text(
            bars.get_x() + bars.get_width() / 2,
            bars.get_height() + 0.5,
            str(count),
            ha="center",
            va="bottom",
        )
    plt.show()


def plot_stacked_bar_graph(discipline_matches):
    """
    Plots a stacked bar graph of keyword matches versus total match counts for
    all disciplines, highlighting the percentages of overlap.

    Args:
        discipline_matches: A dictionary containing keyword match and total
        word data.

    Returns:
        None
    """
    discipline_names = list(discipline_matches.keys())
    percentages = []
    total_word_counts = []
    match_counts = []
    for counts in discipline_matches.values():
        total_word_count = counts["total_word_count"]
        final_match_count = counts["final_match_count"]
        percentage = (final_match_count / total_word_count) * 100
        percentages.append(percentage)
        total_word_counts.append(total_word_count)
        match_counts.append(final_match_count)
    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(
        discipline_names,
        total_word_counts,
        color="skyblue",
        label="Total Word Count",
    )
    _ = plt.bar(
        discipline_names,
        match_counts,
        bottom=total_word_counts,
        color="salmon",
        label="Match Count",
    )
    # Add percentages on top
    for bars, percentage in zip(bars1, percentages):
        plt.text(
            bars.get_x() + bars.get_width() / 2,
            bars.get_height() + 0.5,
            f"{percentage:.2f}%",
            ha="center",
            va="bottom",
        )
    plt.xlabel("Engineering Discipline")
    plt.ylabel("Counts (# of words)")
    plt.title("Match Counts and Percentages for Engineering Disciplines")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()
