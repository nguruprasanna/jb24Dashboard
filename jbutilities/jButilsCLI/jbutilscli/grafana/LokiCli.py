import pytz
import datetime
import json
import requests
import os
import sys
import getopt
import pdb
import datetime

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


class Loki:
    def __init__(self):
        '''
        Init version for comotail
        '''
        self.__version__ = "0.0.1"

    def send_to_loki(self,comodict):
        '''
        Send to loki. Receive comodict and send to url given in settings
        '''
        # example of usage grafana/loki api when you need push any log/message from your python scipt


        host = 'localhost'
        curr_datetime = comodict['comodatetime']
        
        if curr_datetime:
            print('Date-time:', curr_datetime)
            curr_datetime = curr_datetime.isoformat('T')
            print('Date-time_iso:', curr_datetime)
        else:
            curr_datetime = datetime.datetime.now(pytz.timezone('Europe/Ljubljana'))
            curr_datetime = curr_datetime.isoformat('T')
            print('Date-time_iso2:', curr_datetime)
        msg=comodict['comomsg']
        if msg:
            pass
        else:
            msg = 'On server {host} detected error'.format(host=host)

        # push msg log into grafana-loki
        url = 'http://localhost:3100/api/prom/push'
        headers = {
            'Content-type': 'application/json'
        }
        #'labels': '{source=\"Temenos Transact \",job=\"COMO\", comotime=\"' + comodict['comotime'] + '\",batchname=\"'+ comodict['comobatname'] + '\",jobname=\"' + comodict['comojobname'] + '\",' + 'host=\"' + host + '\"}',
        payload = {
            'streams': [
                {
                    'labels': '{source=\"Temenos Transact \",job=\"COMO\", comotime=\"' + comodict['comotime'] + '\",batchname=\"'+ comodict['comobatname'] +  '\",' + 'host=\"' + host + '\"}',
                    'entries': [
                        {
                            'ts': curr_datetime,
                            'line': "[" + comodict['comoinfo'] + "]" + comodict['comofull']
                        }
                    ]
                }
            ]
        }
        #pdb.set_trace()
        payload = json.dumps(payload)
        answer = requests.post(url, data=payload, headers=headers)
        pdb.set_trace()
        response = answer.text
        
        # end pushing
        return response

