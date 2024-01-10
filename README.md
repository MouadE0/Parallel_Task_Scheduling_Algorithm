# Task Scheduling Algorithm

This repository contains a high performance computing project done at CentraleSupelec university in 2022. It contains Python scripts implementing a task scheduling algorithm for directed acyclic graphs (DAGs). The algorithm aims to efficiently schedule tasks on multiple processors, considering dependencies and optimizing the overall schedule length.

The algorithm works by identifying critical paths in the DAG, generating a schedule, and optimizing it using various heuristics. Both classic and parallel implementations are provided for comparison and scalability.

## Contents

1. [classic.py](classic.py): Implements the task scheduling algorithm using a classic approach.
2. [parallel.py](parallel.py): Provides a parallelized version of the algorithm using MPI (Message Passing Interface).

## Dependencies
Python
Azure
mpi4py : Required for the parallelized version



