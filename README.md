Video sharing app made using django.

<h1>Setup django project:</h1>
Open your terminal and navigate to the directory you wish to store the project and run the following commands:
git clone https://github.com/Subash22/video-sharer.git

Once you've cloned the repository, navigate into the repository.

Create a virtual environment and activate it using the following commands:
python3 -m venv venv
source venv/bin/activate

Once you've activated your virtual environment install your python packages by running:
pip install -r requirements.txt

Now let's migrate our django project:
python manage.py migrate

If there are no issues, you should now be able to open your server by running:
python manage.py runserver

You can view api documentation here:
https://documenter.getpostman.com/view/15092668/UzQypiBt

Happy coding.😄
