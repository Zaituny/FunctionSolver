# FunctionSolver
This is a repository for the Master Micro's 2025 Winter SW internship

## Features

- Plot two mathematical functions simultaneously
- Find intersection points between functions
- Interactive plot with hover information
- Support for common mathematical operations and functions
- Clean, modern UI with customizable styling

## Installation

```bash
# Clone the repository
git clone https://github.com/Zaituny/FunctionSolver.git
# Move into project directory
cd FunctionSolver

# Install dependencies
python -m pip install -r requirements.txt
```

## App Screenshots
# Main Page
![Main Page](app_screenshots/app.png)

# Plotting Functions
Example 1: Plotting two functions, f(x) = x^2 + 1 and g(x) = -x^2 + 2
![example1](app_screenshots/example_run_1.png)
![example1 hover1](app_screenshots/example_run_1_hover_1.png)
![example1 hover2](app_screenshots/example_run_1_hover_2.png)
Example 2: Plotting two functions, f(x) = log(x) and g(x) = -x^2 + 2
![example2](app_screenshots/example_run_2.png)
![example2 hover1](app_screenshots/example_run_2_hover_1.png)
Example 3: Plotting two functions, f(x) = log(x^2+2) and g(x) = -x^2+2
![example3](app_screenshots/example_run_3.png)
# Invalid Input
Both input fields are empty
![Invalid Input](app_screenshots/both_input_fields_empty.png)
One of the input fields is empty
![Invalid Input](app_screenshots/one_input_field_empty.png)
Invalid variable name in both input fields
![Invalid Input](app_screenshots/invalid_variable_names_in_both_fields.png)
Invalid variable name in one of the input fields
![Invalid Input](app_screenshots/invalid_variable_name_in_one_field.png)
Invalid log function
![Invalid Input](app_screenshots/invalid_log_expression.png)
Incomplete expression
![Invalid Input](app_screenshots/incomplete_expression.png)

## License

MIT License - see LICENSE file for details.