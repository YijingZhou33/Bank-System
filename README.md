# Software Testing 

This repository contains code and testing for the PROJ **Bank Loan Management System**.

## Requirements

We are using Python 3.7.x and built-in database SQLite for this project.

## Setup

1. Ensure that you have python 3.7 installed

2. Also two packages `coverage` and `pytest_cov`

   `pip install coverage`
   `pip install pytest-cov`

3. Clone the repository

### Bank System 

`cd` into the `source_code` directory and run `python main.py` 

### pytest Unit Testing 

`cd` into the `pytest` directory

- **statement coverage**: `pytest --cov=main_test --cov-report term-missing`
- **branch coverage**: `pytest --cov=main_test --cov-report term-missing --cov-branch`