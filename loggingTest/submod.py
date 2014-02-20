#-* coding:UTF-8 -*
#!/usr/bin/env python

import logging  
    
logger = logging.getLogger('main.mod.submod')  
logger.info('logger of submod say something...')  
    
def tst():  
    logger.info('this is submod.tst()...')  

