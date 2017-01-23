import numpy, copy, random, math
from .models import Constants


def get_stdev(ask_total, numdims):
    ask_avg = ask_total / numdims

    stdev = math.exp(0.7079252 + 0.0655263 * ask_avg - 0.000551 * math.pow(ask_avg, 2))

    return stdev

def get_autopricedims(ask_total, numdims):
    """
    :param ask_total: the total price set by the seller
    :param numdims: the number of price dimensions in this treatment
    :return: dvalues: a numdims-sized list containing automatically generated dims that sum to ask_total
    """
    # take mu and stddev from data
    mu = ask_total*1./numdims
    stddev = get_stdev(ask_total, numdims)

    print(ask_total)
    print(numdims)
    print(stddev)

    # take numDim draws from a normal distribution
    # truncated normal would be better, but we don't have scipy at the moment.
    rawvals = numpy.random.normal(mu, stddev, numdims).tolist()

    # this rounds the numbers to nearest int
    #   and makes sure there is no negative #s or numbers greater than maxVal
    intvals = [min(Constants.maxprice, max(Constants.minprice, int(round(a)))) for a in rawvals]
    dvalues = copy.copy(intvals)

    # now we need to get to our target value, which i suggest we achieve by
    # incrementing values randomly.
    diff = ask_total - sum(dvalues)
    while not diff == 0:
        increment = int(numpy.sign(diff))
        dim = random.randint(0, numdims - 1)
        dvalues[dim] += increment
        # make sure we haven't gone negative here
        dvalues[dim] = max(0, dvalues[dim])

        diff = ask_total - sum(dvalues)

    return dvalues