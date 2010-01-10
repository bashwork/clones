'''
Python Notification Wrappers
-------------------------------------------------

These aim to be simple wrappers around various notification
librarires.
'''
try: import pynotify
except ImportError: pass

try: from Growl import GrowlNotifier
except ImportError: pass

#-------------------------------------------------------------------# 
# Classes
#-------------------------------------------------------------------# 
class Notifier(object):
    '''
    Base object for a notification client
    '''

    def notify(self, msg):
        ''' Create a new notification

        :param msg: The next message to alert the user with
        '''
        print "%s\n%s" % (msg['title'], msg['message'])

class GnomeNotifier(Notifier):
    '''
    Notifier wrapper for gnome dbus-notifications
    '''

    def __init__(self):
        ''' Inititialize a new instance of the Gnome Notifier'''
        pynotify.init('amqp-notify')
        self.image = None

    def notify(self, msg):
        ''' Create a new notification

        :param msg: The next message to alert the user with
        '''
        notify = pynotify.Notification(msg['title'], msg['message'], self.image)
        notify.show()

class GrowlNotifier(Notifier):
    '''
    Notifier wrapper for osx growl notifications
    '''

    def __init__(self):
        ''' Inititialize a new instance of the Gnome Notifier'''
        self._notify = GrowlNotifier(applicationName='amqp-notify',
                notifications=['amqp-notify'], defaultNotifications=['amqp-notify'])
        self._notify.register()
        self.image = None

    def notify(self, msg):
        ''' Create a new notification

        :param msg: The next message to alert the user with
        '''
        try:
            self._notify.notify('amqp-notify', msg['title'],
                msg['message'], self.image, True)
        except Exception, ex: pass

#-------------------------------------------------------------------# 
# Exports
#-------------------------------------------------------------------# 
__all__ = ['Notifier', 'GnomeNotifier', 'GrowlNotifier']
