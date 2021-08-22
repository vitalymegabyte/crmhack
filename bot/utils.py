import requests
#from handlers.text_handler import get_vector
import scipy.spatial.distance as ds
import numpy as np

def get_clients(user_id, text):
    r = requests.get('http://backend/get_clients/' + str(user_id), json={'text': text})
    data = r.json()
    return data