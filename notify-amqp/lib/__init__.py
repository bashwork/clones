import NotifyAMQP

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
