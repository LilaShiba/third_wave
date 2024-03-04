#!/bin/bash

# Update and Upgrade the System
echo "Updating and upgrading your system..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Git, Python3, and pip
echo "Installing Git, Python3, and pip..."
sudo apt-get install -y git python3 python3-pip

# Verify Installation
echo "Verifying the installation..."
git --version
python3 --version
pip3 --version

# Create a Python Virtual Environment
echo "Creating a Python virtual environment..."
python3 -m venv flask_env

# Activate the Virtual Environment
echo "Activating the virtual environment..."
source flask_env/bin/activate

# Clone the GitHub Repository
echo "Cloning the GitHub repository..."
git clone https://github.com/LilaShiba/flask_server_ubi.git

# Navigate into the Repository Directory
cd flask_server_ubi

# Install Requirements from requirements.txt
echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo "Setup is complete. Your Flask server environment is ready!"
