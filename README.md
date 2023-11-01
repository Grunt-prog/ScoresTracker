# **ScoresTracker**

**Student Score Visualization Tool**

This is a Flask web application that provides a user management system and allows users to retrieve and visualize student performance data based on their roll numbers. The application is connected to a MySQL database and generates graphs to analyze student scores in different subjects.

## **Table of Contents**
- [**Features**](#features)
- [**Getting Started**](#getting-started)
  - [**Prerequisites**](#prerequisites)
  - [**Installation**](#installation)
- [**Usage**](#usage)
- [**Database Setup**](#database-setup)
- [**User Management**](#user-management)
- [**Data Visualization**](#data-visualization)
- [**Contributing**](#contributing)
- [**License**](#license)

## **Features**

- User management system with authentication.
- Retrieval of student performance data from a MySQL database.
- Visualization of student scores in the form of graphs.
- Customizable data analysis options.
- Easily extensible for additional features.

## **Getting Started**

### **Prerequisites**

Before you can run the application, make sure you have the following dependencies installed:

- Python (version 3.6 or higher)
- Flask
- MySQL Server
- MySQL Connector for Python
- Any additional libraries you might need for data visualization (e.g., Matplotlib)

### **Installation**

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use venv\Scripts\activate
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## **Usage**

To start the Flask application, run the following command:

```bash
python app.py
