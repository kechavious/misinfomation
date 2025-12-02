def mse(true, pred):
    """
    Mean Squared Error
    """
    return sum((t - p)**2 for t, p in zip(true, pred)) / len(true)


def mae(true, pred):
    """
    Mean Absolute Error
    """
    return sum(abs(t - p) for t, p in zip(true, pred)) / len(true)

