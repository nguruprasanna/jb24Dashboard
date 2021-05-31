import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import RegexMatchingEventHandler
import logging
from loguru import logger
from watchdog.events import FileCreatedEvent
from .comotailcli import comotailcli
from ..grafana import LokiCli


__copyright__ = """

    Copyright 2021 Guru Nagarajan, eSolveTech.

    Licensed under the NU General Public License , Version 3.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       https://www.gnu.org/licenses/gpl-3.0.en.html

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "GPLV3"



'''
Thanks to...
https://stackoverflow.com/questions/50593200/flask-application-with-watchdog-observer - if background needed
https://xiaoouwang.medium.com/tutorial-advanced-use-of-watchdog-in-python-excluding-files-a-git-auto-commit-example-part-7024913ad5a8

'''

class watchComo:
    def __init__(self,watchfolder=".",go_recursively = True, patterns=["(.*)tSA(.*)"], ignore_patterns=[], ignore_directories=False, case_sensitive=True, eXistingfiles=1):
        print("init watch")
        
        logger.info('Initializing watchdog')
        self.watchfolder= watchfolder
        self.patterns = patterns
        logger.debug(f"patterns { patterns } ")
        ignore_patterns.append("^./.git")
        ignore_patterns.append("^./.vscode")
        self.ignore_patterns= ignore_patterns
        logger.debug(f"ignore patterns { ignore_patterns }")

        self.ignore_directories = ignore_directories
        self.case_sensitive = case_sensitive
        self.eXistingfiles = eXistingfiles
        ##TODO##Removecode
        #regex support added - remove code!!
        #my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        #my_event_handler.__init__(ignore_regexes=['^[.]{1}.*', '.*/[.]{1}.*'])
        ##TODO##

        my_event_handler = RegexMatchingEventHandler(regexes=patterns,ignore_regexes=ignore_patterns, ignore_directories=ignore_directories, case_sensitive=case_sensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_deleted = self.on_deleted
        my_event_handler.on_modified = self.on_modified
        my_event_handler.on_moved = self.on_moved
        self.my_watch_handler = my_event_handler

        
        my_observer = Observer()
        my_observer.schedule(my_event_handler, watchfolder, recursive=go_recursively)
        self.my_watch_observer = my_observer
        logger.info('Initializing watchdog complete')
        print("started")
        self.comotailcli = comotailcli()
        #TODO# initialise dashboard based ons ettings grafana/splunk etc.
        self.dashBoard=LokiCli.Loki()

    def on_created(self,event):
        logger.debug(f"hey, {event.src_path} has been created!")
        #logger.debug(f"settings files received are { settings }")
        comodict=self.comotailcli.como_process(event.src_path)
        if comodict:
            resp=self.dashBoard.send_to_loki(comodict)
        else:
            resp=f"No data to send for { event.src_path }"
        logger.debug(f"response { resp }")

    def on_deleted(self,event):
        logger.debug(f"what the ! Someone deleted {event.src_path}!")

    def on_modified(self,event):
        logger.debug(f"hey buddy, {event.src_path} has been modified")
        comodict=self.comotailcli.como_process(event.src_path)
        resp=self.dashBoard.send_to_loki(comodict)
        logger.debug(f"response { resp }")

    def on_moved(self,event):
        logger.debug(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

    def startwatch(self):
        # Start the observer
        print("observer started")
        observer=self.my_watch_observer
        observer.start()
        if self.eXistingfiles:
            for file in os.listdir(self.watchfolder):
                filename = os.path.join(self.watchfolder, file)
                event = FileCreatedEvent(filename)
                #self.my_watch_handler.on_created(event)
                logger.debug(f"processing existing file { filename} ")
                self.my_watch_handler.dispatch(event)


        try:
            while True:
                # Set the thread sleep time
                #observer.join(2)
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
