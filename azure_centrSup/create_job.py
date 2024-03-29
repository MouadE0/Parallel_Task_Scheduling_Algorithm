#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse

import azure.batch

from azure.batch import models
from azure.batch.batch_auth import SharedKeyCredentials

import configs



def create_job(batch_client, name_job, name_pool, cmd_prep_task=None):

    user = models.UserIdentity(
    auto_user = models.AutoUserSpecification(
        elevation_level = models.ElevationLevel.admin,
        scope = models.AutoUserScope.task
        )
    )

    prepare_task = models.JobPreparationTask(
        command_line = cmd_prep_task,
        id = None,
        user_identity = user
        )

    job = models.JobAddParameter(
        id = name_job,
        pool_info = models.PoolInformation(pool_id = name_pool),
        job_preparation_task = prepare_task
        )
    batch_client.job.add(job)








if __name__ == "__main__" :


    parser = argparse.ArgumentParser(
                                    description='Creating a Azure Batch Job().',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                    )
    parser.add_argument('--pool_id', help='Id of pool(pool should exist)', dest='pool_id', default='CentraleSupelecPool1')
    parser.add_argument('--job_id', help='Id of job', dest='job_id', default='CentraleSupelecJob1')
    args = parser.parse_args()

    pool_id = args.pool_id
    job_id = args.job_id


    credentials_batch = SharedKeyCredentials(account_name = configs.batch['name'], key = configs.batch['key'])
    batch_client = azure.batch.BatchServiceClient(credentials = credentials_batch, batch_url = configs.batch['url'])


    create_job(
               batch_client = batch_client,
               name_job = job_id,
               name_pool = pool_id, 
               cmd_prep_task = configs.cmd_prep_task
              )

    print("Job Created: {0}\n".format(job_id))
    with open('output_job_id.txt','a+') as file_resource:
        file_resource.write("Job {0} created and linked to pool {1}.\n".format(job_id, pool_id))