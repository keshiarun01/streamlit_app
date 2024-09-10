# NYC Job Postings Dashboard: Exploratory Data Analysis Using Streamlit

An interactive dashboard built with Streamlit to analyze and visualize job postings in New York City, providing insights into employment trends across various sectors and job categories.

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Data Cleaning](#data-cleaning)
- [Streamlit Dashboard](#streamlit-dashboard)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Deployment](#deployment)
- [Conclusion](#conclusion)
- [Contributors](#contributors)

## Project Overview

New York City is a hub for diverse industries, from finance to healthcare. This project uses Streamlit to create a dashboard that visualizes job market trends, aiding stakeholders in making data-driven decisions for urban planning and workforce development.

## Dataset

The dataset, sourced from [NYC Jobs](https://catalog.data.gov/dataset/nyc-jobs), includes internal and external job postings available on the City of New York’s official jobs site.

### Key Fields:

- **Job ID, Agency, Posting Type, Number of Positions, Business Title, Job Level, Job Category, Salary Frequency, Career Level, Full-Time/Part-Time Indicator.**

## Data Cleaning

- **Removed Irrelevant Columns**: Excluded non-visualizable fields.
- **Handled Missing Values**: Filled missing data with 'unknown' or 'not provided'.
- **Removed Duplicates**: Cleaned redundant entries.
- **Converted Data Types**: Adjusted date columns to `datetime`.
- **Handled Outliers**: Removed outliers in salary data.
- **Saved Cleaned Data**: Cleaned data exported as `cleaned_data_nyjobs.csv`.

## Streamlit Dashboard

An interactive dashboard built with Streamlit, offering data visualization and filtering options. The application is divided into three pages for easy navigation.

### Features

- **Data Preview**: Displays a table of job postings with adjustable row display.
- **Interactive Filters**: Allows filtering by date range, minimum salary, and job category.

## Exploratory Data Analysis (EDA)

Key visualizations include:

1. **Salary Range Distribution**: Highlights common salary ranges.
2. **Top 10 Job Categories**: Identifies the most active job categories.
3. **Full-Time/Part-Time Distribution**: Shows the prevalence of full-time vs. part-time roles.
4. **Career Level Distribution**: Displays job postings across different career levels.
5. **Job Postings Over Years**: Visualizes trends in job postings.
6. **Word Cloud of Job Descriptions**: Highlights common keywords.
7. **Internal vs. External Job Postings**: Compares internal and external job openings.
8. **Job Posting Trends by Month**: Shows monthly job posting trends.

## Deployment

Deployed on Streamlit Sharing for easy accessibility and scalability.

### Deployment Steps:

1. **Preparation**: Tested locally; created `requirements.txt` for dependencies.
2. **GitHub Integration**: Uploaded code to a public repository.
3. **Streamlit Sharing**: Linked GitHub repository for automatic deployment.
4. **Monitoring**: Used Streamlit's dashboard to monitor application performance.

App Preview: [NYC Job Postings Dashboard](https://8sqmkeqee57ufdylly2hdm.streamlit.app/)

## Conclusion

The dashboard provides a detailed overview of the NYC job market, highlighting trends in salaries, job categories, and locations, offering valuable insights for job seekers, employers, and policymakers.
