from os.path import join, isdir, realpath
from os import makedirs
import logging
import logging.handlers

import xdg.BaseDirectory

cache_dir = realpath(join(xdg.BaseDirectory.xdg_cache_home, "gwibber"))

if not isdir(cache_dir):
  makedirs(cache_dir)

LOG_FILENAME = join(cache_dir, "gwibber.log")

def setup_logging(console = False, debuglog = False):
  log =  logging.getLogger()
  if debuglog:
    log.setLevel(logging.DEBUG)
  else:
    log.setLevel(logging.INFO)

  if console:
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(name)-12s %(threadName)-12s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(console_formatter)
    log.addHandler(console_handler)

  text_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20971520, backupCount=5)
  text_formatter = logging.Formatter("%(asctime)s - %(name)-12s %(threadName)-14s:  %(levelname)-8s - %(message)s")
  text_handler.setFormatter(text_formatter)
  log.addHandler(text_handler)

  log.info("Logger initialized")
