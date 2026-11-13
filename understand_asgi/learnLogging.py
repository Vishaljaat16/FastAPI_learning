from logging import *  


#* ----------- This all used to show or print values in console -----
# debug("This is an debug")
# warning("This is a warning")
# error("This is a Error")
# critical("This is a critical")


#* ---------- Now save to logging inside the file ------ 

# basicConfig(filename='understand_asgi/logfile.log', level=DEBUG)

# debug("This is an debug")
# warning("This is a warning")
# error("This is a Error")
# critical("This is a critical")

#* --------- Change the Log file mode --------------

# basicConfig(filename='understand_asgi/logfile.log', level=DEBUG, filemode='w')

# debug("This is an debug")
# warning("This is a warning")
# error("This is a Error")
# critical("This is a critical")


#* ---------- format -----------------

# basicConfig(filename='understand_asgi/logfile.log', level=DEBUG, filemode='w', format='%(asctime)s -- %(message)s')

# debug("This is an debug")
# warning("This is a warning")
# error("This is a Error")
# critical("This is a critical") 

# LOG_FORMAT = '%(asctime)s -- %(message)s // %(lineno)d'
# basicConfig(filename='understand_asgi/logfile.log', level=DEBUG, filemode='w', format=LOG_FORMAT)

# debug("This is an debug")
# info("This is an Info")
# warning("This is a warning")
# error("This is a Error")
# critical("This is a critical") 


#* --------- style ------------

LOG_FORMAT = '{lineno} *** {name} *** {asctime} *** {message}' 
basicConfig(filename='understand_asgi/logfile.log', level=DEBUG, filemode='w', format=LOG_FORMAT, style='{')

logger = getLogger('Vishal')

logger.debug("This is an debug")
logger.info("This is an Info")
logger.warning("This is a warning")
logger.error("This is a Error")
logger.critical("This is a critical")  