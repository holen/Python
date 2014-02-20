#-* coding:UTF-8 -*
#!/usr/bin/env python
'''
Loggers expose(陈列) the interface that application code directly uses.
Handlers send the log records (created by loggers) to the appropriate(适合的) destination.
Filters provide a finer grained facility for determining which log records to output.
Formatters specify the layout of log records in the final output.
'''
import logging  
import logging.handlers  
  
LOG_FILE = 'tst.log'  
  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)   # 实例化formatter  
handler.setFormatter(formatter)      # 为handler添加formatter  
  
#logger = logging.getLogger('tst')    # 获取名为tst的logger  
logger = logging.getLogger(__name__)        # default is root 
logger.addHandler(handler)           # 为logger添加handler  
logger.setLevel(logging.DEBUG)  
  
logger.info('first info message')  
logger.debug('first debug message')  

# format args
'''
Format          Description
%(name)s        Name of the logger (logging channel).
%(levelno)s     Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
%(levelname)s   Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
%(pathname)s    Full pathname of the source file where the logging call was issued (if available).
%(filename)s    Filename portion of pathname.
%(module)s      Module (name portion of filename).
%(funcName)s    Name of function containing the logging call.
%(lineno)d      Source line number where the logging call was issued (if available).
%(created)f     Time when the LogRecord was created (as returned by time.time()).
%(relativeCreated)d     Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
%(asctime)s     Human-readable time when the LogRecord was created. By default this is of the form “2003-07-08 16:49:45,896” (the numbers after the comma are millisecond portion of the time).
%(msecs)d       Millisecond portion of the time when the LogRecord was created.
%(thread)d      Thread ID (if available).
%(threadName)s  Thread name (if available).
%(process)d     Process ID (if available).
%(message)s     The logged message, computed as msg % args.
'''
