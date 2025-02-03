
# Set the TESTING environment variable
export TESTING=1

# Run tests with coverage and generate HTML report
coverage run -m pytest

# Generate HTML coverage report
coverage html

# Open the HTML report in Firefox
open -a "Firefox" htmlcov/index.html