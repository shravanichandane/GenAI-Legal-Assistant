import numpy as np
import scipy.stats as st

def compute_mean_accuracy(scores):
    """Computes the mean accuracy from an array of scores."""
    return np.mean(scores)

def compute_std_dev(scores):
    """Computes the standard deviation of an array of scores."""
    return np.std(scores, ddof=1)

def compute_confidence_interval(scores, confidence=0.95):
    """Computes the confidence interval for an array of scores."""
    n = len(scores)
    if n < 2:
        return 0.0, 0.0
    m, se = np.mean(scores), st.sem(scores)
    h = se * st.t.ppf((1 + confidence) / 2., n-1)
    return m - h, m + h

def compute_all_metrics(scores):
    """Computes mean, std dev, and 95% CI for the given scores."""
    mean = compute_mean_accuracy(scores)
    std = compute_std_dev(scores)
    ci_lower, ci_upper = compute_confidence_interval(scores)
    return {
        "mean_accuracy": mean,
        "std_dev": std,
        "ci_95_lower": ci_lower,
        "ci_95_upper": ci_upper
    }
