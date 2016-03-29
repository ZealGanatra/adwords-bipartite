import csv
import operator
import math
import sys
import random

random.seed(0)

class Advertiser(object):
    def __init__(self, advertiser_id, budget):
        self.advertiser_id = advertiser_id
        self.budget = budget
        self.total_budget = budget
        self.spent = 0
        self.queries_budget = []

    def add_to_query(self, query):
        self.queries_budget.append(query)


def msvv_sort(advertiser_query_budget):
    advertiser = advertiser_query_budget.advertiser
    x_u = advertiser.spent / advertiser.total_budget
    si_xu = 1 - math.exp(x_u - 1)
    return advertiser_query_budget.bid * si_xu


def balance_sort(advertiser_query_budget):
    advertiser = advertiser_query_budget.advertiser
    return advertiser.budget - advertiser.spent


class Query(object):
    def __init__(self, keyword):
        self.keyword = keyword
        self.advertisers_budget = []

    def add_advertiser(self, query_advertiser_budget):
        self.advertisers_budget.append(query_advertiser_budget)

    def sort_advertisers(self, sorting_technique=None):
        sorted_advertiser = sorted(self.advertisers_budget, key=sorting_technique, reverse=True)
        return sorted_advertiser


class QueryAdvertiserBudget(object):
    query = None

    def __init__(self, query, advertiser, bid):
        self.query = query
        self.advertiser = advertiser
        self.bid = bid
        self.advertiser.add_to_query(self)
        self.query.add_advertiser(self)


advertisers = {}
queries = {}
queries_list = []
total_revenue = 0


def load_bidder_datasets():
    with open('bidder_dataset.csv', 'rb') as csvfile:
        bidder_datasets = csv.reader(csvfile)
        global queries
        global advertisers
        counter = 0
        for row in bidder_datasets:
            if counter == 0:
                counter += 1
                continue

            advertiser = advertisers.get(row[0])
            if advertiser is None:
                advertiser = Advertiser(row[0], float(row[3]))

            advertisers[row[0]] = advertiser
            query = queries.get(row[1], Query(row[1]))
            queries[row[1]] = query
            QueryAdvertiserBudget(query, advertiser, float(row[2]))


def adword_match(sort_technique):
    size = 100
    global queries_list
    global queries
    mean_revenue = 0
    for i in range(0, size):
        revenue = 0
        shuffled_query = queries_list
        random.shuffle(shuffled_query)
        for advertiser_id in advertisers:
            advertiser = advertisers.get(advertiser_id)
            advertiser.spent = 0
        for query in shuffled_query:
            if query != "":
                query_obj = queries[query]
                for advertiser_query_budget in query_obj.sort_advertisers(sort_technique):
                    advertiser = advertiser_query_budget.advertiser
                    bid = advertiser_query_budget.bid
                    if (advertiser.budget - advertiser.spent) >= bid:
                        # advertiser.budget -= bid
                        revenue += bid
                        advertiser.spent += bid
                        break
        mean_revenue += revenue
    mean_revenue /= size
    competitive_ratio = mean_revenue / total_revenue
    print("Revenue count for %s is %f and competitive ration is %f" % (method, mean_revenue, competitive_ratio))
    return mean_revenue / size, competitive_ratio


def greedy_match():
    adword_match(operator.attrgetter('bid'))


def msvv_match():
    adword_match(msvv_sort)


def balance_match():
    adword_match(balance_sort)


def load_queries():
    with open('queries.txt', 'rb') as queriesfile:
        global queries_list
        queries_list = queriesfile.read().split('\n')
        # queries = queries.split()


def calculate_maxrevenue():
    global total_revenue
    for advertiser_id in advertisers:
        advertiser = advertisers.get(advertiser_id)
        total_revenue += advertiser.budget


def main():
    load_bidder_datasets()
    load_queries()
    calculate_maxrevenue()
    if (method == "greedy"):
        greedy_match()
    if (method == "msvv"):
        msvv_match()
    if (method == "balance"):
        balance_match()


if len(sys.argv) != 2:
    print "python adowrds.py <greedy|mssv|balance>"
    exit(1)
method = sys.argv[1]

if __name__ == "__main__":
    main()
