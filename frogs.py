#!/usr/bin/python
"""
Copyright 2021 ARC Centre of Excellence for Climate Extremes 

author: Paola Petrelli <paola.petrelli@utas.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This script is used to download, checksum and update the FROGs dataset
on the NCI server.
The dataset is stored in /g/data/ua8/Precipitation/FROGs
The code logs files are currently in /g/data/ua8/Working/Download/FROGs
Uses FTPGetter class code in util.py which is a modified version of 
a code originally from Pauline Mak

Date created:
 2021-11-24
Last change:
 2022-05-31

"""

import os
import argparse
import logging
from util import FTPGetter
from datetime import datetime

def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='''Download FROGs 
             1DD_V1 precipitation regridded data from the IPSL ftp site.
             https://ftp.climserv.ipsl.polytechnique.fr/FROGs/1DD_V1/
             Usage: python frogs.py  ''',
             formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d','--debug', action='store_true', required=False,
                        help='Print out debug information, default is False')
    return vars(parser.parse_args())

def main():
    """Uses FTPGetter instance to start ftp session and download data

    If files already exists localy, to decide if updates are needed
    the variable 'check' (default is "") can be set to:
     - md5sum  it will compare md5sum for local and remote files
     - mdate it will use modified time
     NB md5sums is slow as it transfers the files first anyway
    """

    # Initialise getter instance
    # Set up log file with INFO level as default
    inputs=parse_input()
    level = "info"
    if inputs["debug"]:
        level = "debug"
    today = datetime.today().strftime('%Y-%m-%d')
    user = os.getenv("USER")
    root_dir = os.getenv("AUSREFDIR", "/g/data/jt48/aus-ref-clim-data-nci")
    flog = f"{root_dir}/frogs/code/update_log.txt"
    getter = FTPGetter("ftp.climserv.ipsl.polytechnique.fr",
                        check='mdate', extension=".nc", flog=flog, level=level)
    # connect to log
    data_log = getter.logger
    data_log.info(f"Updated on {today} by {user}")
    datasetName = "1DD_V1"
    localDir = f"{root_dir}/frogs/data/"
    remoteDir = "FROGs/"
    datasetList = []
    data_log.debug(f"Processing dataset... {datasetName}")
    getter.ftp.cwd(remoteDir + datasetName)   # go to dataset dir
    os.chdir(localDir + datasetName)   # go to dataset dir
    getter.ftp.retrlines("LIST", datasetList.append)
    for ds in datasetList[2:]:
        fileList = getter.doDirectory(ds,True)
        baseDir = os.getcwd()
        for f in fileList:
            getter.handleFile(baseDir, f)
        getter.ftp.cwd("../")  # get out of ftp dataset dir
        os.chdir("../")     #get out of local dataset dir

    getter.print_summary()
    getter.close()
    logging.shutdown()

if __name__ == "__main__":
    main()
