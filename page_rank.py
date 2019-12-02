import os
import time
from progress import Progress
from random import choice

WEB_DATA = os.path.join(os.path.dirname(__file__), 'school_web.txt')


def load_graph(fd):
    """Load graph from text file

    Parameters:
    fd -- a file like object that contains lines of URL pairs

    Returns:
    A representation of the graph.

    Called for example with

    >>> graph = load_graph(open("web.txt"))

    the function parses the input file and returns a graph representation.
    Each line in the file contains two white space seperated URLs and
    denotes a directed edge (link) from the first URL to the second.
    """
    graph = {}
    # Iterate through the file line by line
    for line in fd:
        # And split each line into two URLs
        node, target = line.split()
        # if graph contains an array for node, append target to it
        if node in graph:
            graph[node].append(target)
        # else initialise an array for node containing target
        else:
            graph[node] = [target]
    return graph


def print_stats(graph):
        """Print number of nodes and edges in the given graph"""
        print(f"{len(graph)} nodes and {sum(len(graph[x]) for x in graph)} edges")


def stochastic_page_rank(graph, n_iter=1_000_000, n_steps=100):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of random walks performed
    n_steps (int) -- number of followed links before random walk is stopped

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    hit_count = {}
    # initialize hit_count[node] with 0 for all nodes
    for x in graph:
        hit_count[x] = 0

    # repeat n_iterations times:
    for x in range(n_iter):
        # current_node <- randomly selected node
        current_node = choice(list(graph))
        # repeat n_steps times:
        for x in range(n_steps):
            # current_node with <- randomly chosen node among the out edges of current_node
            current_node = choice(graph[current_node])
        # hit_count[current_node] += 1/n_iterations
        hit_count[current_node] += 1 / n_iter
    return hit_count


def distribution_page_rank(graph, n_iter=100):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of probability distribution updates

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    node_prob = {}

    # initialize node_prob[node] = 1/(number of nodes) for all nodes
    for x in graph:
        node_prob[x] = 1 / len(graph)

    # repeat n_iterations times:
    for i in range(n_iter):
        # initialize next_prob[node] = 0 for all nodes
        next_prob = {}
        for node in graph:
            next_prob[node] = 0

        # for each node
        for node in graph:
            # p <- node_prob[node] divided by its out degree
            p = node_prob[node] / len(graph[node])
            # for each target among out edges of node:
            for target in graph[node]:
                next_prob[target] += p
        node_prob = next_prob
    return node_prob


def main():
    # Load the web structure from file
    web = load_graph(open(WEB_DATA))

    # print information about the website
    print_stats(web)

    # The graph diameter is the length of the longest shortest path
    # between any two nodes. The number of random steps of walkers
    # should be a small multiple of the graph diameter.
    diameter = 3

    # Measure how long it takes to estimate PageRank through random walks
    print("Estimate PageRank through random walks:")
    n_iter = len(web)**2
    n_steps = 2*diameter
    start = time.time()
    ranking = stochastic_page_rank(web, n_iter, n_steps)
    stop = time.time()
    time_stochastic = stop - start

    # Show top 20 pages with their page rank and time it took to compute
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:20]))
    print(f'Calculation took {time_stochastic:.2f} seconds.\n')

    # Measure how long it takes to estimate PageRank through probabilities
    print("Estimate PageRank through probability distributions:")
    n_iter = 2*diameter
    start = time.time()
    ranking = distribution_page_rank(web, n_iter)
    stop = time.time()
    time_probabilistic = stop - start

    # Show top 20 pages with their page rank and time it took to compute
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:20]))
    print(f'Calculation took {time_probabilistic:.2f} seconds.\n')

    # Compare the compute time of the two methods
    speedup = time_stochastic/time_probabilistic
    print(f'The probabilitic method was {speedup:.0f} times faster.')


if __name__ == '__main__':
    main()
