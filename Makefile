# Flask application
FLASK_APP=app.py

# Default target: Start the Flask app
all: flask-run

# Start the Flask app
flask-run:
	@echo "Starting Flask server..."
	FLASK_APP=$(FLASK_APP) flask run

# Install Flask dependencies
install-flask-deps:
	@echo "Installing Python dependencies for Flask..."
	pip3 install -r requirements.txt

# Clean up Python bytecode files
clean-pycache:
	@echo "Cleaning Python bytecode files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Python cache cleaned."

# Clean and remove Python virtual environment (optional)
clean-venv:
	@echo "Cleaning Python virtual environment..."
	rm -rf venv
	@echo "Virtual environment removed."

# Create and activate a virtual environment
create-venv:
	@echo "Creating Python virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created."

# Activate the virtual environment (run manually in terminal)
activate-venv:
	@echo "To activate the virtual environment, run: source venv/bin/activate"