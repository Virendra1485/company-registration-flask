# Server Set-up

## Prerequisites 
* python >= 3.8
* pip3

1. Clone the repository on you local machine with the command: 
    ```
    git clone https://github.com/Virendra1485/company-registration-flask.git
    ```
2. Now move to repo with command:
    ```
    cd company-registration-flask/
    ```
3. Then run command 

    ```
   sudo docker-compose up --build
   ```
4. Now open new terminal or command prompt and run

    ```
   sudo docker exec -it company-registration-flask_web_1 bash
   ```
   This will open a command line for docker web server
5. Now run commands.
    ```
   flask db upgrade
   flask initialize_data
   ```
6. Now you can access the server on 

    ```
   http://127.0.0.1:5000
   ```
