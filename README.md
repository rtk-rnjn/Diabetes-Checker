# Quart Web Application with Machine Learning

This project is a Quart web application that incorporates machine learning to predict the risk of diabetes based on user input. The application allows users to input various health parameters and get a prediction regarding their risk of diabetes.

## Project Structure

The project consists of the following files and directories:

- `quart_app/`: The main application directory.
    - `app.py`: Initializes the Quart web application and integrates the machine learning component.
    - `routes/`: Contains route definitions for the application.
        - `index.py`: Defines the main route for user input and prediction.
    - `assets/`: Contains datasets used for machine learning operations.
- `ml.py`: The machine learning module responsible for handling data preprocessing, model training, and predictions.
- `utils.py`: Utility functions and decorators used throughout the project, including data conversion and async decorators.
- `__main__.py`: Launches the application using the Quart runner.
- `templates/`: Contains the HTML template for the user interface.
    - `index.html`: The user input form and result display.
Installation
To run this project, make sure you have Python installed. You can set up a virtual environment and install the required dependencies listed in requirements.txt:

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python __main__.py
```

1. Access the web application at http://localhost:5000 in your web browser.

2. Fill in the health parameters in the input form and submit.

3. The application will provide a prediction on whether you are at risk of diabetes or not.

## Configuration

- `project.toml`: Contains tool configurations, including code formatting and linting settings.

## Dependencies

The project relies on the following Python libraries:

- `hypercorn`: An ASGI web server for Quart.
- `numpy`: For numerical operations.
- `pandas`: For data manipulation.
- `Quart`: A web framework for building asynchronous web applications.
- `scikit-learn`: For machine learning model training and prediction.
You can install these dependencies using the requirements.txt file.

## Contributing

Feel free to contribute to this project by opening issues, suggesting improvements, or creating pull requests.
