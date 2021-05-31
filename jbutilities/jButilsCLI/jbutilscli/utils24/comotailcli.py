import pytz
import datetime
import json
import requests
import os
import sys
import getopt
import pdb
import datetime
from loguru import logger


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


'''Does tail -f on log files in a given directory.
The display is last updated lines from the previous
display(or from the time of the start'''


class comotailcli:
    def __init__(self):
        '''
        Init version for comotail
        '''
        self.__version__ = "0.0.1"
        self.lineinfo= {}
        
    def comoline_process(self,lines):
        '''
        process each line and send back.
        '''
        comodict = {}
        lineslist=lines.split("\n")
        for line in lineslist:
            #print(line)
            parts = line.split("_")
            
            if len(parts) == 7:
                # partsnc = line.split("_",5)
                # comoparts = line.rstrip("\r\n")
                comodate = parts[4]
                comotime = parts[5]



                comodatetime_str = comodate + ' ' + comotime


                #%m is %b 
                ##possible to log old ones if config file as 
                ###limits_config:
                ###reject_old_samples: false
                ##outof order can be excluded by host. or other labels.
                comodatetime = datetime.datetime.strptime(comodatetime_str, '%d %b %Y %H:%M:%S')
                timezone = pytz.timezone("CET")
                with_timezone = timezone.localize(comodatetime)
                print(with_timezone)
                comodatetime=with_timezone

                comojobname=parts[2]
                comobatname = parts[1]
                comoinfo='INFO' 
                #dEFAULT - Add logic for error and como completed
                msg = parts[6]
                #other data to be added
                #TODO
                #Como server, error hadling, crashes, warning, more intelligence!

                # linedict={"time":comotime,"job":comojobname,"bat":"comobatname"}
                # print("sending....")
                # print(linedict["time"])
                # print(line)
                #send_to_loki(linedict["time"],line)
                comodict={'comodate':comodate,'comotime':comotime,'comobatname':comobatname,'comojobname':comojobname,'comoinfo':comoinfo,'comomsg':msg,'comofull':line,'comodatetime':comodatetime}
                #send_to_loki("",line,comotime,comobatname,comojobname)
                #self.send_to_loki(comodict)
        return comodict

    def como_process(self,filename):
        '''
        process como file and process each line.
        '''
        ##TODO##
        #store the data sent to loki in database (db file)
        #store first four lines of server information
        ##TODO##
        logger.debug(f'processing filename {filename}')
        file = open(filename, 'r')
        file.seek(0, 2)
        where = file.tell()
        lineinfo = self.lineinfo
        latest=""
        ts=""
        resp=""
        linedict={}
        if filename in lineinfo:
            prevline = lineinfo[filename]
            if prevline < where:
                    file.seek(prevline)
                    size = prevline-where
                    l = file.read(size)
                    lineinfo[filename] = where
                    #print(l.strip())
                    rl = l.strip()
                    linedict=self.comoline_process(rl)
                    resp = "sent"
                    #send_to_loki(linedict["time"],rl)
                    # Print the latest logged line
        else:
            lineinfo[filename] = where
            resp="no new data"
    
        self.lineinfo = lineinfo
        return linedict


    def Walk(self,root, recurse=0, pattern='*', return_folders=0 ):
        '''
        walk through all files and process
        '''
        import fnmatch, os, string
        
        # initialize
        result = []

        # must have at least root folder
        try:
            names = os.listdir(root)
        except os.error:
            return result

        # expand pattern
        pattern = pattern or '*'
        pat_list = string.splitfields( pattern , ';' )
        
        # check each file
        for name in names:
            fullname = os.path.normpath(os.path.join(root, name))

            # grab if it matches our pattern and entry type
            for pat in pat_list:
                if fnmatch.fnmatch(name, pat):
                    if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
                        result.append(fullname)
                    continue
                    
            # recursively scan other folders, appending results
            if recurse:
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    result = result + self.Walk( fullname, recurse, pattern, return_folders )
                
        return result
        
    def main(self):
        '''
        Original code. support for existing users to run independetly and using classic walk instead of watchdog.
        '''
        dirname = sys.argv[1]
        print(dirname)
        files = self.Walk(dirname, 1, '*', 1)
        if len(files) == 0:
            print('Empty directory!')
            sys.exit(1)
    #Set the filename and open the file

        for filename in files:

            print('printing file names', filename)
            
            lineinfo = {}
            latest=""
            ts=""
            while 1:
                for filename in files:
                        if filename.find('tSA'):
                            #pdb.set_trace()
                            file = open(filename, 'r')
                            file.seek(0, 2)
                            where = file.tell()
                        
                            if filename in lineinfo:
                                prevline = lineinfo[filename]
                                if prevline < where:
                                        file.seek(prevline)
                                        size = prevline-where
                                        l = file.read(size)
                                        lineinfo[filename] = where
                                        #print(l.strip())
                                        rl = l.strip()
                                        linedict= self.comoline_process(rl)
                                        #send_to_loki(linedict["time"],rl)
                                        # Print the latest logged line
                                else:
                                    lineinfo[filename] = where
                        


if __name__ == '__main__':
    comotail = comotailcli()
    comotail.main()

