# bayes.py
# Example: Disease diagnosis
# P(D) prior disease prevalence
# P(+|D) sensitivity, P(+|~D) false positive rate

def bayes(p_d, p_pos_given_d, p_pos_given_notd):
    p_notd = 1 - p_d
    # P(+) total
    p_pos = p_pos_given_d * p_d + p_pos_given_notd * p_notd
    # P(D|+)
    p_d_given_pos = (p_pos_given_d * p_d) / p_pos
    return p_d_given_pos

if __name__ == "__main__":
    p = bayes(p_d=0.01, p_pos_given_d=0.95, p_pos_given_notd=0.05)
    print("P(disease | positive) = {:.3f}".format(p))
