# -*- coding = utf-8 -*-
# @Time: 2024/11/20 15:18
# @Author: Zhihang Yi
# @File: 007K_Means_Clustering1.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import openpyxl
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def main():
    cohorts = pd.read_excel('~/Downloads/Most_Recent_Cohorts_Data.xlsx', engine='openpyxl', index_col=0)
    candidate_schools = pd.read_excel('~/Downloads/Potential_Candidate_Schools.xlsx', engine='openpyxl', index_col=0)

    candidate_schools = screening_schools(cohorts, candidate_schools)
    candidate_schools = data_imputation(candidate_schools)
    candidate_schools = screening_attributes(candidate_schools)

    candidate_schools.to_csv('candidate_schools.csv')


def screening_schools(cohorts, candidate_schools):
    candidate_schools = matching_schools(cohorts, candidate_schools)
    candidate_schools = remove_hcm2_schools(candidate_schools)
    candidate_schools = remove_50pct_null_schools(candidate_schools)
    return candidate_schools


def matching_schools(cohorts, candidate_schools):
    """
    :param cohorts:
    :param candidate_schools:
    :return: candidate schools after first screening by comparing
    cohorts with candidate_schools
    """
    for unitid in cohorts.index:
        if unitid not in candidate_schools.index:
            cohorts.drop(index=unitid, inplace=True)

    return cohorts


def remove_unrelevant(candidate_schools):
    candidate_schools = candidate_schools.drop(columns=['CITY', 'STABBR', 'INSTURL', 'NPCURL'])
    return candidate_schools

def remove_hcm2_schools(candidate_schools):
    """
    :param candidate_schools:
    :return: Delete the schools which are not currently operating institution and which are on
    Heightened Cash Monitoring 2 by Department of Education, meaning that they
    encounter economic depression and lack students and which has no or very limited
    information about percentage of degrees awarded.
    """
    candidate_schools = candidate_schools[candidate_schools.loc[:, 'HCM2'] == 0]
    return candidate_schools


def remove_50pct_null_schools(candidate_schools):
    """
    :param candidate_schools:
    :return:Delete the schools of whom 50% of the attributes are NULL. If the percentage
    of missing data exceeds 50%, the imputation will result in great error, which we
    treat as a threshold for missing data.
    """
    threshold = len(candidate_schools.columns) / 2

    candidate_schools = candidate_schools[candidate_schools.isna().sum(axis=1) < threshold]
    candidate_schools = candidate_schools[candidate_schools.isnull().sum(axis=1) < threshold]

    return candidate_schools


def data_imputation(candidate_schools):
    """
    preparing process of data imputation.

    :param candidate_schools:
    :return: return candidate schools with data imputated.
    """
    features = [
        'NPT4_PUB', 'NPT4_PRIV', 'NPT41_PUB', 'NPT42_PUB',
        'NPT43_PUB', 'NPT44_PUB', 'NPT45_PUB', 'NPT41_PRIV',
        'NPT42_PRIV', 'NPT43_PRIV', 'NPT44_PRIV', 'NPT45_PRIV'
    ]

    sample = candidate_schools.loc[:, features]
    candidate_schools.drop(columns=features, inplace=True)

    net_price = imputation_process(sample, features)
    candidate_schools.loc[:, 'Net_Price'] = net_price

    return candidate_schools


def imputation_process(sample, features):
    """
    the imputating process of data imputation
    :param sample:
    :param features:
    :return:
    """
    sample_copy = sample.copy()
    sample_copy = imputation_initialze(sample_copy)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(sample_copy)

    k = 5

    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    sample.loc[:, 'Cluster'] = kmeans.labels_

    for cluster in range(k):
        group = sample[sample.loc[:, 'Cluster'] == cluster]
        group_index = sample.loc[:, 'Cluster'] == cluster

        for feature in features:
            mean = group.loc[:, feature].mean()
            sample.loc[group_index, feature] = sample.loc[group_index, feature].fillna(mean)

        sample.loc[group_index, 'returnValue'] = sample.loc[group_index, features].mean(axis=1).round(2)

    return sample.loc[:, 'returnValue']


def imputation_initialze(candidate_schools):
    for attr in candidate_schools.columns:
        mean = candidate_schools.loc[:, attr].mean()
        candidate_schools.loc[:, attr] = candidate_schools.loc[:, attr].fillna(mean)

    return candidate_schools


def screening_attributes(candidate_schools):
    candidate_schools = remove_unrelevant(candidate_schools)
    return candidate_schools


if __name__ == '__main__':
    main()
