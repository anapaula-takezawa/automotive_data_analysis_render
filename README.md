 <p align="center">
  <img src="automotive_data_explorer_cover_under_1mb.jpg"
       alt="Automotive Data Explorer — Interactive Data Dashboard"
       width="100%">
</p>

# Automotive Data Explorer — Interactive Dashboard

**Author:** Ana Paula Takezawa  
**Education:** MBA in Data Science and Artificial Intelligence — TripleTen Brasil

**Live Demo:** [Access the Interactive Dashboard](https://my-new-repo-vbxl.onrender.com)

---

## Project Overview

Automotive Data Explorer is an interactive web application designed to explore and visualize used vehicle advertisement data from the United States.

The project combines Exploratory Data Analysis (EDA), data manipulation, statistical analysis, and interactive visualization to investigate patterns and relationships in the used car market.

Developed using Python, Pandas, Plotly, and Streamlit, the application provides an interactive environment for exploring vehicle prices, characteristics, and listing trends.

Originally developed as part of the Software Development Tools module of the Data Science program at TripleTen Brasil, the project was further expanded to include a comprehensive exploratory analysis notebook and an enhanced interactive dashboard.

## Project Objectives

- Perform Exploratory Data Analysis (EDA) on used vehicle listings.
- Identify patterns and relationships between vehicle attributes and prices.
- Develop an interactive dashboard using Streamlit.
- Create data visualizations with Plotly.
- Apply data manipulation and analysis techniques using Pandas.
- Deploy a Python web application to a cloud platform.

## Dataset

The project uses a dataset containing **51,525 used vehicle advertisements** from the United States.

The dataset includes information such as:

- Vehicle price
- Model and manufacturing year
- Vehicle condition
- Cylinder count
- Fuel type
- Odometer reading
- Transmission
- Vehicle category
- Paint color
- Four-wheel drive information
- Advertisement posting date
- Days listed

The dataset is provided in the repository as `vehicles.csv`.

## Dashboard Features

The interactive dashboard allows users to explore the automotive market through filters, performance indicators, and data visualizations.

### Interactive Filters

Users can filter the dataset by:

- Vehicle type
- Vehicle condition
- Fuel type
- Transmission
- Price range
- Manufacturing year

### Key Performance Indicators (KPIs)

The dashboard displays dynamically calculated indicators:

- Total number of advertisements
- Median vehicle price
- Median manufacturing year
- Median odometer reading

### Data Visualizations

The dashboard includes:

- **Price Distribution:** Histogram showing the distribution of vehicle prices.
- **Price by Condition:** Comparison of median prices across vehicle conditions.
- **Price vs. Odometer:** Scatter plot exploring the relationship between vehicle price and odometer readings.
- **Price by Model Year:** Analysis of median prices across manufacturing years.
- **Fuel Distribution:** Distribution of advertisements by fuel type.
- **Vehicle Type Distribution:** Comparison of advertisement volume across vehicle categories.
- **Monthly Listing Trends:** Number of advertisements posted over time.

### Data Exploration

An interactive data table allows users to inspect vehicle advertisements after applying the selected filters.

## Exploratory Data Analysis

A dedicated Jupyter Notebook documents the exploratory data analysis process, including:

- Dataset inspection and structure
- Missing value analysis
- Data preparation and cleaning
- Statistical summaries
- Univariate and bivariate analysis
- Price distribution and vehicle attribute relationships
