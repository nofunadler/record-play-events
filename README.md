### Instructions
- install [python](https://www.python.org/downloads/) if you don't have it on your system
- go to your favorite location, create a new folder for the script and open a terminal session in that location. opening a session can be done by typing `cmd` and pressing `enter` in the folder's path bar (at the top of the folder window)
- create a virtual environment (to keep all script's dependencies self contained) by typing `python -m venv .venv`. this will create a new folder named `.venv` with all python runtime on it. this may take a few minutes
- activate the virtual environment with `.\.venv\Scripts\Activate.bat`
- run `pip install -r requirements.txt`
- launch the script with `python script.py`
- close your virtual environment with `deactivate`


### Customizations:
- passing different key names while invoking the program will change the `start` and `end` keys. e.g. `python script.py space enter` will change the start recording key to `space` and the end recording key to `enter`