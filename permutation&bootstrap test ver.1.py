#Source code from https://campus.datacamp.com/
#Recode and integrated by hrluo93@foxmail.com


#!/usr/bin/env python
# coding: utf-8

# In[19]:

import numpy as np
a=input("input group a:")
b=input("input group b:")
force_a = [int(n) for n in a.split(",")]
force_b = [int(n) for n in b.split(",")]
def permutation_sample(data1, data2):
    """Generate a permutation sample from two data sets."""

    # Concatenate the data sets: data
    data = np.concatenate((data1, data2))

    # Permute the concatenated array: permuted_data
    permuted_data = np.random.permutation(data)

    # Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]

    return perm_sample_1, perm_sample_2
def draw_perm_reps(data_1, data_2, func, size=1):
    """Generate multiple permutation replicates."""

    # Initialize array of replicates: perm_replicates
    perm_replicates = np.empty(size)

    for i in range(size):
        # Generate permutation sample
        perm_sample_1, perm_sample_2 = permutation_sample(data_1,data_2)

        # Compute the test statistic
        perm_replicates[i] = func(perm_sample_1,perm_sample_2)

    return perm_replicates
def diff_of_means(data_1, data_2):
    """Difference in means of two arrays."""

    # The difference of means of data_1, data_2: diff
    diff = np.mean(data_1)-np.mean(data_2)

    return diff
    # Compute difference of mean impact force from experiment: empirical_diff_means

empirical_diff_means = diff_of_means(force_a,force_b)

# Draw 100,000 permutation replicates: perm_replicates
perm_replicates = draw_perm_reps(force_a, force_b, diff_of_means, size=100000)

# Compute p-value: p
p1 = np.sum(perm_replicates >= empirical_diff_means) / len(perm_replicates)

# Print the result
print('Permutation Test P-value =', p1)

##A bootstrap test for identical distributions

# Concatenate forces: forces_concat
forces_concat = np.concatenate((force_a,force_b))

# Initialize bootstrap replicates: bs_replicates
bs_replicates = np.empty(100000)

for i in range(100000):
    # Generate bootstrap sample
    bs_sample = np.random.choice(forces_concat, size=len(forces_concat))
    
    # Compute replicate
    bs_replicates[i] = diff_of_means(bs_sample[:len(force_a)],
                                     bs_sample[len(force_a):])

# Compute and print p-value: p
p2 = np.sum(bs_replicates>=empirical_diff_means) / len(bs_replicates)
print('Bootstrap test for identical distributions P-value =', p2)
def bootstrap_replicate_1d(data,func):
    bs_sample=np.random.choice(data,len(data))
    return func(bs_sample)

def draw_bs_reps(data,func,size=1):
    bs_replicates=np.empty(size)
    for i in range(size):
        bs_replicates[i]=bootstrap_replicate_1d(data,func)
    return bs_replicates
##A two-sample bootstrap hypothesis test for difference of means.
# Compute mean of all forces: mean_force
mean_force = np.mean(forces_concat)

# Generate shifted arrays
force_a_shifted = force_a - np.mean(force_a) + mean_force
force_b_shifted = force_b - np.mean(force_b) + mean_force

# Compute 100,000 bootstrap replicates from shifted arrays
bs_replicates_a = draw_bs_reps(force_a_shifted, np.mean, 100000)
bs_replicates_b = draw_bs_reps(force_b_shifted, np.mean, 100000)

# Get replicates of difference of means: bs_replicates
bs_replicates = bs_replicates_a - bs_replicates_b

# Compute and print p-value: p
p3 = np.sum(bs_replicates>=empirical_diff_means) / len(bs_replicates)
print('Bootstrap hypothesis test for difference of means P-value =', p3)





