'''
'''
from optparse import OptionParser
import os

import yaml
from amqplib import client_0_8 as amqp
import pynotify

#-------------------------------------------------------------------# 
# Classes
#-------------------------------------------------------------------# 
class NotifyAMQP(object):
    '''
    Monitor a given AMQP stream and put the resulting messages
    on gnome notification alerts.
    '''

    def __init__(self, given_opts = {}):
        ''' Initialize a new instance of the NotifyAMQP monitor

        :param given_opts: The default options to the process
        '''
        opts = {'exchange':'amq.fanout', 'queue':'amqpgrowl'}
        opts.update(given_opts)
        self.image = os.path.abspath(os.path.join('..', 'resources', 'amqp.jpg'))
        self.title = "New Message On %s" % opts['queue']
        self.setup()

    def setup(self):
        ''' Initialize the amqp client

        Fix this and prolly just use txamqp
        '''
        self.conn = amqp.Connection(host="localhost:5672 ",
            userid=opts['username'], password=opts['password'],
            virtual_host=opts['vhost'], insist=False)
        self.chan = connection.channel()
        self.chan.queue_declare(queue=opts['queue'], durable=True,
            exclusive=False, auto_delete=False)
        self.chan.exchange_declare(exchange=opts['exchange'], type="direct",
            durable=True, auto_delete=False,)
        self.chan.queue_bind(queue=opts['queue'], exchange=opts['exchange'],
            routing_key=opts['key'])

    def monitor(self, process=lambda x: x):
        ''' Monitor a given AMQP stream

        :param process: A function that can preprocess the input
        '''
        message = process(message)
        notify = pynotify.Notification(self.title, message, self.image)
        notify.show()

    def stop(self):
        ''' Stop the running amqp loop and disconnect from the bus

        Register to :INT
        '''
        self.chan.close()
        self.conn.close()

    @staticmethod
    def _command_args():
        ''' Parse the command line arguments

        :return: The resulting command line arguments
        '''
        parser = OptionParser()
        parser.add_option("-q", "--queue", action="store", type="string",
            dest="queue", help="The name of the AMQP Queue to subscribe to")
        parser.add_option("-e", "--exchange", action="store", type="string",
            dest="exchange", help="The name of the AMQP exchange to bind to")
        parser.add_option("-k", "--key", action="store", type="string",
            dest="key", help="The routing key to bind to")
        parser.add_option("-v", "--vhost", action="store", type="string",
            dest="vhost", help="The name of the AMQP vhost to connect to")
        parser.add_option("-r", "--remote", action="store", type="string",
            dest="remote", help="The AMQP broker hostname")
        parser.add_option("-u", "--username", action="store", type="string",
            dest="username", help="The AMQP username")
        parser.add_option("-p", "--password", action="store", type="string",
            dest="password", help="The AMQP password")
        parser.add_option("-c", "--config", action="store", type="string",
            dest="config", help="Use the given configuration file for options")
        parser.add_option("-s", "--save", action="store", type="string",
            dest="save", help="Save the specified configuration to file")
        parser.add_option("-d", "--daemonize", action="store_true",
            dest="daemonize", help="Set to daemonize this process")
        opts, args = parser.parse_args()
        return opts.__dict__

    @staticmethod
    def _file_args(file):
        '''
        Parse configuration options from the config file
        
        :param file: The config file to parse or default
        :return: Dictionary of config file options
        '''
        try:
            with open(file) as stream:
                options = yaml.load(stream)
        except: options = None
        return options['notify'] if options else {}

    @staticmethod
    def process():
        '''
        Parse configuration options from command line and file
        
        :return: Dictionary of config file options
        '''
        opts = NotifyAMQP._command_args()
        if opts.has_key('config'):
            opts.update(NotifyAMQP.file_args(opts['config'])
        if opts.has_key('save'):
            with open(opts['save'], 'w') as stream:
               yaml.dump(opts, stream) 
        return opts

#-------------------------------------------------------------------# 
# Helper Functions
#-------------------------------------------------------------------# 
def start_server():
    '''
    Helper function to start and run the notify process
    '''
    options = NotifyAMQP.process()
    instance = NotifyAMQP(options)
    instance.monitor()

#-------------------------------------------------------------------# 
# Exports
#-------------------------------------------------------------------# 
__all__ = ['start_server', 'NotifyAMQP']
