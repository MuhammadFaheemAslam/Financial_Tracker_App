# Finance Tracker App

**Finance Tracker** is a web application designed to help individuals manage their monthly budgets by tracking expenses and adjusting budgets accordingly. The app allows users to set a monthly budget, track their spending, and visualize how their expenses compare to their budget.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Apps Overview](#apps-overview)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Folder Structure](#folder-structure)
7. [Contributing](#contributing)

## Introduction

**Finance Tracker** helps users take control of their finances by:
- **Tracking Monthly Expenses**: Easily add and categorize expenses.
- **Budget Management**: Set monthly budgets for different categories.
- **Adjusting Budgets**: View how your spending aligns with your monthly budget and adjust it as needed.
- **Data Visualization**: Interactive charts to visualize income, expenses, and budget adjustments.

The app uses Flask for the backend, MySQL for data storage (via AWS RDS), and EC2 for hosting.

## Features

- **Expense Tracker**:
  - Add, edit, and delete expenses.
  - Categorize expenses (e.g., groceries, rent, entertainment).
  
- **Budget Management**:
  - Set monthly budgets for different categories.
  - View budget progress and adjust as needed.

- **Data Visualization**:
  - Interactive charts using Chart.js to visualize expenses, budget status, and monthly adjustments.

- **AWS Hosting**:
  - Deployed on AWS EC2 with MySQL database hosted on AWS RDS for reliable data storage.

## Apps Overview
### Registration Page
 Register the user with email and give username and password.

  ![Register Page](financial-tracker/AppScreens/RegistrationPage.png "Registration Page")

### Login Page
  Login into the app with your registerd email.

  ![Home Page](financial-tracker/AppScreens/LoginPage.png "Login Page")


### Home Page
   The HomePage shows an overview of Add expenses, Set budget.

  ![Home Page](financial-tracker/AppScreens/Homepage.png "Home Page")


### Dashboard Page
  The dashboard shows an overview of your total monthly expenses, budget, and a comparison chart.
  
 ![Dashboard Page](financial-tracker/AppScreens/DashboardPage.png "Dashboard Page")

 
### Set Budget
  Set and view monthly budgets for various categories.
  
![Monthly Budget](financial-tracker/AppScreens/AddBudgetPage.png "Monthly Budget Screen")

### View Budgets
  View the all Budgets you set earlier.
  
![Monthly Budget](financial-tracker/AppScreens/ViewBudgetsPage.png "All Budgets Screen")


### Update Budgets
  Update the all Budgets you set earlier.
  
![Monthly Budget](financial-tracker/AppScreens/UpdateBudgetPage.png "Modify Budgets Screen")

### Delete Budgets
  Delete the Budgets you set earlier.
  
![Monthly Budget](financial-tracker/AppScreens/DeleteBudgetPage.png "Delete Budgets Screen")

### Add Expense
  Easily add new expenses, categorize them, and track spending.

![Add Expense](financial-tracker/AppScreens/AddExpensePage.png "Add Expense Screen")


### View Expense
  View all your expenses.

![View Expense](financial-tracker/AppScreens/ViewExpensesPage.png "All Expense Screen")


### Update Expense
  Edit your expenses.

![Update Expense](financial-tracker/AppScreens/EditExpensePage.png "Update Expense Screen")


Charts that compare your expenses to your budget over time.

## Installation

To set up **Finance Tracker** locally, follow these steps:

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- MySQL (or access to an AWS RDS MySQL instance)
- Pip

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/finance-tracker.git
    cd finance-tracker
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    - Configure your database settings in `config.py` (under `SQLALCHEMY_DATABASE_URI`).
    - Run migrations (if applicable):

    ```bash
    python manage.py db upgrade
    ```

5. Run the application:

    ```bash
    python run.py
    ```

The app should now be accessible at `http://localhost:5000`.

## Usage

- **Dashboard**: View an overview of your monthly budget, expenses, and charts.
- **Add Expenses**: Track your expenses by category and date.
- **Set Budgets**: Set your monthly budgets and track progress throughout the month.
- **Adjust Budgets**: View budget usage and make adjustments as necessary.

## Folder Structure

Here’s an overview of the project structure:

