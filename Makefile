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

# Variables
AWS_ACCESS_KEY_ID := $(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY := $(shell aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION := $(shell aws configure get region)

# Path to your app.yaml file
APP_YAML := app.yaml

# Target to deploy the application
deploy: add-aws-credentials deploy-app revert-app-yaml

# Step 1: Add AWS credentials to app.yaml
add-aws-credentials:
	@echo "Adding AWS credentials to app.yaml..."
	@cp $(APP_YAML) $(APP_YAML).bak
	@echo "  AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)" >> $(APP_YAML)
	@echo "  AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)" >> $(APP_YAML)
	@echo "  AWS_DEFAULT_REGION: $(AWS_DEFAULT_REGION)" >> $(APP_YAML)

# Step 2: Deploy the application (replace with your actual deployment command)
deploy-app:
	@echo "Deploying the application..."
	# Replace this with your actual deployment command (e.g., gcloud app deploy)
	# Example:
	gcloud app deploy

# Step 3: Revert the app.yaml file to its original state
revert-app-yaml:
	@echo "Reverting app.yaml changes..."
	@mv $(APP_YAML).bak $(APP_YAML)
	@echo "app.yaml reverted."

# Clean up any backup files (optional)
clean:
	@rm -f $(APP_YAML).bak