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

This script is used to download, checksum and update the FROGs dataset on
 the NCI server
The dataset is stored in /g/data/ua8/Precipitation/FROGs
The code logs files checksums are currently in /g/data/ua8/Working/Download/FROGs
Modified version of a code originally from Pauline Mak
 Last change:
 2021-11-23
 2022-02-02 Added get_credentials function
 """

import os
import hashlib
import logging
from ftplib import FTP, all_errors
from datetime import datetime
from time import gmtime, strptime


class FTPGetter():
    def __init__(self, ftpHost, check="", extension=".nc", user=None,
                 pwd=None, flog="download.log", level="debug"):
        """Initiate instance of FTPGetter

        Parameters
        ----------
        ftpHost: str
            ftp address
        check: str, optional
            To see if local files need updating, mdate to use modified
            date, md5sum to use checksum (slower), "" don't check.
            (default="")
        extension: str, optional
            File extension to download is used to filter files
            (default=".nc")
        user: str, optional
            Username for login, (default is None)
        pwd: str, optional
            Password for login, (default is None)
        flog: str, optional
            Name of log file (default="download.log")
        level: str, optional
            Logging level (default="debug")
        """
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.check = check
        self.extension = extension
        self.ftp = FTP(ftpHost)
        if user:
            if pwd is None:
                raise Exception("Password needed to login as user")
            self.ftp.login(user, pwd)
        else:
            self.ftp.login()
        # set up logger
        self.logger = self.set_log('log', flog, level=level)

        self.logger.debug(f"Check: {check}")
        self.logger.debug(f"Extension: {extension}")


    def set_log(self, name, fname, level):
        """Set up logging with a file handler

        Parameters
        ----------
        name: str
            Name of logger object
        fname: str
             Log output filename
        level: str
            Base logging level
        """

        # First disable default root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # start a logger
        logger = logging.getLogger(name)
        # set a formatter to manage the output format of our handler
        formatter = logging.Formatter(
            "%(asctime)s | %(message)s", "%H:%M:%S")
        minimal = logging.Formatter("%(message)s")
        if level == "debug": 
            minimal = logging.Formatter("%(levelname)s: %(message)s")
        # set the level passed as input, has to be logging.LEVEL not a string
        log_level = logging.getLevelName(level.upper())
        logger.setLevel(log_level)
        # add a handler for console this will have the chosen level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(minimal)
        logger.addHandler(console_handler)
        # add a handler for the log file, this is set to INFO level
        file_handler = logging.FileHandler(fname)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(minimal)
        logger.addHandler(file_handler)
        # return the logger object
        logger.propagate = False
        return logger
 

    def doDirectory(self, dirLine, makedir):
        """Process a directory return list of files and subdirs"""

        lineList = []
        if(dirLine[0] == 'd'):
            dirName = dirLine[(dirLine.rindex(" ") + 1):]
            self.logger.debug(f"do Directory dirName: {dirName}")
            if makedir:
               if(not os.path.exists(dirName)):
                  os.mkdir(dirName)
               os.chdir(dirName)  # go to "dataset" dir
            self.ftp.cwd(dirName)
            self.logger.debug(f"ftp: {self.ftp.pwd()}")
            self.ftp.retrlines("LIST", lineList.append)
        self.logger.debug(f"Dir listing: {lineList}")
        self.logger.debug(f"do Directory dirLine: {dirLine}")
        return lineList 


    def handleFile(self, baseDir, fileLine):
        """Handle files, call doFile if extension correspond"""

        if fileLine[0]== '-'  :
            try:    
                line = fileLine[(fileLine.rindex(" ") + 1):]
                filename = line.split(" ")[-1]
                idx = len(self.extension)
                if filename[-idx:] == self.extension:
                   self.doFile(baseDir, filename)    
            except ValueError as error:
                self.logger.debug("Handle file: {error}")
                pass


    def doFile(self, baseDir, filename):
        """Check if file to update or new and call downloadFile"""

        curDir = os.getcwd()
        update = False
        # if files exists and one check method was selected
        # compare to remote to check if to update
        if(os.path.exists(filename)):
            if self.check == 'md5sum':
                update = self.check_md5sum(filename)
            elif self.check == 'mdate':
                update = self.check_mdt(filename)
            if update is True:
               self.logger.info(f"file exists to update: {filename}")
            else:
                return
        # call download function and add file to list if successful
        result = self.downloadFile(filename, update)
        if result is True:
            if update is True:
                self.updatedFiles.append(os.path.abspath(filename))
            else:
                self.newFiles.append(os.path.abspath(filename))


    def check_md5sum(self, filename):
        """Check local and remote md5 checksum and return comparison

        This is much slower then checking modified date
        """

        m = hashlib.md5()
        self.ftp.retrbinary('RETR %s' % filename, m.update)
        ftp_md5 =  m.hexdigest()
        local_md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()
        self.logger.debug(f"File: {filename}")
        self.logger.debug(f"Local md5: {local_md5}")
        self.logger.debug(f"ftp md5: {ftp_md5}")
        different = local_md5 != ftp_md5
        return different


    def check_mdt(self,filename):
        """Check local and remote modified time and return comparison"""

        result = self.ftp.sendcmd("MDTM " + filename)
        remoteLastModDate = datetime(*(strptime(result[4:],
                                       "%Y%m%d%H%M%S")[0:6]))
        localModTime = datetime.fromtimestamp(
                       os.path.getmtime(filename))
        new = localModTime < remoteLastModDate
        self.logger.debug(f"File: {filename}")
        self.logger.debug(f"Local mod_date: {localModTime}")
        self.logger.debug(f"ftp mod_date: {remoteLastModDate}")
        self.logger.debug(f"update: {new}")
        return new


    def downloadFile(self, filename, isUpdate):
        """Download file

        If isUpdate is True save it to filename.1
        """

        if isUpdate:
            newFile = open(filename+".1", "wb")
        else:
            newFile = open(filename, "wb")
        try:
            try:
                self.logger.info(f"Trying to download file... {filename}")
                self.ftp.retrbinary(f"RETR {filename}", newFile.write)
                os.popen(f"chmod g+rxX {filename}").readline() 
                os.popen(f"chgrp ia39 {filename}").readline() 
            except Exception as e:
                self.errorFiles.append(f"{filename} could not be downloaded:")
                self.logger.error(e)
                return False 
        finally:
            newFile.close()
            if isUpdate:
               os.rename(f"{filename}.1", filename)
            return True


    def print_summary(self):
        """Print a summary of new, updated and error files to log file"""

        self.logger.info("==========================================")
        self.logger.info("Summary")
        self.logger.info("==========================================")
        self.logger.info("These files were updated: ")
        for f in self.updatedFiles:
            self.logger.info(f"{f}")
        self.logger.info("==========================================")
        self.logger.info("These are new files: ")
        for f in self.newFiles:
            self.logger.info(f"{f}")
        self.logger.info("==========================================")
        self.logger.info("These files and problems: ") 
        for f in self.errorFiles:
            self.logger.info(f"{f}")
        self.logger.info("\n\n") 


    def close(self):
        """Close ftp connection"""

        self.ftp.quit()


def get_credentials(fname, token=False):
    """Open file and read username/passowrd or token

    Requires information to be formatted as
    1st line: username
    2nd line: password
    or if token True
    1st line: token
    """

    f = open(fname, "r")
    lines = f.readlines()
    if token:
        utoken = lines[0].replace("\n","")
        credentials = (token,)
    else:
        uname = lines[0].replace("\n","")
        passw = lines[1].replace("\n","")
        credentials = (uname,passw)
    return credentials
