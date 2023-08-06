#!/usr/bin/env python
# coding: utf-8

# Author : Alex Richardson
# Initial Date: Sept 8, 2022
# About: strymread class to read CAN data from CSV file captured using
# libpanda (https://jmscslgroup.github.io/libpanda/). Cribbed from Rahul's code
# such that it has almost no major dependencies like tensorflow now. We lost about 21 methods
# related largely to plotting and advanced signal processing.
# Read associated README for full description
# License: MIT License

#   Permission is hereby granted, free of charge, to any person obtaining
#   a copy of this software and associated documentation files
#   (the "Software"), to deal in the Software without restriction, including
#   without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:

#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
#   ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
#   TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#   PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
#   SHALL THE AUTHORS, COPYRIGHT HOLDERS OR ARIZONA BOARD OF REGENTS
#   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
#   AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#   OR OTHER DEALINGS IN THE SOFTWARE.

__author__ = 'Alex Richardson'
__email__  = 'william.a.richardson@vanderbilt.edu'

# For System and OS level task
import sys, getopt

## General Data processing and visualization Import

import time
import ntpath
import datetime
import numpy as np

import pandas as pd # Note that this is not commai Panda, but Database Pandas
import os
import copy

# cantools import
import cantools
from . import DBC_Read_Tools as dbc
import pkg_resources
from subprocess import Popen, PIPE

from .utils import configure_logworker
LOGGER = configure_logworker()

dbc_resource = ''

try:
    import importlib.resources as pkg_resources
    with pkg_resources.path('strymread_lite', 'dbc') as rsrc:
        dbc_resource = rsrc
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    print("Python older than 3.7 detected. ")
    try:
        import importlib_resources as pkg_resources
        with pkg_resources.path('strymread_lite', 'dbc') as rsrc:
            dbc_resource = rsrc
    except ImportError:
        print("importlib_resources not found. Install backported importlib_resources through `pip install importlib-resources`")

import vin_parser as vp

