#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#***********************************************************************//
#******************  DARK HORSE NEURO MED Python API  ******************//
#***********************************************************************//

# Written by Matt Stead and Dan Crepeau
# Copyright Dark Horse Neuro Inc, 2022

# Third party imports
import numpy as np

# Local imports
from .med_file.dhnmed_file import (open_MED, read_MED, close_MED, read_session_info)

class MedSession():
    """
    Basic object for operations with MED sessions.

    Parameters
    ----------
    session_path: str
        path to MED session
    password: str
        password for MED session
    new_session: bool
        whether this is a new session for writing (default=False)
    read_metadata: bool
        whether to read metadata (default=True)
    check_all_passwords: bool
        check all files or just the first one encoutered(default=True)
    """
    
    class OpenSessionException(Exception):
        pass
        
    class ReadSessionException(Exception):
        pass
    
    
    # private member __pointers is a tuple that contains 3 pointers:
    #   (globals_m11, globals_d11, session)
    __pointers = None


    def __init__(self, session_path, password=None, reference_channel=None):
    
        if password is not None and reference_channel is not None:
            self.__pointers = open_MED(session_path, password, reference_channel)
        if password is not None and reference_channel is None:
            self.__pointers = open_MED(session_path, password)
        if password is None and reference_channel is None:
            self.__pointers = open_MED(session_path)
        
        if self.__pointers is None:
            raise MedSession.OpenSessionException("Unable to open session: " + str(session_path))
            
        # read channel/session metadata
        self.session_info = read_session_info(self.__pointers)
        
        return
        

    def readByTime(self, start_time, end_time):
    
        if self.__pointers is None:
            raise MedSession.ReadSessionException("Unable to read session!  Session is invalid.")
        
        self.data = read_MED(self.__pointers, start_time, end_time)
        return
        
        
    def readByIndex(self, start_idx, end_idx):
    
        if self.__pointers is None:
            raise MedSession.ReadSessionException("Unable to read session!  Session is invalid.")
        
        self.data = read_MED(self.__pointers, "no_entry", "no_entry", start_idx, end_idx)
        return
        
    def close(self):
    
        close_MED(self.__pointers);
        self.__pointers = None
        return;
        
    def __del__(self):
    
        if self.__pointers is not None:
            self.close()
        return
    
