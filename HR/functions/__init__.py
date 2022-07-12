import calendar
import datetime
from HR import db
def check_date(date_dict):
    if date_dict['Year']==0:
        return 'Year is invalid'

    if date_dict['Month'] < 1 or date_dict['Month'] > 12:
        return 'Month is not valid'
    if date_dict['Day'] < 1 or date_dict['Day'] > 31:
        return 'Day is not valid'
    try : 

        date = datetime.date(date_dict['Year'], date_dict['Month'], date_dict['Day'])
    except ValueError as e:
        return e.args[0]


    return True

def dict_to_datetime(date_dict):
    try :
        return datetime.date(date_dict['Year'], date_dict['Month'], date_dict['Day']).isoformat()
        
    except ValueError as e:
        return e.args[0]

def is_employee_exists(employee_id):
    pass    