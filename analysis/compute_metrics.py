def mse(true, pred):
    """
    Mean squared error between lists.
    """
    return sum((t - p)**2 for t, p in zip(true, pred)) / len(true)


def mae(true, pred):
    """
    Mean absolute error.
    """
    return sum(abs(t - p) for t, p in zip(true, pred)) / len(true)
