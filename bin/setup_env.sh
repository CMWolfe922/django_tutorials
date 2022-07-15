python -m venv env
activate() {
    . env/Scripts/activate
    echo "Updating pip"
    pip install -U pip
    echo "Installing requirements to virtual environment"
    pip install -r requirements.txt
}
activate
