# Drop it!

A file hosting web app like dropbox made with flask with basic functionalities like
- login/register a user
- upload/delete files
- creating a directory structure
- sharing a file with another user
- view shared files
- view and download files to your system
- search files

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
python3 and A web browser with javascript enabled 
```

### Installing

Clone the repository on your local system
```
git clone https://github.com/shashijangra22/Drop-it.git
```
Open the directory

```
cd Drop-it
```
setup a virtual environment

```
python3 -m venv venv
```
activate the virtual environment
```
source venv/bin/activate
```
install the dependencies with a simple command
```
pip install -r modules.txt
```

initialise the database
```
flask db init
```
create migrations in the database

```
flask db migrate
```
upgrade to the latest migration
```
flask db upgrade
```
run a local server

```
flask run
```

Open `localhost:5000` on your web browser and enjoy !
## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The Web Framework 
* [pip](https://pip.pypa.io/en/stable/quickstart/) - Dependency Management
* [Python 3](https://docs.python.org/3/) - Server Side Scripting Language
* [MaterializeCSS](https://materializecss.com/) - CSS Framework
* [Jquery](https://api.jquery.com/) - Javascript Framework
* [HTML5/CSS3]()

## Contributing

Write code in modules so that we can easily test your code. Feel free to make pull requests!

## Authors

* **Shashi Jangra** 
* **Varun Gupta**  
* **Sarath Chandra** 
* **Yaswanth Koravi** 

## Acknowledgments

* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