class strymread_lite:
    '''
    `strymread` reads the logged CAN data from the given CSV file.
    This class provides several utilities functions

    Parameters
    ----------------
    csvfile: `str`, `pandas.DataFrame`,  default = None
        The CSV file to be read. If `pandas.DataFrame` is supplied, then csvfile is set to None
        PandasDataFrame, if provided, must have  columns ["Time", "Message", "MessageID", "Bus"]

    dbcfile: `str`,  default = ""
        The DBC file which will provide codec for decoding CAN messages

    kwargs: variable list of argument in the dictionary format

    bus: `list` | default = None
        A list of integer correspond to Bus ID.

    dbcfolder: `str` | default = None
        Specifies a folder path where to look for appropriate dbc if  dbcfile='' or dbcfile = None
        Appropriate dbc file can be inferred from <brand>_<model>_<year>.dbc
        If dbcfolder  is None or empty string, then by default, strymread will look for dbc file in the dbc folder of the package where we ship sample dbc file to work with.

    verbose: `bool`
        Option for verbosity, prints some information when True

    Attributes
    ---------------
    dbcfile: `str`, default = ""
        The filepath of DBC file

    csvfile:`str`  | `pandas.DataFrame`
        The filepath of CSV Data file, or, raw  CAN Message DataFrame

    dataframe: `pandas.Dataframe`
        Pandas dataframe that stores content of csvfile as dataframe

    dataframe_raw: `pandas.Dataframe`
        Pandas original dataframe with all bus IDs. When `bus=` is passed to the constructor to filter out dataframe based on bus id, then original dataframe is save
        in dataframe_raw

    candb: `cantools.db`
        CAN database fetched from DBC file

    burst: `bool`
        A boolean flag that checks if CAN data came in burst. If `True`, then CAN Data was captured in burst, else
        `False`. If CAN Data came in burst (as in say 64 messages at a time or so)
        then any further analysis might not be reliable. Always check that.

    success: `bool`
        A boolean flag, if `True`, tells that reading of CSV file was successful.

    bus: `list` | default = None
        A list of integer correspond to Bus ID.

    dbcfolder: `str` | default = None
        Specifies a folder path where to look for appropriate dbc if `dbcfile=""` or `dbcfile = None`
        Appropriate dbc file can be inferred from <brand>_<model>_<year>.dbc
        If dbcfolder  is None or empty string, then by default, strymread will look for dbc file in package's dbcfolder
        where we ship sample dbc file to work with.

    database: `str`
        The name of the database corresponding to the model/make of the vehicle from which the CAN data
        was captured

    inferred_dbc: `str`
        DBC file inferred from the name of the csvfile passed.


    Returns
    ---------------
    `strymread`
        Returns an object of type `strymread` upon successful reading or else return None

    Example
    ----------------
    >>> import strym
    >>> from strym import strymread
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> dbcfile = 'newToyotacode.dbc'
    >>> csvdata = '2020-03-20.csv'
    >>> r0 = strymread(csvfile=csvdata, dbcfile=dbcfile)
    '''

    def __init__(self, csvfile, dbcfile = "", **kwargs):

       # success attributes will be set to True ultimately if everything goes well and csvfile is read successfully
        self.success = False



        if csvfile is None:
            print("csvfile is None. Unable to proceed with further analysis. See https://jmscslgroup.github.io/strym/api_docs.html#module-strym for further details.")
            return

        if isinstance(csvfile, pd.DataFrame):
            self.dataframe = csvfile
            self.csvfile = ''
            if ((len(dbcfile) == 0) or (dbcfile is None)):
                print("Please provide a valid dbcfile using argument `dbcfile` to strymread if you intend to supply a dataframe to strymread")
                return

        elif isinstance(csvfile, str):

            # Check if file exists
            if not os.path.exists(csvfile):
                print("Provided csvfile: {} doesn't exist, or read permission error".format(csvfile))
                return

            # if file size is less than 60 bytes, return without processing
            if os.path.getsize(csvfile) < 60:
                print("Nothing significant to read in {}. No further analysis is warranted.".format(csvfile))
                return

            self.csvfile = csvfile
            self.basefile = ntpath.basename(csvfile)
        else:
            print("Unsupported type for csvfile. Please see https://jmscslgroup.github.io/strym/api_docs.html#module-strym for further details.")

            return

        # Optional argument for verbosity
        self.verbose = kwargs.get("verbose", False)

        # Optional argument for bus ID
        self.bus = kwargs.get("bus", None)

        # Optional argument for dbcfolder where to look for dbc files
        self.dbcfolder = kwargs.get("dbcfolder", None)

        # If a single bus ID is passed, convert it to list of one item, if multiple bus ID
        # needs to be passed, then it must be passed as int
        if isinstance(self.bus, int):
            self.bus = [self.bus]

        # If data were recorded in the first then burst attribute will be set to True. In practical scenario, we won't proceeding
        # with further analysis when data comes in burst, however, if csvfile has data in burst, no real error will be raised. It
        # will be upto user to check attribute boolean for True/False
        self.burst = False

        if len(self.csvfile) > 0:
            # All CAN messages will be saved as pandas dataframe
            try:
                # Get the number of rows using Unix `wc` word count function

                is_windows = sys.platform.startswith('win')

                if not is_windows:
                    word_counts = Popen(['wc', '-l', self.csvfile], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    output, err = word_counts.communicate()
                    output = output.decode("utf-8")
                    output = output.strip()
                    output = output.split(' ')
                    n_lines = int(output[0])
                    if n_lines < 5:
                        print("Not enough data to read in the provided csvfile {}".format(ntpath.basename(self.csvfile)))
                        return
                    self.dataframe = pd.read_csv(self.csvfile,dtype={'Time': np.float64,'Bus':np.uint8, 'MessageID': np.uint32, 'Message': str, 'MessageLength': np.uint16}, nrows=n_lines - 2)

                else:
                    self.dataframe = pd.read_csv(self.csvfile,dtype={'Time': np.float64,'Bus':np.uint8, 'MessageID': np.uint32, 'Message': str, 'MessageLength': np.uint16}, skipfooter=2)


            except pd.errors.ParserError:
                print("Ill-formated CSV File. A properly formatted CAN-data CSV file must have at least following columns:  ['Time', 'Bus', 'MessageID', 'Message']")
                print("No data was written the csvfile. Unable to perform further operation")
                return
            except UnicodeDecodeError:
                print("Ill-formated CSV File. A properly formatted CAN-data  CSV file must have at least following columns:  ['Time', 'Bus', 'MessageID', 'Message']")
                print("No data was written to the csvfile. Unable to perform further operation")
                return
            except pd.errors.EmptyDataError:
                print("CSVfile is empty.")
                return

        if self.dataframe.shape[0] == 0:
            print("No data was present in the csvfile or pandas dataframe supplied is empty. Unable to perform further operation")
            return

        self.dataframe  = self.dataframe.dropna()

        if set(['Time', 'MessageID', 'Message', 'Bus']).issubset(self.dataframe.columns) == False:
            print("Ill-formated CSV File or pandas dataframe. A properly formatted CAN-data CSV file/dataframe must have at least following columns:  ['Time', 'Bus', 'MessageID', 'Message']")
            print("Unable to perform further operation")
            return

        if np.any(np.diff(self.dataframe['Time'].values) < 0.0):
            print("Warning: Timestamps are not monotonically increasing. Further analysis is not recommended.")
            return

        def vin(csvfile):
            """
            returns the vehicle identification number, VIN, (if detected) from the filename
            uses a very very simple method of looking for a 17 char string near the end of the filename

            Parameters
            --------------
            csvfile: `str`
                Parse VIN number from the name of the `csvfile`

            """

            # we use underscores to split up the filename
            splits = csvfile.split('_')
            candidates = []
            # print(f'The splits of the file are {splits}')
            for split in splits:
                # all VIN are 17 chars long
                if len(split) == 17:
                    # keep them in an array, in case the path has other 17 char elements
                    candidates.append(split)
            if len(candidates) >= 1:
                # return the end element, as none of our fileendings has 17 char elements at this time
                # HACK: if folks create _some17charfileending.csv then this will fail
                return candidates[-1]
            else:
                return 'VIN not part of filename'

        vin = vin(self.csvfile)
        brand = "toyota"
        model = "rav4"
        year = "2019"

        try:
            if vp.check_valid(vin) == True:
                brand = vp.manuf(vin)
                brand = brand.split(" ")[0].lower()
                try:
                    model = vp.online_parse(vin)['Model'].lower()
                except ConnectionError as e:
                    print("Retrieving model of the vehicle requires internet connection. Check your connection.")
                    return
                year = str(vp.year(vin))
                LOGGER.info("Vehicle model infered is {}-{}-{}".format(brand, model, year))

        except:
            if self.verbose:
                print('No valid vin... Continuing as Toyota RAV4. If this is inaccurate, please append VIN number to csvfile prefixed with an underscore.')

        self.inferred_dbc = "{}_{}_{}.dbc".format(brand, model, year)

        if (dbcfile is None) or(dbcfile==""):
            dbcfile = str(dbc_resource) + "/" + self.inferred_dbc

        if not os.path.exists(dbcfile):
            print("The dbcfile: {} doesn't exist, or read permission error".format(dbcfile))
            return

        # if control comes to the point, then the reading of CSV file was successful
        self.success = True

        self.dataframe =  self.timeindex(self.dataframe, inplace=True)
        self.dataframe_raw = None
        if self.bus is not None:
            if not np.all(np.isin(self.bus, self.dataframe['Bus'].unique())):
                print("One of the bus id not available.")
                print("Available BUS IDs are {}".format(self.dataframe['Bus'].unique()))
                self.success = False
                return
            else:
                self.dataframe_raw = self.dataframe.copy(deep = True)
                self.dataframe = self.dataframe[self.dataframe['Bus'].isin(self.bus)]

        # Check if data came in burst
        T = self.dataframe['Time'].diff()
        T_head = T[1:64]
        if np.mean(T_head) == 0.0:
            self.burst = True

        # DBC file that has CAN message codec
        self.dbcfile = dbcfile
        # save the CAN database for later use
        if self.dbcfile:
            self.candb = cantools.db.load_file(self.dbcfile)
        else:
            self.candb = None

        # initialize the dbc lookups for any particular usage
        # this creates the dict later used to figure out which signals/msgs to
        # use when decoding these data
        self._dbc_init_dict()

    def _set_dbc(self):
        '''
        `_set_dbc` sets the DBC file

        '''
        self.dbcfile = input('DBC file unspecified. Enter the filepath of the DBC file: ')
        if self.dbcfile:
            try:
                self.dbcfile = str(self.dbcfile)
                print("The new DBC file entered is: {}".format(self.dbcfile))
            except ValueError:
                print('DBC file entered is not a string')
                raise
        self.candb = cantools.db.load_file(self.dbcfile)

    def get_ts(self, msg, signal, verbose=False):
        '''
        `get_ts`  returns Timeseries data by given `msg_name` and `signal_name`

        Parameters
        -------------
        msg: `string` | `int`
            A valid message that can be found in the given DBC file. Can be specified as message name or message ID

        signal: `string` | `int`
            A valid signal in string format corresponding to `msg_name` that can be found in the given DBC file.  Can be specified as signal name or signal ID

        verbose: `bool`, default = False
            If True, print some information

        '''
        if not self.dbcfile:
            self._set_dbc()

        assert(isinstance(msg, int) or isinstance(msg, str)), ("Only Integer message ID or string name is supported for msg_name")

        assert(isinstance(signal, int) or isinstance(signal, str)), ("Only Integer signal ID or string name is supported for signal_name")

        if isinstance(msg, int):
            msg = dbc.getMessageName(msg, self.candb)
            if verbose:
                print("Message Name: {}".format(msg))

        if isinstance(signal, int):
            signal = dbc.getSignalName(msg, signal, self.candb)
            if verbose:
                print("Signal Name: {}\n".format(signal))

        # try-exception is fix for hybrid RAV4 since if you are using data
        # from a hybrid the accel message length is 4 vs. 8 in the Internal Combustion Engine

        ts = pd.DataFrame(columns = ["Time", "Message"])
        try:
            ts = dbc.convertData(msg, signal,  self.dataframe, self.candb)
        except ValueError as e:
            if (isinstance(msg, int) and msg == 552) or (isinstance(msg, str) and msg == 'ACCELEROMETER'):
                    if 'Short' in str(e):
                        LOGGER.info('Found RAV4 where acceleration messages are 4  bytes.')
                        self.dataframe = dbc.CleanData(self.dataframe,address=552)
                        ts = dbc.convertData(msg, signal,  self.dataframe, self.candb)
        return ts

    def messageIDs(self):
        '''

        Retreives list of all messages IDs available in the given CSV-formatted CAN data file.

        Returns
        ---------
        `list`
            A python list of all available message IDs  in the given CSV-formatted CAN data file.

        '''
        msgIDs = self.dataframe['MessageID'].unique()
        msgIDs.sort()
        return msgIDs

    def count(self):
        '''
        A utility function to return and optionally plot  the counts for each Message ID as bar graph

        Returns
        ----------
        `pandas.DataFrame`
            A pandas DataFrame with total message counts per Message ID and total count by Bus

        Example
        ---------
        >>> import strym
        >>> from strym import strymread
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> dbcfile = 'newToyotacode.dbc'
        >>> csvdata = '2020-03-20.csv'
        >>> r0 = strymread(csvfile=csvlist[0], dbcfile=dbcfile)
        >>> r0.count()
        '''
        dataframe = self.dataframe

        bus = dataframe['Bus'].unique()
        bus.sort()
        columns = ['Counts_Bus_' + str(int(s)) for s in bus]
        columns.insert(0, 'MessageID')
        all_msgs = self.messageIDs()
        dfx = pd.DataFrame(columns=columns)
        dfx['MessageID'] = all_msgs
        dfx.index = dfx['MessageID'].values

        countbybus = dataframe.groupby(['MessageID', 'Bus'])


        for key,item in countbybus:
            a_group = countbybus.get_group(key)
            dfx.at[key[0], 'Counts_Bus_{}'.format(int(key[1]))] = a_group.shape[0]

        dfx.fillna(0, inplace=True)

        dfx['TotalCount'] = 0
        for b in bus:

            dfx['TotalCount'] =  dfx['TotalCount'] + dfx['Counts_Bus_{}'.format(int(b))]

        return dfx

    def start_time(self):
        '''
        `start_time` retrieves the the human-readable  time when logging of the data started

        Returns
        ---------
        `str`
            Human-readable string-formatted time.
        '''
        return time.ctime(self.dataframe["Time"].iloc[0])

    def end_time(self):
        '''
        `end_time` retrieves the the human-readable  time  when logging of the data was stopped.

        Returns
        ---------
        `str`
            Human-readable string-formatted time.
        '''
        return time.ctime(self.dataframe["Time"].iloc[-1])

    def triptime(self):
        '''
        `triptime` retrieves total duration of the recording for given CSV-formatted log file in seconds.

        Returns
        ---------
        `double`
            Duration in seconds.

        '''
        duration = self.dataframe["Time"].iloc[-1] - self.dataframe["Time"].iloc[0]

        return duration

    def speed_raw(self, bus):
        '''
        Get Speed on All buss
        '''
        d=self.topic2msgs('speed')
        ts =  self.get_ts(d['message'],d['signal'])
        ts = ts[  ts['Bus'] == bus ]

        return ts

    def speed(self):
        '''
        Returns
        ---------
        `pandas.DataFrame`
            Timeseries speed data from the CSV file

        Example
        ----------
        >>> import strym
        >>> from strym import strymread
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> dbcfile = 'newToyotacode.dbc'
        >>> csvdata = '2020-03-20.csv'
        >>> r0 = strymread(csvfile=csvlist[0], dbcfile=dbcfile)
        >>> speed = r0.speed()

        '''
        # OLD
        # return self.get_ts('SPEED', 1)
        # NEW
        d=self.topic2msgs('speed')
        ts =  self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def speed_limit(self):
        '''
        Returns
        --------
        `pandas.DataFrame`
            Timeseries data for acceleration in speed limit from the CSV file

        '''
        # OLD
        # ts = self.get_ts('KINEMATICS', 'ACCEL_Y')

        d=self.topic2msgs('speed_limit')
        ts =  self.get_ts(d['message'],d['signal'])


        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def accely(self):
        '''
        Returns
        --------
        `pandas.DataFrame`
            Timeseries data for acceleration in y-direction from the CSV file

        '''
        # OLD
        # ts = self.get_ts('KINEMATICS', 'ACCEL_Y')

        d=self.topic2msgs('accely')
        ts =  self.get_ts(d['message'],d['signal'])



        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def accelx(self):
        '''
        Returns
        --------
        `pandas.DataFrame`
            Timeseries data for acceleration in x-direction  (i.e. longitudinal acceleration) from the CSV file

        '''

        # OLD
        # ts = self.get_ts('ACCELEROMETER', 'ACCEL_X')

        d=self.topic2msgs('accelx')
        ts =  self.get_ts(d['message'],d['signal'])


        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def accelz(self):
        '''
        Returns
        --------
        `pandas.DataFrame`
            Timeseries data for acceleration in z-direction  from the CSV file

        '''

        # OLD
        #ts = self.get_ts('ACCELEROMETER', 'ACCEL_Z')

        d=self.topic2msgs('accelz')
        ts =  self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def steer_torque(self):
        '''
        Returns
        --------
        `pandas.DataFrame`
            Timeseries data for steering torque from the CSV file

        '''


        # OLD
        # ts = self.get_ts('KINEMATICS', 'STEERING_TORQUE')

        d=self.topic2msgs('steer_torque')
        ts =  self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def yaw_rate(self):
        '''
        Returns
        ----------
        `pandas.DataFrame`
            Timeseries data for yaw rate from the CSV file

        '''

        # OLD
        # ts = self.get_ts('KINEMATICS', 'YAW_RATE')

        d=self.topic2msgs('yaw_rate')
        ts =  self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts


    def steer_rate(self):
        '''
        Returns
        ----------
        `pandas.DataFrame`
            Timeseries data for steering  rate from the CSV file

        '''

        # OLD
        # ts = self.get_ts('STEER_ANGLE_SENSOR', 'STEER_RATE')

        d=self.topic2msgs('steer_rate')
        ts =  self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def steer_angle(self):
        '''
        Returns
        --------
        `pandas.DataFrame`
            Timeseries data for steering  angle from the CSV file

        '''
#         signal_id = dbc.getSignalID('STEER_ANGLE_SENSOR', 'STEER_ANGLE', self.candb)
#         return self.get_ts('STEER_ANGLE_SENSOR', signal_id)
        d=self.topic2msgs('steer_angle')
        ts = self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts
    # NEXT

    def steer_fraction(self):
        '''
        Returns
        ----------
        `pandas.DataFrame`
            Timeseries data for steering  fraction from the CSV file

        '''

        # OLD
        # ts = self.get_ts('STEER_ANGLE_SENSOR', 'STEER_FRACTION')

        d=self.topic2msgs('steer_fraction')
        ts = self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def wheel_speed_fl(self):
        '''
        Returns
        ----------
        `pandas.DataFrame`
            Timeseeries data for wheel speed of front left tire from the CSV file

        '''

        # OLD
        # message = 'WHEEL_SPEEDS'
        # signal = 'WHEEL_SPEED_FL'
        # ts = self.get_ts(message, signal)

        d=self.topic2msgs('wheel_speed_fl')
        ts = self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def wheel_speed_fr(self):
        '''
        Returns
        ----------
        `pandas.DataFrame`
            Timeseeries data for wheel speed of front right tire from the CSV file

        '''

        # OLD
        # message = 'WHEEL_SPEEDS'
        # signal = 'WHEEL_SPEED_FR'
        # ts = self.get_ts(message, signal)

        d=self.topic2msgs('wheel_speed_fr')
        ts = self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def wheel_speed_rr(self):
        '''
        Returns
        ---------
        `pandas.DataFrame`
            Timeseeries data for wheel speed of rear right tire from the CSV file

        '''

        # OLD
        # message = 'WHEEL_SPEEDS'
        # signal = 'WHEEL_SPEED_RR'
        # ts = self.get_ts(message, signal)

        d=self.topic2msgs('wheel_speed_rr')
        ts = self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def wheel_speed_rl(self):
        '''
        Returns
        ----------
        `pandas.DataFrame`
            Timeseeries data for wheel speed of rear left tire from the CSV file

        '''

        # OLD
        # message = 'WHEEL_SPEEDS'
        # signal = 'WHEEL_SPEED_RL'
        # ts = self.get_ts(message, signal)

        d=self.topic2msgs('wheel_speed_rl')
        ts = self.get_ts(d['message'],d['signal'])

        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def rel_accel(self, track_id):
        '''
        utility function to return timeseries relative acceleration of detected object from radar traces of particular track id

        Parameters
        --------------
        track_id: int | `numpy array` | list

        Returns
        -----------
        `pandas.DataFrame` | `list<pandas.DataFrame>`
            Timeseries relative acceleration data from the CSV file

        '''
        df_obj = []
        if isinstance(track_id, int):
            if track_id < 0 or track_id > 15:
                raise ValueError("Invalid track id:{}".format(track_id))

            df_obj =self.get_ts('TRACK_B_'+str(track_id), 1)
        elif isinstance(track_id, np.ndarray) or isinstance(track_id, list):
            for id in track_id:
                if id < 0 or id > 15:
                    raise ValueError("Invalid track id:{}".format(track_id))

                df_obj1 =self.get_ts('TRACK_B_'+str(id), 1)
                if df_obj1.empty:
                    continue
                df_obj.append(df_obj1)

        return df_obj

    def long_dist(self, track_id):
        '''
        utility function to return timeseries longitudinal distance from radar traces of particular track id

        Parameters
        -------------
        track_id: `int` | `numpy array` | `list`

        Returns
        -----------
        `pandas.DataFrame` | `list<pandas.DataFrame>`
            Timeseries longitduinal distance data from the CSV file

        '''
        df_obj = []
        if isinstance(track_id, int):
            if track_id < 0 or track_id > 15:
                raise ValueError("Invalid track id:{}".format(track_id))

            df_obj =self.get_ts('TRACK_A_'+str(track_id), 1)
        elif isinstance(track_id, np.ndarray) or isinstance(track_id, list):
            for id in track_id:
                if id < 0 or id > 15:
                    raise ValueError("Invalid track id:{}".format(track_id))

                df_obj1 =self.get_ts('TRACK_A_'+str(id), 1)
                if df_obj1.empty:
                    continue
                df_obj.append(df_obj1)

        return df_obj

    def lat_dist(self, track_id):
        '''
        utility function to return timeseries lateral distance from radar traces of particular track id

        Parameters
        -------------
        track_id: int | `numpy array` | list

        Returns
        -----------
        `pandas.DataFrame` | `list<pandas.DataFrame>`
            Timeseries lateral distance data from the CSV file
        '''
        df_obj = []
        if isinstance(track_id, int):
            if track_id < 0 or track_id > 15:
                raise ValueError("Invalid track id:{}".format(track_id))

            df_obj =self.get_ts('TRACK_A_'+str(track_id), 2)
        elif isinstance(track_id, np.ndarray) or isinstance(track_id, list):
            for id in track_id:
                if id < 0 or id > 15:
                    raise ValueError("Invalid track id:{}".format(track_id))

                df_obj1 =self.get_ts('TRACK_A_'+str(id), 2)
                if df_obj1.empty:
                    continue
                df_obj.append(df_obj1)

        return df_obj

    def rel_velocity(self, track_id):
        '''
        utility function to return timeseries lateral distance from radar traces of particular track id

        Parameters
        -------------
        track_id: int | `numpy array` | list

        Returns
        -----------
        `pandas.DataFrame` | `list<pandas.DataFrame>`
            Timeseries lateral distance data from the CSV file
        '''
        df_obj = []
        if isinstance(track_id, int):
            if track_id < 0 or track_id > 15:
                print("Invalid track id:{}".format(track_id))
                raise
            df_obj =self.get_ts('TRACK_A_'+str(track_id), signal="REL_SPEED")
        elif isinstance(track_id, np.ndarray) or isinstance(track_id, list):
            for id in track_id:
                if id < 0 or id > 15:
                    print("Invalid track id:{}".format(track_id))
                    raise
                df_obj1 =self.get_ts('TRACK_A_'+str(id), signal="REL_SPEED")
                if df_obj1.empty:
                    continue
                df_obj.append(df_obj1)

        return df_obj

    def relative_leadervel(self):
        '''
        Utility function to return timeseries relative velocity of the leader obtained through all RADAR traces

        Parameters
        -----------


        Returns
        --------
        `pandas.DataFrame`
            Timeseries relative velocity of the leader

        '''

        long_dist = self.long_dist(np.arange(0, 16))
        lat_dist = self.lat_dist(np.arange(0, 16))
        rel = self.rel_velocity(np.arange(0, 16))
        # Concatenate long, lat and relative vel of all tracks to a single dataframe
        long_dist = pd.concat(long_dist)
        lat_dist = pd.concat(lat_dist)
        rel = pd.concat(rel)

        long_dist['Long'] = long_dist['Message']
        long_dist['Lat'] = lat_dist['Message']
        long_dist['Relvel'] = rel['Message']
        long_dist.drop(columns=['Message'], inplace=True)
        lead_state = long_dist
        lead_state.sort_values(by='Time', inplace=True)
        lead_state = lead_state[np.abs(lead_state['Lat']) <= 0.5]
        lead_rel = pd.DataFrame()
        lead_rel['Time'] = lead_state['Time']
        lead_rel['Message'] = lead_state['Relvel']
        return lead_rel

    def acc_state(self):
        '''
        Get the cruise control state of the vehicle

        Returns
        ---------
        `pandas.DataFrame`
            Timeseries data with different levels corresponding to different cruise control state

            "disabled": 2, "hold": 11, "hold_waiting_user_cmd": 10, "enabled": 6,  "faulted": 5;

        '''
        message = 'PCM_CRUISE_SM'
        signal = 'CRUISE_CONTROL_STATE'
        signal_id = dbc.getSignalID(message,signal, self.candb)
        df = self.get_ts(message, signal_id)
        df.loc[(df.Message == 'disabled'),'Message']=2
        df.loc[(df.Message == 'hold'),'Message'] = 11
        df.loc[(df.Message == 'hold_waiting_user_cmd'),'Message'] = 10
        df.loc[(df.Message == 'enabled'),'Message'] = 6
        df.loc[(df.Message == 'faulted'),'Message'] = 5

        return df

    def lead_distance(self):
        '''
        Get the distance information of lead vehicle

        Returns
        ----------
        `pandas.DataFrame`
            Timeseeries data for lead distance from the CSV file
        '''

        # OLD
        # ts = self.get_ts('DSU_CRUISE', 'LEAD_DISTANCE')

        d=self.topic2msgs('lead_distance')
        ts =  self.get_ts(d['message'],d['signal'])


        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        # We will remove the bus column as it is irrelevant to bus column
        # if we want to remove duplicates
        if 'Bus' in ts.columns:
            ts.drop(columns=['Bus'], inplace=True)

        ts = strymread_lite.remove_duplicates(ts)
        return ts

    def frequency(self):
        '''
        Retrieves the frequency of each message in a pandas.Dataframe()


        +-----------+----------+------------+---------+---------+---------+---------+
        | MessageID | MeanRate | MedianRate | RateStd | MaxRate | MinRate | RateIQR |
        +-----------+----------+------------+---------+---------+---------+---------+
        |           |          |            |         |         |         |         |
        +-----------+----------+------------+---------+---------+---------+---------+
        |           |          |            |         |         |         |         |
        +-----------+----------+------------+---------+---------+---------+---------+
        |           |          |            |         |         |         |         |
        +-----------+----------+------------+---------+---------+---------+---------+

        Returns
        ----------
        `pandas.DataFrame`
            Returns the a data frame containing mean rate, std rate, max rate, min rate, rate iqr

        '''

        messageIDs = self.messageIDs()

        f = pd.DataFrame()

        means = []
        medians = []
        maxs = []
        mins = []
        stds = []
        iqrs = []
        for ID in messageIDs:
            r = self.dataframe[self.dataframe['MessageID'] == ID]
            r = strymread_lite.remove_duplicates(r)
            tdiff = 1./r['Time'].diff()
            tdiff = tdiff[1:]
            means.append(np.mean(tdiff.values))
            medians.append(np.median(tdiff.values))
            maxs.append(np.max(tdiff.values))
            mins.append(np.min(tdiff.values))
            stds.append(np.std(tdiff.values))

            first_quartile = np.percentile(tdiff.values, 25)
            third_quartile = np.percentile(tdiff.values, 75)
            iqrs.append(third_quartile- first_quartile) #interquartile range

        f['MessageID'] = messageIDs
        f['MeanRate'] = means
        f['MedianRate'] = medians
        f['RateStd'] = stds
        f['MaxRate'] = maxs
        f['MinRate'] = mins
        f['RateIQR'] = iqrs

        return f

    def msg_subset(self, **kwargs):
        '''
        Get the subset of message dataframe  based on a condition.

        Parameters
        -------------

        conditions: `str` | `list<str>`

            Human readable condition for subsetting of message dataframe.
            Following conditions are available:

            - *lead vehicle present*: Extracts only those messages for which there was lead vehicle present.
            - *cruise control on*: Extracts only those messages for which cruise control is on.
            - *operand op x*: Extracts those messages for which operator `op` is operated on operand to fulfil `x`.

            Available operators `op` are `[>,<,==, !=, >=,<=]`

            Available operand `operand` are `[speed, acceleration, lead_distance, steering_angle, steering_rate, yaw_rate ]`.
            Details of operands are as follows:

            - speed: timeseries longitudinal speed of the vehicle
            - acceleration: timeseries longitudinal acceleration of the vehicle
            - lead_distance: timeseries distance of lead vehicle from the vehicle
            - steering_angle: timeseries steering angle of the vehicle
            - steering_rate: timeseries steering rate of the vehicle
            - yaw_rate: timeseries yaw rate of the vehicle

            For example, "speed < 2.3"

        time: (t0, t1)

            `t0` start elapsed-time
            `t1` end elapsed-time

            Extracts messages from time `t0` to `t1`. `t0` and `t1` denotes elapsed-time and not the actual time.

        ids: `list`

            Get message dataframe containing messages given the list `id`


        Returns
        -----------
        `strymread`
            Returns strymread object with a modified dataframe attribute

        '''
        df = None

        # Whole time by default
        time = (0, self.dataframe['Time'].iloc[-1] - self.dataframe['Time'].iloc[0])

        try:
            if isinstance(kwargs["time"], tuple):
                time = kwargs["time"]
            else:
                raise ValueError('Time should be specified as a tuple with first value beginning time, and second value as end time. E.g . time=(10.0, 20.0)')

        except KeyError as e:
            pass

        # All message IDs by default
        ids  = self.messageIDs()

        try:
            if isinstance(kwargs["ids"], list):
                ids = kwargs["ids"]
            elif isinstance(kwargs["ids"], int):
                ids = []
                ids.append(kwargs["ids"])
            else:
                raise ValueError('ids should be specified as an integer or a  list of integers.')

        except KeyError as e:
            pass

        df = self.dataframe[(self.dataframe['Time'] - self.dataframe['Time'].iloc[0] >= time[0]) & (self.dataframe['Time'] - self.dataframe['Time'].iloc[0] <= time[1])]
        df = df[df.MessageID.isin(ids)]

        conditions = None


        try:
            if isinstance(kwargs["conditions"], list):
                conditions = kwargs["conditions"]

            elif isinstance(kwargs["conditions"], str):
                conditions = []
                conditions.append(kwargs["conditions"])
            else:
                raise ValueError('conditions should be specified as a string or a  list of strings with valid conditions. See documentation for more detail..')

        except KeyError as e:
            pass

        if conditions is None:
            r_new = copy.deepcopy(self)
            r_new.dataframe = df
            return r_new

        subset_frames = []
        if conditions is not None:
            for con in conditions:
                slices = []
                index = None
                con = con.strip()
                con = " ".join(con.split()) # removee whitespace characters - even multiple of them and replaces them with a single whitespace

                # get all the meassages for which lead vehicle is present.
                if con.lower() == "lead vehicle present":
                    msg_DSU_CRUISE = self.get_ts('DSU_CRUISE', 6)
                    # 252m is read in the front when radar doesn't see any vehicle in the front.
                    index = msg_DSU_CRUISE['Message'] < 252

                elif con.lower() == "cruise control on":
                    acc_state = self.acc_state()
                    # acc state of 6 denotes that cruise control was enabled.
                    index = acc_state['Message'] == 6

                else:
                    conlower = con.lower()
                    constrip = conlower.split()
                    if len(constrip) < 3:
                        print("Unsupported conditions provided. See documentation for more details.")
                        raise ValueError("Unsupported conditions provided. See documentation for more details.")
                        return None

                    operators = ['<', '>', '>=','<=','==','!=']
                    operand = ['speed', 'acceleration', 'lead_distance', 'steering_angle', 'steering_rate', 'yaw_rate' ]

                    valuecheck = False
                    value = None
                    try:
                        value = float(constrip[2])
                        valuecheck = True
                    except ValueError:
                        valuecheck = False

                    # This is equivalent to pattern: `operator op value`
                    if (constrip[0] in operand) & (constrip[1] in operators) & (valuecheck):
                        if constrip[0] == 'speed':
                            speed = self.speed()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'acceleration':
                            acceleration = self.accelx()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'steering_angle':
                            steering_angle = self.steer_angle()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'steering_rate':
                            steering_rate = self.steer_rate()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'steering_rate':
                            steering_rate = self.steer_rate()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'yaw_rate':
                            yaw_rate = self.yaw_rate()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                    elif (constrip[0].split('.')[0].isdigit()) &  (constrip[0].split('.')[2].lower()  == 'message') & (constrip[1] in operators) & (valuecheck):
                        # above condition check something like 386.LONG_DIST.Message > 34.0 where 345 is a valid message id.
                        required_id =  int(constrip[0].split('.')[0])

                        if constrip[0].split('.')[1].isdigit():
                            required_signal = int(constrip[0].split('.')[1])
                        else:
                            required_signal = constrip[0].split('.')[1].upper()

                        if required_id not in self.messageIDs():
                            raise ValueError('Request Message ID {} was unavailable in the data file {}'.format(required_id,  self.csvfile))


                        ts = self.get_ts(required_id, required_signal)

                        bool_result = eval("ts " + constrip[1] + constrip[2])
                        index = bool_result['Message']

                # Get the list of time slices satisfying the given condition
                if (index is None):
                    continue
                slices = self.timeslices(index)
                for time_frame in slices:
                    sliced_frame = df.loc[time_frame[0]: time_frame[1]]
                    subset_frames.append(sliced_frame)

        if len(subset_frames) > 0:
            set_frames = pd.concat(subset_frames)
            r_new = copy.deepcopy(self)
            r_new.dataframe = set_frames
            return r_new
        else:
            print("No data was extracted based on the given condition(s).")
            return None

    def time_subset(self, **kwargs):
        '''
        Get the time slices satsifying a particular condition for the dataframe.

        Parameters
        -------------

        conditions: `str` | `list<str>`

            Human readable condition for subsetting of message dataframe.
            Following conditions are available:

        - "lead vehicle present": Extracts only those message for which there was lead vehicle present.

        Returns
        --------
        `list`
            A list of tuples with start and end time of slices. E.g. [(t0, t1), (t2, t3), ...] satisfying the given conditions

        '''

        conditions  = None
        try:
            if isinstance(kwargs["conditions"], list):
                conditions = kwargs["conditions"]

            elif isinstance(kwargs["conditions"], str):
                conditions = []
                conditions.append(kwargs["conditions"])
            else:
                raise ValueError('conditions should be specified as a string or a  list of strings with valid conditions. See documentation for more detail..')

        except KeyError as e:
            pass

        slices_set = []
        if conditions is not None:
            for con in conditions:
                slices = []
                index = None
                con = con.strip()
                con = " ".join(con.split()) # removee whitespace characters - even multiple of them and replaces them with a single whitespace
                # get all the meassages for which lead vehicle is present.
                if con.lower() == "lead vehicle present":
                    msg_DSU_CRUISE = self.get_ts('DSU_CRUISE', 6)
                    # 252m is read in the front when radar doesn't see any vehicle in the front.
                    index = msg_DSU_CRUISE['Message'] < 252

                elif con.lower() == "cruise control on":
                    acc_state = self.acc_state()
                    # acc state of 6 denotes that cruise control was enabled.
                    index = acc_state['Message'] == 6

                else:
                    conlower = con.lower()
                    constrip = conlower.split()
                    if len(constrip) < 3:
                        print("Unsupported conditions provided. See documentation for more details.")
                        raise ValueError("Unsupported conditions provided. See documentation for more details.")
                        return None

                    operators = ['<', '>', '>=','<=','==','!=']
                    operand = ['speed', 'acceleration', 'lead_distance', 'steering_angle', 'steering_rate', 'yaw_rate' ]

                    valuecheck = False
                    value = None
                    try:
                        value = float(constrip[2])
                        valuecheck = True
                    except ValueError:
                        valuecheck = False

                    # This is equivalent to pattern: `operator op value`
                    if (constrip[0] in operand) & (constrip[1] in operators) & (valuecheck):
                        if constrip[0] == 'speed':
                            speed = self.speed()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'acceleration':
                            acceleration = self.accelx()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'steering_angle':
                            steering_angle = self.steer_angle()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'steering_rate':
                            steering_rate = self.steer_rate()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'steering_rate':
                            steering_rate = self.steer_rate()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                        elif constrip[0] == 'yaw_rate':
                            yaw_rate = self.yaw_rate()
                            bool_result = eval(conlower)
                            index = bool_result['Message']

                    elif (constrip[0].split('.')[0].isdigit()) &  (constrip[0].split('.')[2].lower()  == 'message') & (constrip[1] in operators) & (valuecheck):
                        # above condition check something like 386.LONG_DIST.Message > 34.0 where 345 is a valid message id.
                        required_id =  int(constrip[0].split('.')[0])

                        if constrip[0].split('.')[1].isdigit():
                            required_signal = int(constrip[0].split('.')[1])
                        else:
                            required_signal = constrip[0].split('.')[1].upper()

                        if required_id not in self.messageIDs():
                            raise ValueError('Request Message ID {} was unavailable in the data file {}'.format(required_id,  self.csvfile))


                        ts = self.get_ts(required_id, required_signal)

                        bool_result = eval("ts " + constrip[1] + constrip[2])
                        index = bool_result['Message']

                # Get the list of time slices satisfying the given condition
                if (index is None):
                    continue
                slices = self.timeslices(index)
                slices_set.append(slices)

        return slices_set

    @staticmethod
    def create_chunks(df, continuous_threshold = 3.0, column_of_interest = 'Message'):
        """
        `create_chunks` computes separate chunks from a timeseries data.

        Parameters
        -------------
        df: `pandas.DataFrame`
            DataFrame that needs to divided into chunks

        continuous_threshold: `float`, Default = 3.0
            Continuous threshold above which we a change point detection is made, and signals start of a new chunk.

        column_of_interest: `str` , Default = "Message"
            Column of interest in DataFrame on which `continuous_threshold` should act to detect change point for creation of chunks

        plot: `bool`, Default = False
            If True, a scatter plot of Full timeseries of `df` overlaid with separate continuous chunks of `df` will be created.

        Returns
        ---------
        `list` of `pandas.DataFrame`
            Returns a list of DataFrame with same columns as `df`

        """
        if column_of_interest not in df.columns.values:
            print("Supplied column of interest not available in columns of supplied df.")
            raise

        if 'Time' not in df.columns.values:
            print("There is no Time column in supplied df. Please pass a df with a Time column.")
            raise



        # Messages such as acceleration, speed may come on multiple buses
        # as observed from data obtained from Toyota RAV4 and Honda Pilot
        # and often they are copy of each other, they can be identified as
        # duplicate if they were received with same time-stamp

        df = strymread_lite.remove_duplicates(df)

        chunksdf_list = []
        for i, msg in df.iterrows():

            if i == df.index[0]:
                start = i
                last = i
                continue

            # Change point detection
            if np.abs(msg[column_of_interest] - df.loc[last][column_of_interest]) > continuous_threshold:
                chunk = df.loc[start:last]
                start = i
                chunksdf_list.append(chunk)

            last = i

            # when the last message is read
            if i == df.index[-1]:
                chunk = df.loc[start:last]
                chunksdf_list.append(chunk)

        return chunksdf_list

    def topic2msgs(self,topic):
        '''
        Return a dictionary value with the message ID and signal name for this particular DBC file, based on
        the passed in topic name. This is needed because various DBC files have different default names and
        signal structures depending on manufacturer. This redirection provides robustness to strym when the
        dbc files are not standardized---as they will never be so.

        Parameters
        -------------
        topic: `string`
            The string name of the topic in question. Only limited topics are supported by default

        Returns
        -------------
        d: `dictionary`
            Dictionary with the key/value pairs for `message` and `signal` that should be
            passed to the corresponding strym function. To access the message signal, use
            d['message'] and d['signal']
        '''
        #import os
        #dbcshort=os.path.basename(self.dbcfile)
        dbcshort = self.inferred_dbc

        #print('dbcshort={},topic={},dict={}'.format(dbcshort,topic,self.dbcdict))
        d = self.dbcdict[dbcshort][topic]
        # TODO add an exception here if the d return value is empty
        return d

    def _dbc_addTopic(self,dbcfile,topic,message,signal):
        '''
        Add a new message/signal pair to a topic of interest for this DBC file. For example,
        the Toyota Rav4 speed is found in a CAN Message with message name SPEED and signal 1,
        but for a Honda Pilot the speed is in a message named ENGINE_DATA with signal 'XMISSION_SPEED'

        The use of this method allows the init function to consistently create dictionary entries
        that can be queried at runtime to get the correct message/signal pair for the DBC file in use,
        by functions that will be extracting the correct data.

        This function should typically be called only by _dbc_init_dict during initialization

        Parameters
        -------------
        dbcfile: `string`
            The stringname of the dbc file, without any path, but including the file extension

        topic: `string`
            The abstracted name of the signal of interest, e.g., 'speed'

        message: `string`
            The CAN Message Name from within the DBC file that corresponds to the topic

        signal: `string`
            The signal within the CAN message that provides the data of interest

        '''

        self.dbcdict[dbcfile][topic] = {'message': message, 'signal': signal}

    def _dbc_init_dict(self):
        '''
        Initialize the dictionary for all potential DBC files we are using. The name
        of the dbcfile (without the path) is used as the key, and the values are
        additional dictionaries that give the message/signal pair for signals of interest

        To add to this dictionary, take exising message/signal known pairs, and add them
        to the DBC file for which they are valid. The dictionary created by this init
        function is used by other functions to get the correct pairs for query.

        Parameters
        -------------
        None

        '''
        toyota_rav4_2019='toyota_rav4_2019.dbc'
        toyota_rav4_2020='toyota_rav4_2020.dbc'
        toyota_rav4_2021='toyota_rav4_2021.dbc'
        honda='honda_pilot_2017.dbc'

        self.dbcdict={  toyota_rav4_2019: { },
                        toyota_rav4_2020: { },
                        toyota_rav4_2021: { },
                        honda : { }
                     }

        self._dbc_addTopic(toyota_rav4_2019,'speed','SPEED',1)
        self._dbc_addTopic(toyota_rav4_2019,'speed_limit','RSA1','SPDVAL1')
        self._dbc_addTopic(toyota_rav4_2019,'steer_angle','STEER_ANGLE_SENSOR','STEER_ANGLE')
        self._dbc_addTopic(toyota_rav4_2019,'accely','KINEMATICS','ACCEL_Y')
        self._dbc_addTopic(toyota_rav4_2019,'accelx','ACCELEROMETER','ACCEL_X')
        self._dbc_addTopic(toyota_rav4_2019,'accelz','ACCELEROMETER','ACCEL_Z')
        self._dbc_addTopic(toyota_rav4_2019,'steer_torque','KINEMATICS','STEERING_TORQUE')
        self._dbc_addTopic(toyota_rav4_2019,'yaw_rate','KINEMATICS','YAW_RATE')
        self._dbc_addTopic(toyota_rav4_2019,'steer_rate','STEER_ANGLE_SENSOR','STEER_RATE')
        self._dbc_addTopic(toyota_rav4_2019,'steer_fraction','STEER_ANGLE_SENSOR','STEER_FRACTION')
        self._dbc_addTopic(toyota_rav4_2019,'wheel_speed_fl','WHEEL_SPEEDS','WHEEL_SPEED_FL')
        self._dbc_addTopic(toyota_rav4_2019,'wheel_speed_fr','WHEEL_SPEEDS','WHEEL_SPEED_FR')
        self._dbc_addTopic(toyota_rav4_2019,'wheel_speed_rr','WHEEL_SPEEDS','WHEEL_SPEED_RR')
        self._dbc_addTopic(toyota_rav4_2019,'wheel_speed_rl','WHEEL_SPEEDS','WHEEL_SPEED_RL')
        self._dbc_addTopic(toyota_rav4_2019,'lead_distance','DSU_CRUISE','LEAD_DISTANCE')



        self._dbc_addTopic(toyota_rav4_2020,'speed','SPEED',1)
        self._dbc_addTopic(toyota_rav4_2020,'speed_limit','RSA1','SPDVAL1')
        self._dbc_addTopic(toyota_rav4_2020,'steer_angle','STEER_ANGLE_SENSOR','STEER_ANGLE')
        self._dbc_addTopic(toyota_rav4_2020,'accely','KINEMATICS','ACCEL_Y')
        self._dbc_addTopic(toyota_rav4_2020,'accelx','ACCELEROMETER','ACCEL_X')
        self._dbc_addTopic(toyota_rav4_2020,'accelz','ACCELEROMETER','ACCEL_Z')
        self._dbc_addTopic(toyota_rav4_2020,'steer_torque','KINEMATICS','STEERING_TORQUE')
        self._dbc_addTopic(toyota_rav4_2020,'yaw_rate','KINEMATICS','YAW_RATE')
        self._dbc_addTopic(toyota_rav4_2020,'steer_rate','STEER_ANGLE_SENSOR','STEER_RATE')
        self._dbc_addTopic(toyota_rav4_2020,'steer_fraction','STEER_ANGLE_SENSOR','STEER_FRACTION')
        self._dbc_addTopic(toyota_rav4_2020,'wheel_speed_fl','WHEEL_SPEEDS','WHEEL_SPEED_FL')
        self._dbc_addTopic(toyota_rav4_2020,'wheel_speed_fr','WHEEL_SPEEDS','WHEEL_SPEED_FR')
        self._dbc_addTopic(toyota_rav4_2020,'wheel_speed_rr','WHEEL_SPEEDS','WHEEL_SPEED_RR')
        self._dbc_addTopic(toyota_rav4_2020,'wheel_speed_rl','WHEEL_SPEEDS','WHEEL_SPEED_RL')
        self._dbc_addTopic(toyota_rav4_2020,'lead_distance','DSU_CRUISE','LEAD_DISTANCE')



        self._dbc_addTopic(toyota_rav4_2021,'speed','SPEED',1)
        self._dbc_addTopic(toyota_rav4_2021,'speed_limit','RSA1','SPDVAL1')
        self._dbc_addTopic(toyota_rav4_2021,'steer_angle','STEER_ANGLE_SENSOR','STEER_ANGLE')
        self._dbc_addTopic(toyota_rav4_2021,'accely','KINEMATICS','ACCEL_Y')
        self._dbc_addTopic(toyota_rav4_2021,'accelx','ACCELEROMETER','ACCEL_X')
        self._dbc_addTopic(toyota_rav4_2021,'accelz','ACCELEROMETER','ACCEL_Z')
        self._dbc_addTopic(toyota_rav4_2021,'steer_torque','KINEMATICS','STEERING_TORQUE')
        self._dbc_addTopic(toyota_rav4_2021,'yaw_rate','KINEMATICS','YAW_RATE')
        self._dbc_addTopic(toyota_rav4_2021,'steer_rate','STEER_ANGLE_SENSOR','STEER_RATE')
        self._dbc_addTopic(toyota_rav4_2021,'steer_fraction','STEER_ANGLE_SENSOR','STEER_FRACTION')
        self._dbc_addTopic(toyota_rav4_2021,'wheel_speed_fl','WHEEL_SPEEDS','WHEEL_SPEED_FL')
        self._dbc_addTopic(toyota_rav4_2021,'wheel_speed_fr','WHEEL_SPEEDS','WHEEL_SPEED_FR')
        self._dbc_addTopic(toyota_rav4_2021,'wheel_speed_rr','WHEEL_SPEEDS','WHEEL_SPEED_RR')
        self._dbc_addTopic(toyota_rav4_2021,'wheel_speed_rl','WHEEL_SPEEDS','WHEEL_SPEED_RL')
        self._dbc_addTopic(toyota_rav4_2021,'lead_distance','DSU_CRUISE','LEAD_DISTANCE')


# NEXT
        self._dbc_addTopic(honda,'speed','ENGINE_DATA','XMISSION_SPEED')
        self._dbc_addTopic(honda,'steer_angle','STEERING_SENSORS','STEER_ANGLE')
        self._dbc_addTopic(honda,'accely','KINEMATICS','LAT_ACCEL')
        self._dbc_addTopic(honda,'accelx','VEHICLE_DYNAMICS','LONG_ACCEL')
        self._dbc_addTopic(honda,'steer_rate','STEERING_SENSORS','STEER_ANGLE_RATE')
        self._dbc_addTopic(honda,'steer_torque','STEERING_CONTROL','STEER_TORQUE')
        self._dbc_addTopic(honda,'wheel_speed_fl','WHEEL_SPEEDS','WHEEL_SPEED_FL')
        self._dbc_addTopic(honda,'wheel_speed_fr','WHEEL_SPEEDS','WHEEL_SPEED_FR')
        self._dbc_addTopic(honda,'wheel_speed_rr','WHEEL_SPEEDS','WHEEL_SPEED_RR')
        self._dbc_addTopic(honda,'wheel_speed_rl','WHEEL_SPEEDS','WHEEL_SPEED_RL')

    @staticmethod
    def remove_duplicates(df):
        '''
        Remove rows with duplicate time index from the timeseries data

        Parameters
        --------------
        df: `pandas.DataFrame`
            A pandas dataframe with at least one column `Time` or DateTimeIndex type Index
        '''
        # Usually timeseries have duplicated TimeIndex because more than one bus might produce same
        # information. For example, speed is received on Bus 0, and Bus 1 in Toyota Rav4.
        # Drop the duplicated index, if the type of the index pd.DateTimeIndex
        # Easier to drop the index, this way. If the type is not DateTime, first convert to DateTime
        # and then drop.
        if isinstance(df.index, pd.DatetimeIndex):
            df= df[~df.index.duplicated(keep='first')]

        else:
            df = strymread_lite.timeindex(df, inplace=True)
            df= df[~df.index.duplicated(keep='first')]

        return df


    @staticmethod
    def denoise(df, method="MA", **kwargs):
        '''
        Denoise the time-series dataframe `df` using `method`. By default moving-average is used.

        Parameters
        --------------
        df:  `pandas.DataFrame`
            Original Dataframe to denoise

        method: `string`, "MA"
            Specifies method used for denoising

            MA: moving average (default)

        window_size: `int`
            window size used in moving-average based denoising method

            Default value: 10

        Returns
        ------------
        `pandas.DataFrame`
            Denoised Timeseries Data

        '''
        window_size = 10

        try:
            window_size = kwargs["window_size"]
        except KeyError as e:
            pass


        df_temp = pd.DataFrame()
        df_temp['Time'] = df['Time']
        df_temp['Message'] = df['Message']

        if method == "MA":
            if window_size >=  df.shape[0]:
                print("Specified window size for moving-average method is larger than the length of time-series data")
                raise

            for index in range(window_size - 1, df.shape[0]):
                df_temp['Message'].iloc[index] = np.mean(df['Message'].iloc[index-window_size+1:index])

        return df_temp


    @staticmethod
    def split_ts(df, by=30.0):
        '''
        Split the timeseries data by `by` seconds

        Parameters
        ----------

        df: `pandas.DataFrame`
            dataframe to split

        by: `double`
            Specify the interval in seconds by which the timseries dataframe needs to split

        Returns
        -------

        `pandas.DataFrame`
            `dataframe` with an extra column *Second* denoting splits specified by interval

        `pandas.DataFrame` Array
            An array of splitted pandas Dataframe by Seconds


        '''
        dataframe = pd.DataFrame()
        dataframe['Time'] = df['Time']
        dataframe['Message'] = df['Message']
        initial_time = dataframe['Time'].iloc[0]
        second_elapsed = by
        dataframe['Second'] = 0.0
        for r, row in  dataframe.iterrows():
            next_time = initial_time + by
            if ((dataframe['Time'][r] >= initial_time) and (dataframe['Time'][r] <= next_time)):
                dataframe.loc[r, 'Second'] = second_elapsed
            if (dataframe['Time'][r] > next_time):
                initial_time = dataframe['Time'][r]
                second_elapsed = second_elapsed + by
                dataframe.loc[r, 'Second'] = second_elapsed

        df_split = []
        for second, df in dataframe.groupby('Second'):
            df_split.append(df)

        return dataframe, df_split

    @staticmethod
    def timeindex(df, inplace=False):
        '''
        Convert multi Dataframe of which on column must be 'Time'  to pandas-compatible timeseries where timestamp is used to replace indices
        The convesion happens with no time zone information, i.e. all Clock time are in GMT

        Parameters
        --------------

        df: `pandas.DataFrame`
            A pandas dataframe with two columns with the column names "Time" and "Message"

        inplace: `bool`
            Modifies the actual dataframe, if true, otherwise doesn't.

        Returns
        -----------
        `pandas.DataFrame`
            Pandas compatible timeseries with a single column having column name "Message" where indices are timestamp in hum  an readable format.
        '''

        if inplace:
            newdf = df
        else:
            newdf =df.copy(deep = True)

        Time = pd.to_datetime(newdf['Time'], unit='s')
        newdf.reset_index(drop=True, inplace=True)
        newdf['Clock'] = pd.DatetimeIndex(Time).tolist()

        if inplace:
            newdf.set_index('Clock', inplace=inplace)
        else:
            newdf = newdf.set_index('Clock')
        return newdf

    @staticmethod
    def dateparse(ts):
        '''
        Converts POSIX timestamp to human readable Datformat as per GMT

        Parameters
        -------------
        ts: `float`
            POSIX formatted timestamp

        Returns
        ----------
        `str`
            Human-readable timestamp as per GMT
        '''
        from datetime import datetime, timezone
        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        ts = float(ts)
        d = datetime.fromtimestamp(ts).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S:%f')
        return d

    @staticmethod
    def timeslices(ts):
        """
        `timeslices` return a set of timeslices in the form of `[(t0, t1), (t2, t3), ...]`
        from `ts` where ts is a square pulse (or a timeseries) representing two levels 0 and 1
        or True and False where True for when a certain condition was satisfied and False for
        when condition was not satisfied. For example: ts should be a pandas Series (index with timestamp)
        with values  `[True, True, True, ...., False, False, ..., True, True, True ]` which represents
        square pulses. In that case, `t0, t2, ...` are times for edge rising, and `t1, t2, ...` for edge falling.

        Parameters
        --------
        ts: `pandas.core.series.Series`
            A valid pandas time series with timestamp as index for the series

        Returns
        --------
        `list`
            A list of tuples with start and end time of slices. E.g. `[(t0, t1), (t2, t3), ...]`
        """

        if ts.dtypes == bool:
            ts = ts.astype(int)

        tsdiff = ts.diff()

        # diff creates a NaN in the first row, so that can affect the calculation.
        # In that case, we NaN can be replaced with 1 if there was True
        tsdiff[0] = ts[0]

        slices = []
        time_tuple = (None,  None)
        for index, row in tsdiff.iteritems():
            if row == 1:
                # Rising Edge Detected. We will get index to rising edge
                location_of_index = tsdiff.index.indexer_at_time(index)
                if time_tuple == (None, None):
                    required_index = tsdiff.index[location_of_index+1].tolist()
                    # time_tuple = (required_index[0], None)
                    time_tuple = (index, None)

            elif row == -1:
                # Falling Edge Detected. We will get index before falling edge
                location_of_index = tsdiff.index.indexer_at_time(index)
                if time_tuple[1] == None and time_tuple[0] != None:
                    required_index = tsdiff.index[location_of_index-1].tolist()
                    time_tuple = (time_tuple[0], required_index[0] )
                    #time_tuple = (time_tuple[0], index)
                    slices.append(time_tuple)
                    time_tuple = (None,  None)

        return slices
