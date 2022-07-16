#!/usr/bin/env bash

# Create an environment variable to test for existence:
ENV_FILE='./env/'
IGNORE_FILE='./.gitignore' 

# .gitignore array of commands:
declare -a IGNORE=('.gitignore' '.vscode' '.idea' 'venv' 'env' '.venv' '.env' '__pycache__' '*.ini' '*.cfg')

# =============================================================================================================== #
# CREATE FUNCTIONS:
# =============================================================================================================== #
activate() {
    . env/bin/activate
    echo "Updating pip"
    pip install -U pip
    echo "Installing requirements to virtual environment"
    pip install -r requirements.txt
    echo "Virtual Environment env/ created and activated!"
}

# Check if the .gitignore file exists, and if not 
# create the file and then write the appropriate 
# lines to the file:
createGitignore() {

	if [ ! -f "${IGNORE_FILE}" ];then
		echo "No ${IGNORE_FILE} Exists, Creating one now.."
		touch "${IGNORE_FILE}"

	fi
}

writeToGitignore() {
	echo "Writing params to .gitignore file"
	for p in "${IGNORE[@]}"; do
		echo "$p" | tee -a "${IGNORE_FILE}"
	done
}
# =============================================================================================================== #
# CREATE SHELL SCRIPT EXECUTION LOGIC
# =============================================================================================================== #

if [ ! -d "$ENV_FILE" ] 
then
    echo "Virtual Environment DOES NOT exist."
    python3 -m venv env
    echo "Activate the virtual environment"
    activate
else echo "Environment already exists"
fi

if [ ! -f "$IGNORE_FILE" ];then

    createGitignore
    writeToGitignore

else echo ".gitignore file exists"
fi
