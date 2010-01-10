'''
Python AMQP Actor Wrapper
-------------------------------------------------

This aims to be a simple base class wrapper around
acting on new messages on a amqp queue. Either a base
class where a derieved class will overload a stop, start,
and process or a simple strategy injection for the three.
'''
from actor import Actor
from amqplib import client_0_8 as amqp

#-------------------------------------------------------------------# 
# Classes
#-------------------------------------------------------------------# 
class AMQPActor(Actor):
    '''
    Monitor a given AMQP stream and put the resulting messages
    on gnome notification alerts.
    '''

    def __init__(self, given_opts = {}):
        ''' Initialize a new instance of the AMQPActor monitor

        :param given_opts: The default options to the process
        '''
        Actor.__init__(self, given_opts)

    def initialize(self):
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

    def start(self, process=lambda x: x, action=lambda x: x):
        ''' Monitor a given AMQP stream

        :param process: A function that can preprocess the input
        '''
        message = process(message)
        action(message)

    def shutdown(self):
        ''' Stop the running amqp loop and disconnect from the bus

        Register to :INT
        '''
        self.chan.close()
        self.conn.close()

#-------------------------------------------------------------------# 
# Exports
#-------------------------------------------------------------------# 
__all__ = ['AMQPActor']
