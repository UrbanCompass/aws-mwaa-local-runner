# -*- coding: utf-8 -*-
"""
:copyright: (c) 2022 by Urban Compass, Inc.
:author: kaiyu.wang
"""

import sys, os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from uc.listing_data_sources.common.agent_cache import cache_manager


default_args = {

}

with DAG(
    "agent_cache_refresh_dag",
    default_args=default_args,
    description="agent cache refresh job",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=["example"],
) as dag:
    t1 = PythonOperator(
        task_id="agent_cache_refresh",
        python_callable=cache_manager.run_agent_cache_refresh_job,
        op_kwargs={
            "num_processes": 8,
            "agent_cache_table_name": "development-agent-cache",
            "people_service_hostport": "grpc://peopleserver.grpc.dev.na.compass.com:31337",
            "entity_profile_service_hostport": "grpc://peopleserver.grpc.gamma.na.compass.com:80",
        },
    )

    t1
