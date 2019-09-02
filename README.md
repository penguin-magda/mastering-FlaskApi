If you use **Docker** build image based on Dockerfile, then run container and go.

If not follow below command in terminal:    
Create directory, where you clone repo:

    mkdir task
    cd task

Create and start virtual environment

    python3 -m venv venv    
    source venv/bin/activate
    
Clone repo:

    git clone <link-to-repo>

Go to app directory

    cd flask-api/

Install require packages

    pip install -r requirements.txt
    

Upgrade database

    flask db upgrade

Populate databasae with fake data

    flask populatedb artists
    flask populatedb hits
    
Run flask app

    flask run   

API sharing below endponts:
    
    [GET] api/v1/hits - displays a list of 20 hits sorted by the date of addition 
    [GET] api/v1/hits/<title_url> - displays details of single hit
    [POST] api/v1/hits - create new hit based on 'artist_id' and 'title'
    [PUT] api/v1/hits/<title_url> - update hit (only fields: 'artist_id', 'title' and 'title_url'
    [DELETE] api/v1/hits/<title_url> - delete hit