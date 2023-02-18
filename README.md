## AIOPlanner
# Steps to Install the Virtual Environment (if you have Python installed already):
(Make sure python and pip are up to date)
1. Pull the repository into a local folder using git clone "URL" [photo]
2. Change your working directory to the git repository folder [photo]
3. Check the branch you are in... if it says main, use this command --> "git checkout development" if you are in git bash or switch the branch to development if you are using a Git GUI [photo]
4. In your terminal, make sure your working directory is the AIOPlanner repository. Type this command: source env/Scripts/activate         (you can exit the virtual environment by pressing CTRL+D) [photo]
5. Install Flask and Flask Alchemy: pip3 install flask flask-sqlalchemy [photo]
6. Test the application by typing python3 app.py or python app.py (depending on your python version) [photo]
7. To see the app, run that in localhost: http://127.0.0.1:5000

#If you do not have Python and pip installed --> "python command not found" or "pip command not found":
Go to Python website: https://www.python.org
Download Python [photo]
Check your version to see if it is installed properly --> python3 --version
