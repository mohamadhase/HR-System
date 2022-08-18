# internal imports
from HR import app

if __name__ == '__main__':
    #Run the application on defult port 5000 
    #Just for local development of the API
    app.run(debug=True,threaded=True)
