'''
Python Serialization Wrappers
-------------------------------------------------

These are helper functions to wrap deserializing
amqp messages from the specified format to their
python object representation.
'''
# pickle serializer
try: import cPickle as pickle
except ImportError: import pickle

# yaml serializer
import yaml
try:
    from yaml import CLoader as YLoader
except ImportError: from yaml import YLoader

# json serializer
try: import cjson as json
except ImportError: import json

# xml serializer
try: import pyxser
except ImportError: pass

#-------------------------------------------------------------------# 
# Helper Functions
#-------------------------------------------------------------------# 
def _default_message():
    ''' Decode a message that is plain text

    :param message: The message to pre-process
    :return: The pre-processed message
    '''
    return {'message': '', 'title': ''}

#-------------------------------------------------------------------# 
# Default Processing Functions
#-------------------------------------------------------------------# 
def text_process(message):
    ''' Decode a message that is plain text

    :param message: The message to pre-process
    :return: The pre-processed message
    '''
    return {'message': message or '', 'title': None}

def xml_process(message):
    ''' Decode a message from the xml format

    :param message: The message to pre-process
    :return: The pre-processed message
    '''
    try:
        message = pyxser.unserialize(obj=message, enc="utf-8")
    except: message = _default_message()
    return message

def yaml_process(message):
    ''' Decode a message from the yaml format

    :param message: The message to pre-process
    :return: The pre-processed message
    '''
    try:
        message = yaml.load(message, Loader=YLoader)
    except: message = _default_message()
    return message

def json_process(message):
    ''' Decode a message from the json format

    :param message: The message to pre-process
    :return: The pre-processed message
    '''
    try:
        message = json.loads(message)
    except: message = _default_message()
    return message

def pickle_process(message):
    ''' Decode a message from the pickle format

    :param message: The message to pre-process
    :return: The pre-processed message
    '''
    try:
        message = pickle.loads(message)
    except: message = _default_message()
    return message

#-------------------------------------------------------------------# 
# Exports
#-------------------------------------------------------------------# 
__all__ = [
    'pickle_process', 'json_process', 'xml_process',
    'yaml_process', 'text_process']

