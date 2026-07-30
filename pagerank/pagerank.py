import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    # Load the corpus
    corpus = crawl(sys.argv[1])

    # Compute PageRank by sampling
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # Compute PageRank by iteration
    ranks = iterate_pagerank(corpus, DAMPING)

    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse HTML files and build a dictionary mapping each page
    to the set of pages it links to.
    """

    pages = {}

    for filename in os.listdir(directory):

        if not filename.endswith(".html"):
            continue

        with open(os.path.join(directory, filename), encoding="utf-8") as f:
            contents = f.read()

            # Find all links
            links = set(re.findall(r'<a\s+(?:[^>]*?)href="([^"]*)"', contents))

            # Remove self-links
            links.discard(filename)

            pages[filename] = links

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = {
            link for link in pages[filename]
            if link in pages
        }

    return pages



def transition_model(corpus, page, damping_factor):
    """
    Return probability distribution for next page.
    """

    probabilities = {}

    total_pages = len(corpus)

    # Random jump probability
    for p in corpus:
        probabilities[p] = (1 - damping_factor) / total_pages

    links = corpus[page]

    # Follow links
    if links:
        for link in links:
            probabilities[link] += damping_factor / len(links)

    # Page with no links
    else:
        for p in corpus:
            probabilities[p] += damping_factor / total_pages

    return probabilities



def sample_pagerank(corpus, damping_factor, n):
    """
    Estimate PageRank by sampling from the transition model.
    """

    counts = {}

    # Initialize counts
    for page in corpus:
        counts[page] = 0

    # Choose first page randomly
    page = random.choice(list(corpus.keys()))

    # Generate samples
    for i in range(n):

        counts[page] += 1

        model = transition_model(
            corpus,
            page,
            damping_factor
        )

        page = random.choices(
            list(model.keys()),
            weights=model.values()
        )[0]

    # Convert counts to PageRank probabilities
    ranks = {}

    for page in counts:
        ranks[page] = counts[page] / n

    return ranks



def iterate_pagerank(corpus, damping_factor):
    """
    Compute PageRank using iteration.
    """

    ranks = {}

    # Initial values
    for page in corpus:
        ranks[page] = 1 / len(corpus)

    while True:

        new_ranks = {}

        for page in corpus:

            rank = (1 - damping_factor) / len(corpus)

            for possible_page in corpus:

                links = corpus[possible_page]

                if page in links:
                    rank += (
                        damping_factor
                        * ranks[possible_page]
                        / len(links)
                    )

                elif len(links) == 0:
                    rank += (
                        damping_factor
                        * ranks[possible_page]
                        / len(corpus)
                    )

            new_ranks[page] = rank

        # Check convergence
        converged = True

        for page in corpus:
            if abs(new_ranks[page] - ranks[page]) > 0.001:
                converged = False
                break

        ranks = new_ranks

        if converged:
            break

    return ranks



if __name__ == "__main__":
    main()