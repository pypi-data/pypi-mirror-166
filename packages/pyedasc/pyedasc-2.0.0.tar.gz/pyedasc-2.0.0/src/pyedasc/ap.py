"""The code here aims to detect and analyze action potential waveforms in the 
abf files provided. The module contains 2 objects: Parameters and Plotting. 
The Parameters object includes methods for action potential peak detection,
resting potential points detection & fixation and parameter analysis. 

Objects
-------
Parameters(abf_file:str, voltage_channel_number:int, current_channel_number:int,
           sweep_number:int, absolute_rp_interval:list[int], ap_number:int=0, 
           peak_detection_threshold:int=None, rp_1_det:list[int]=None, 
           rp_2_det:list[int]=None, rp_3_det:list[int]=None, 
           rp_1_fixedP:int=None, rp_2_fixedP:int=None, rp_3_fixedP:int=None)
                 
Plotting(abf_file:str, voltage_channel_number:int, current_channel_number:int, 
         sweep_number:int, absolute_rp_interval:list[int], ap_number:int=0, 
         peak_detection_threshold:int=None, rp_1_det:list[int]=None, 
         rp_2_det:list[int]=None, rp_3_det:list[int]=None, 
         rp_1_fixedP:int=None, rp_2_fixedP:int=None, rp_3_fixedP:int=None)

"""
import os
import pyabf
import numpy as np
from celluloid import Camera

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.animation as animation
from scipy.signal import find_peaks

# local modules
from pyedasc import tools
from pyedasc import tools
otls = tools.OtherTools()

class Parameters():

    def __init__(self, abf_file, 
                 voltage_channel_number, 
                 current_channel_number, 
                 
                 absolute_rp_interval=None,
                 sweep_number=None,
                 ap_number=0, 
                 peak_detection_threshold=None,
                 
                 rp_1_det=None,
                 rp_2_det=None,
                 rp_3_det=None,
                 
                 rp_1_fixedP=None,  
                 rp_2_fixedP=None,   
                 rp_3_fixedP=None):
        
        """Detects action potentials in abf files and sets their limits in the 
        given voltage signal and analyzes specific parameters. 

        Parameters
        ==========
        
        #### abf_file : str
            ABF file name or path.
            
        #### voltage_channel_number : int
            Channel of voltage signal (numbering 0, n-1).
            
        #### current_channel_number : int
            Channel of current signal (numbering 0, n-1).
            
        #### sweep_number : int, optional
            Sweep to analyze (numbering 0, n-1), by default last sweep is 
            analyzed.
            
        #### absolute_rp_interval : list[int], optional
            A list of 2 integers that represent the index boundaries of the 
            analysis region for absolute resting potential value. The default 
            interval is the first 100 values.
            
        #### ap_number : int, optional
            Which of the detected action potentials will be analyzed, 
            by default 0 (first one).
            
        #### peak_detection_threshold : int, optional
            Voltage threshold for peak detection, by default None.
            
            
        ## RP points - second level of detection
    
        #### rp_1_det : list[int], optional
            List of 2 integers representing interval edges for rp1 point 
            detection, by default None.
            
        #### rp_2_det : list[int], optional
            List of 2 integers representing interval edges for rp2 point 
            detection, by default None.
            
        #### rp_3_det : list[int], optional
            List of 2 integers representing interval edges for rp3 point 
            detection, by default None.
            
            
        ## RP points - third level of detection
        
        #### rp_1_fixedP : int, optional
            Fixed point for rp1 point, by default None.
            
        #### rp_2_fixedP : int, optional
            Fixed point for rp2 point, by default None.
            
        #### rp_3_fixedP : int, optional
            Fixed point for rp3 point, by default None.
        
            
        Methods & Layout
        ================
        
        
        ## LOCAL TOOLS 
        
        #### sampleFactor(time_interval:float) -> int:
            Converts a time interval to equivalent number of points on signal, 
            regardless of abf file sample rate.
        
        #### time_subtraction(a:int, b:int) -> float:
            Returns time difference between two points on time axis.
        
        
        ## PEAK DETECTION 
        
        #### peaks() -> tuple:
            Detects action potentials (AP) as peaks on voltage channel, 
            over some threshold level, in mV.
            
        #### current_peak() -> tuple:
            Returns the value and the index of the currently selected action 
            potential, provided with the `ap_number` atribute, by the user. 
            `ap_number` is 0 by default.
            
        #### previous_peak() -> tuple:
            If multiple APs are detected in the trace and the ap_number > 1,
            returns the previous AP value and index.
            
        #### next_peak() -> int:
            If multiple APs are detected in the trace, returns the next 
            AP value and index.
            
        #### resting_potential() -> float:
            This method returns mean voltage value in selected interval, 
            from absolute_rp_interval[0] to absolute_rp_interval[1].
        
        
        ## DETECTION OF RP1, RP2 and RP3 
        
        #### rp_1() -> tuple:
            Returns information about rp_1 position, before the action 
            potential peak.
        
        #### rp_2() -> tuple:
            Returns information about rp_2 position, between the action 
            potential peak and rp_3.
            
        #### rp_3() -> tuple:
            Returns information about rp_3 position, after rp_2.
            
            
        ## INFO PRINTING 
        
        #### trace_info(sweep_number:int) -> str:
            Prints information about the number of action potentials,
            their amplitude, position on time axis and the sample number.
        
        #### __str__() -> str:
            Returns information about abf file path and RP values.
        
        #### __repr__() -> str:
            Returns information about Parameters object.
        
        
        ## AMPLITUDE PARAMETERS 
        
        #### threshold(method:str) -> tuple: 
            Calculate the action potential threshold by several methods. 
            Returns (value, index) according to the specified method.
            
        #### overshoot() -> float:
            Returns the positive voltage value at the AP peak (mV).
            
        #### total_amplitude() -> float:
            Returns AP total amplitude or AP size by adding positive resting
            potential value to overshoot value.
            
        #### afterhyperpolarization() -> tuple:
            Returns the minimum voltage value in interval from rp2 to rp3, 
            i.e. minimum voltage after falling phase.
   
        #### afterhyperpolarization_at(percentage) -> tuple:
            Returns the point where the ahp amplitude was recovered to 
            resting potential value, at a certain percentage.

        #### ahp_substracted_value() -> float:
            The value of ahp baselined at resting potential.


        ## DURATION PARAMETERS 
        
        #### ahp_recovery_time_at(percentage) -> float:
            Returns duration (ms) from ahp point to ahp recovery point at given
            procentage.
            
        #### ahp_time_constant() -> float:
            Isolates voltage signal from AHP to AHP80 and fit with 
            mono_exponential to find the ahp time constant.

        #### duration_at(level:str) -> tuple:
            Returns durations for different parameters of AP.

        #### phase_time(region:str) -> float:
            Returns durations for ascending (rising), descending (falling) 
            phases and also ahp.

        
        ## RATE PARAMETERS ###
        
        #### amplitude_over_time(region:str) -> float:
            Returns the voltage change over time, for rising & falling phases, 
            ahp 80% recovery and total recovery.

        #### growth_rate(region:str, percentage=False) -> float:
            Returns growth rate of voltage in specified region over total 
            amplitude.


        ## AREA 
        
        #### area(region:str) -> float:
            Returns the area of the selected region ('base', 'overshoot', 
            'rise', 'fall', 'upper-rise', 'upper-fall', 'lower-rise', 
            'lower-fall').
            
        #### shoulder_area() -> tuple:
            Returns the AP repolarization shoulder area.


        ## SLOPES 
        
        #### maximal_slope(phase:str) -> tuple:
            Returns the maximal slopes of rising and falling phases.


        ## DATA HANDLING
        
        #### data_loader() -> tuple:
            Returns lists with all parameteres and titles.
        """
        # ABF file initialization
        self.abf_file = abf_file
        self.abf = pyabf.ABF(self.abf_file)
        self.voltage_channel_number = voltage_channel_number
        self.current_channel_number = current_channel_number
        
        # Setting the sweep number, by default last one
        def current_sweep_number():
            """Returns the sweep number as parameter."""
            allSweeps = self.abf.sweepList
            if sweep_number == None:
                return allSweeps[-1]
            else:
                return sweep_number
        self.sweep_number = current_sweep_number()
        
        # Setting the absolute resting potential value detection inverval
        def absolute_rp():
            """Returns the absolute rp interval as a list of 2 values."""
            if absolute_rp_interval == None:
                # The default interval is the first 100 values of voltage.
                abs_rp_interval = [1, 100]
                return abs_rp_interval
            else:
                return absolute_rp_interval
        self.absolute_rp_interval = absolute_rp()
        
        # Setting which of the ap detected is analyzed, by default first one
        self.ap_number = ap_number

        # Extracting the abf file name from path
        self.abf_file_name = os.path.basename(os.path.normpath(self.abf_file))
        
        # Sample acquisition
        self.sampleHz = 1_000_000 # 1 Hz => 1 signal per 1_000_000 us
        self.sampleInterval = int(self.sampleHz / self.abf.sampleRate)
        self.totalPoints = len(self.abf.sweepY)
        self.recTime = (self.sampleInterval * self.totalPoints) / 1000 # ms    
        
        # Voltage threshold for peak detection   
        self.peak_detection_threshold = peak_detection_threshold
        
        # Second level of RP points detection
        self.rp_1_det = rp_1_det
        self.rp_2_det = rp_2_det
        self.rp_3_det = rp_3_det
        
        # Third level of RP points detection
        self.rp_1_fixedP = rp_1_fixedP
        self.rp_2_fixedP = rp_2_fixedP
        self.rp_3_fixedP = rp_3_fixedP
 

    # LOCAL TOOLS        
    
    def sampleFactor(self, time_interval):
        """Converts a time interval to equivalent number of points on signal,
        regardless of abf file sample rate.

        Parameters
        ----------
        time_interval : float
            The number of time units (in ms) to convert into points. 

        Returns
        ----------
        int
            The number of points corresponding to the desired time period.
            
        Examples
        ---------
        >>> # For a sampling rate of 10.00 kHz (interval 100.00 µs).
        >>> sampleFactor(time_interval=5) # 5 ms
        >>> 50
        >>> ... (5 * 1000) to seconds / 100 µs the interval  = 50 points
        """
        return int((time_interval * 1000) / self.sampleInterval) 
    
    
    def time_subtraction(self, a, b):
        """Returns time difference between two points on time axis.

        Parameters
        ----------
        a : int
            Minuend from substraction.
        b : int
            Subtrahend from substraction.

        Returns
        -------
        float
            Substraction difference, in ms.
        """
        minuend = self.abf.sweepX[a] * 1000 # ms
        subtrahend = self.abf.sweepX[b] * 1000 # ms
        difference = minuend - subtrahend
        return difference   


    # PEAK DETECTION
        
    def peaks(self):
        """Detects action potentials (AP) as peaks on voltage channel, 
        over some threshold level, in mV.

        Returns
        -------
            list : floats 
                Action potential peak(s) value(s) detected in the trace,
                in sweep n, given in mV. 
            list : integers
                Coresponding position on trace (index) for each AP peak 
                detected. 
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        heightTH = []
        if self.peak_detection_threshold is None:
            heightTH = 10 # mV
        else:
            heightTH = self.peak_detection_threshold
            # width
        indices, props = find_peaks(self.abf.sweepY, height=heightTH, width=1)
        apPeakValsRounded = [round(i, 2) for i in props['peak_heights']]
        apPeakInd = [int(i) for i in indices]
        return apPeakValsRounded, apPeakInd
    
    
    def current_peak(self):
        """Returns the value and the index of the currently selected action
        potential, provided with the ap_number atribute, by the user. 
        `ap_number` is 0 by default.

        Returns
        -------
        float
            Currently selected action potenial peak value.
        int
            Currently selected action potential peak index.
        """  
        return self.peaks()[0][self.ap_number], self.peaks()[1][self.ap_number]

    
    def previous_peak(self):
        """If multiple APs are detected in the trace and the ap_number > 1,
        returns the previous AP value and index.

        Returns
        -------
        float
            Previous action potenial peak value.
        int
            Previous action potential peak index.
        """
        if len(self.peaks()[1]) > 1:
            if self.ap_number > 0:
                idx = self.peaks()[1][self.ap_number-1]
                val = round(self.abf.sweepY[idx], 2)
                return val, idx
            else:
                print("The first AP in trace is selected (ap_number=1).")
        else:
            print("Only one AP detected in trace.")
    
    
    def next_peak(self):
        """If multiple APs are detected in the trace, 
        returns the next AP value and index.

        Returns
        -------
        float
            Next action potenial peak value.
        int
            Next action potential peak index.
        """
        if len(self.peaks()[1]) > 1:
            try:
                return self.peaks()[1][self.ap_number + 1]
            except IndexError:
                return self.current_peak()[1] + self.sampleFactor(20)
        else:
            print("Only one AP detected in trace.")
    
    
    def resting_potential(self):
        """This method returns mean voltage value in selected interval,
        from self.absolute_rp_interval[0] to self.absolute_rp_interval[1].

        Returns
        -------
        float
            Mean membrane potential value in specified range, in mV.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        limL = self.absolute_rp_interval[0]
        limR = self.absolute_rp_interval[1]
        rpInt = self.abf.sweepY[limL:limR]    
        resting_potential = np.mean(rpInt)
        return resting_potential
        

    # DETECTION OF RP1, RP2 and RP3
    
    def rp_1(self):
        """Returns information about rp_1 position, the last resting 
        potential-like value before the action potential peak.
        
        ### Default: automatic detection
        
        Automatic search for the value of rp1 is made in peak-25ms to peak
        interval. Divide every value in interval to RP absolute value and 
        extract the last value under 0.98. RP1 index is last value under 
        0.98 in abs rp divided list because this is where values clearly
        begin to shift away from resting voltage.
        
        ### Second level of detection
        
        User provided interval for rp1 detection: rp_1_det = [int,int]  
        -> Searching for the closest value to the absolute resting 
        potential in the interval specified by the user.
        
        ### Third level of detection
        
        User provided fixed point for rp_1: rp_1_fixedP = int 
        -> Fixed index point for rp1.
        
        Returns
        -------
        float
            Measured value of rp1, in mV.
        int
            Index of rp1, on voltage signal.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        absRP = self.resting_potential()
    
        if len(self.peaks()[1]) >= 1:
            
            if self.ap_number == 0:
                
                # If third level of detection is active
                if type(self.rp_1_fixedP) == int and self.rp_1_det == None:
                    rp_1_index = self.rp_1_fixedP
                    rp_1_value = self.abf.sweepY[rp_1_index]
                    return rp_1_value, rp_1_index
                
                # If second level of detection is active
                elif self.rp_1_det != None and self.rp_1_fixedP == None:
                    rp1 = self.rp_1_det
                    limL = rp1[0]
                    limR = rp1[1]
                    detectionInt = self.abf.sweepY[limL:limR]
                    rp_1_index = otls.find_nearest(detectionInt, absRP)[1] + limL
                    rp_1_value = self.abf.sweepY[rp_1_index]
                    return rp_1_value, rp_1_index
                
                # If second and third levels of detection are inactive
                elif self.rp_1_det == None and self.rp_1_fixedP == None:
                    # Set limits for detection interval, left: 25 ms before peak
                    peak_index = self.current_peak()[1]
                    limL = peak_index - self.sampleFactor(time_interval=25)
                    limR = peak_index - self.sampleFactor(time_interval=2)
                    # Divide every value in interval to RP absolute value
                    rp_divided = [(i / absRP) for i in self.abf.sweepY[limL:limR]]
                    # Loop through divided values and append indices of values 
                    # over 0.98 to new list 
                    index_holder = []
                    for index, value in enumerate(rp_divided):
                        if value > 0.98:
                            index_holder.append(index)
                    
                    ## Plot verification on rp divided values
                    # plt.plot(rp_divided, '-o')
                    # plt.plot(rp_divided[index_holder[-1]], 'D')
                    # plt.show()
                    
                    ## Plot verification on signal
                    # plt.plot(self.abf.sweepX, self.abf.sweepY, '-o')
                    # plt.plot(self.abf.sweepX[index], self.abf.sweepY[index], 'D')                  
                    # plt.show()

                    # NOTE: RP1 index is last value under 0.98 in abs rp divided list
                    # This is where values clearly begin to shift away from resting 
                    try:
                        rp_1_index = index_holder[-1] + limL
                        rp_1_value = round(self.abf.sweepY[rp_1_index], 2)
                        return rp_1_value, rp_1_index
                    
                    except IndexError:
                        # log here
                        # Explain
                        # try with second and third levels
                        # try to increase limL if rising phase seems to be higher
                        # than 20 ms ?
                        # last instance try to increase ? value threshold 
                        print("RP1 index not found.")
    
            elif self.ap_number >= 1:
                ppInt = self.abf.sweepY[self.previous_peak()[1]
                                        :self.current_peak()[1]]
                limL = otls.find_nearest(ppInt, min(ppInt))[1] + self.previous_peak()[1]
                limR = self.current_peak()[1]
                detectionInt = self.abf.sweepY[limL:limR]
                rp_1_index = otls.find_nearest(detectionInt, absRP)[1] + limL
                rp_1_value = self.abf.sweepY[rp_1_index]
                return rp_1_value, rp_1_index


    def rp_2(self):
        """Returns information about rp_2 position, between the action potential
        peak and AHP.
        
        ### Default: Automatic search for the value of rp2.
       
        Ranges:
            * If only one AP is detected in trace the searching interval is 
            from the peak index to peak + [peak:peak+50ms] .  
            * If multiple AP detected: [current_peak:min(current_peak:next_peak)].
        
        For both cases AHP (i.e. minimum voltage after peak) is detected 
        and rp_2 is searched as resting potential nearest value in interval 
        from peak to AHP.
        
        ### Second level of detection
        
        User provided interval for rp2 detection: rp_2_det = [int,int]  
        -> Searching for the closest value to the absolute resting potential 
        in the interval specified by the user.
        
        ### Third level of detection
        
        User provided fixed point for rp_2: rp_2_fixedP = int -> Fixed index 
        point for rp2.
        
        Returns
        -------
        float
            Measured value of rp2, in mV.
        int
            Index of rp2 on voltage signal.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        absRP = self.resting_potential()
        
        # If second level of detection is inactive
        if self.rp_2_det == None:
            
            # If third level of detection is inactive
            if self.rp_2_fixedP == None:
                
                # Default detection
                limL = self.current_peak()[1]
                preLimR = []
                if len(self.peaks()[1]) == 1:
                    preLimR = limL + self.sampleFactor(time_interval=50.0)
                elif len(self.peaks()[1]) > 1:
                    preLimR = self.next_peak()
                ahpDetInt = self.abf.sweepY[limL:preLimR]
                limR = otls.find_nearest(ahpDetInt, min(ahpDetInt))[1] + limL
                detectionInt = self.abf.sweepY[limL:limR]
                rp_2_index = otls.find_nearest(detectionInt, absRP)[1] + limL
                rp_2_value = round(self.abf.sweepY[rp_2_index], 2)
                return rp_2_value, rp_2_index   
            
            # If third level of detection is given (fixed point for rp_2)
            elif type(self.rp_2_fixedP) == int:
                rp_2_index = self.rp_2_fixedP
                rp_2_value = round(self.abf.sweepY[rp_2_index], 2)
                return rp_2_value, rp_2_index 
            
        # If second level of detection is given (interval for rp_2 detection)    
        elif type(self.rp_2_det) == list:
            detectionInt = self.abf.sweepY[self.rp_2_det[0]:self.rp_2_det[1]]
            rp_2_index = otls.find_nearest(detectionInt, absRP)[1] + self.rp_2_det[0]
            rp_2_value = round(self.abf.sweepY[rp_2_index], 2)
            return rp_2_value, rp_2_index    
    
    
    def rp_3(self):
        """Returns information about rp_3 position, first resting potential-like 
        after AHP.
        
        ### Default: Automatic search for the value of rp3.

        Ranges:
             * If one AP detected: [peak:peak+50ms]   
             * If multiple AP detected: [current_peak:min(current_peak:next_peak)]
        
        ### Second level of detection
 
        User provided interval for rp3 detection: rp_3_det = [int,int]  
        -> Searching for the closest value to the absolute resting potential 
        in the interval specified by the user.
        
        ### Third level of detection
      
        User provided fixed point for rp_3: rp_3_fixedP = int -> Fixed index point
        for rp3.
        
        Returns
        -------
        float
            Measured value of rp3, in mV.
        int
            Index of rp3 on voltage signal.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        absRP = self.resting_potential()
        
        # If second level of detection is inactive
        if self.rp_3_det == None:
            
            # If third level of detection is inactive
            if self.rp_3_fixedP == None:   
                     
                limL = self.rp_2()[1] + self.sampleFactor(time_interval=2)
                # If a single action potential has been detected in trace
                if len(self.peaks()[1]) == 1:    
                    val = self.sampleFactor(time_interval=30)           
                    detectionInt = self.abf.sweepY[limL:-1]
                    rp_3_index = []
                    try:
                        rp_3_index.append(otls.find_nearest(detectionInt, 
                                                            absRP)[1] + limL)   
                    except IndexError:                               
                        rp_3_index.append(-1)
                    rp_3_value = round(self.abf.sweepY[rp_3_index[0]], 2)
                    return rp_3_value, rp_3_index[0]

                # If several action potentials have been detected in trace
                elif len(self.peaks()[1]) > 1:
                    detectionInt = self.abf.sweepY[limL:self.next_peak()]
                    limR = otls.find_nearest(detectionInt, min(detectionInt))[1]
                    
                    rp_3_index = otls.find_nearest(detectionInt[limR:self.next_peak()], 
                                                   absRP)[1] + limL
                    rp_3_value = round(self.abf.sweepY[rp_3_index], 2)
                    return rp_3_value, rp_3_index
                        
            # If third level of detection is given (fixed point for rp_3)           
            elif type(self.rp_3_fixedP) == int:
                rp_3_index = self.rp_3_fixedP
                rp_3_value = round(self.abf.sweepY[rp_3_index], 2)
                return rp_3_value, rp_3_index 
            
        # If second level of detection is given (interval for rp_3 detection)    
        elif type(self.rp_3_det) == list:
            detectionInt = self.abf.sweepY[self.rp_3_det[0]:self.rp_3_det[1]]
            rp_3_index = otls.find_nearest(detectionInt, absRP)[1] + self.rp_3_det[0]
            rp_3_value = round(self.abf.sweepY[rp_3_index], 2)
            return rp_3_value, rp_3_index    

     
    # INFO PRINTING
     
    def trace_info(self, sweep_number:int):
        """Prints information about the number of action potentials, 
        their amplitude, position on time axis and the sample number.

        Parameters
        ----------
        sweep : int
            The trace sweep for which the information will be printed .
            
        Returns
        -------
        printed information: file name, sweep number, the number of 
        action potential detected, its amplitude value, moment on time and 
        index.
        """                        
        sn = sweep_number - 1                     
        self.abf.setSweep(sn, self.voltage_channel_number)
        peakValues = self.peaks()[0]
        peakIndices = self.peaks()[1]
        if len(peakIndices) == 0:
            print('No action potential detected in', self.abf_file_name,
                  'sweep no.', sweep_number, '.')
        else:
            print('Action potentials detected in', self.abf_file_name,
                  'sweep no. ', sweep_number, ':')
        for (index, value), ind in zip(enumerate(peakValues, start=1), peakIndices):    
                    print('The', index, 'AP at', round(self.abf.sweepX[ind]*1000, 1), 
                          'mS, with', round(value, 2), 'mV peak amplitude.',
                          'Sample number:', ind, '.')
                

    def __str__(self) -> str:
        """Returns information about abf file path and RP values."""
        return (f'Abf file path: {self.abf_file},\n'
                + f'RP1 detected at {self.rp_1()[1]}, measuring {self.rp_1()[0]} mV,\n'
                + f'RP2 detected at {self.rp_2()[1]}, measuring {self.rp_2()[0]} mV,\n'
                + f'RP3 detected at {self.rp_3()[1]}, measuring {self.rp_3()[0]} mV,\n'
                + f'absolute RP value: {self.resting_potential()} mV.')
    
    
    def __repr__(self) -> str:
        """Returns information about Parameters object."""
        return (f'Parameters(abf_file_name={self.abf_file_name}, '
                + f'voltage_channel_number={self.voltage_channel_number}, '
                + f'current_channel_number={self.current_channel_number}, '
                + f'sweep_number={self.sweep_number}, '
                + f'ap_number={self.ap_number} )')
    

    ### AMPLITUDE PARAMETERS ###

    def threshold(self, method): 
        """Calculate the action potential threshold by several methods and 
        returns (value, index). 
            
        * Below is described how the threshold values were obtained. For more 
        extensive explanations please consult the documentation and the 
        reference papers indicated.
            
        Parameters
        ----------
        method : str
        
        ### Method 'I'
            The threshold value is given by the index of maximum value of `g`,
            which is the maximum slope of the first voltage derivative versus 
            voltage signal. The value is obtained by dividing the values of the
            second derivative by the values of the first derivative `[ref_1]`.
        
        ### Method 'II'
            The threshold is given by the index of maximum value of h `[ref_1]`. 
            
        ### Method 'III'
            Here, threshold is considered the voltage at the index of the last
            element that is less than or equal to an ad-hoc value of 0.25 on 
            first estimated temporal derivative.
        
        ### Method 'IV'
            Threshold is identified as the voltage corresponding to the maximum
            value of the second estimated temporal derivative.
            
        ### Method 'V'
            Threshold is identified as the voltage corresponding to the maximum
            value of the third estimated temporal derivative, in interval 
            from rp1 + 1 ms up to the peak.
            
        ### Method 'VI'
            Threshold here is the minimum value of first derivative in interval
            from rp1 + 1 ms to peak.
            
        ### Method 'VII'
            The maximum value of kp (maximum point of curvature) `[ref_1]`.
            
        ### Method 'VIII'
            Here, the threshold value is considered at the point where the third
            derivative changes from negative to positive values, before the peak
            of the first derivative `[ref_2]`.
            
        ### Method 'IX'
            Threshold is considered the voltage where second derivative passes 
            the ad-hoc value of 2.5. This value was chosen because it is above
            the signal noise.
            
        ### Method 'X'
            Threshold here is the point at which the first derivative passes an
            ad-hoc value of 10. This value was chosen because it is above the 
            signal noise.
            
        Returns
        -------
        tuple[float, int]
            float
                Threshold potential value in mV.
            int
                Threshold potential index.
        
        Raises
        ------
        ValueError
            Raise when the input method is not an string input in range from
            'I' to 'X'.
        TypeError
            Raise when the input type for method is other than string type.
        
        Examples
        --------
        >>> abf1_par = ap.Parameters(abf_file='abf_file.abf', 
        >>>                          current_channel_number=0,
        >>>                          voltage_channel_number=1, 
        >>>                          ...)
        >>> 
        >>> # Choose a method from 'I' to 'X'.
        >>> abf1_thV = abf1_par.thresholds(method='V')
        >>> print(abf1_thV)
        >>> 
        >>> # printing tuple (value, index) for coresponding method
        >>> (-25.14, 582)
        
            
        References
        ----------
        `ref1` - Sekerli M, Del Negro CA, Lee RH, Butera RJ. Estimating action
        potential thresholds from neuronal time-series: new metrics and 
        evaluation of methodologies. IEEE Trans Biomed Eng. 2004 Sep;
        51(9):1665-72. doi: 10.1109/TBME.2004.827531. PMID: 15376515.
        
        `ref2` - Henze DA, González-Burgos GR, Urban NN, Lewis DA, 
        Barrionuevo G. Dopamine increases excitability of pyramidal neurons in 
        primate prefrontal cortex. J Neurophysiol. 2000 Dec;84(6):2799-809. 
        doi: 10.1152/jn.2000.84.6.2799. PMID: 11110810.
        
        NOTE: For more information see the documentation, at `link`.           
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        time = self.abf.sweepX * 1000
        voltage = self.abf.sweepY
        filteredV = tools.Filters(array=voltage, cutoff_freq=1250, 
                                  sampling_freq=self.abf.sampleRate, 
                                  order=8, type='lowpass').bessel()
       
        #Delta Time
        dt = round(((time[-1] - time[0]) / len(time)), 2)
        
        ## Difference between raw voltage and filtered
        # plt.plot(time, voltage, 'b', label='AP')
        # plt.plot(time, filteredV, 'r', label='AP filtered')
        # plt.show()
        
        limL = self.rp_1()[1] + self.sampleFactor(time_interval=1)
        limR = self.current_peak()[1]
        
        dIvolt = []
        dIIvolt = []
        dIIIvolt = []
        
        # Temporal derivative estimates 
        # Estimated with central difference techniques accurate to O (deltaTime**4)
        # Consult `ref1` for more information.
        for index in range(0, len(filteredV)-3):
            dIvolt.append((filteredV[index-2] - 8*filteredV[index-1]
                           + 8*(filteredV[index+1]) 
                           - filteredV[index+2]) / 12*dt)
            
            dIIvolt.append((-filteredV[index-2] + 16*filteredV[index-1] 
                            - 30*filteredV[index] + 16*filteredV[index+1] 
                            - filteredV[index+2]) / 12*(dt**2))
            
            dIIIvolt.append((filteredV[index-3] - 8*filteredV[index-2] 
                             + 13*filteredV[index-1] - 13*filteredV[index+1] 
                             + 8*filteredV[index+2] 
                             - filteredV[index+3]) / 8*(dt**3))
            
        ## Plots
        # plt.plot(time[:-3], dIvolt, 'blue', label='First time derivative')
        # plt.plot(time[:-3], dIIvolt, 'green', label='Second time derivative')
        # plt.plot(time[:-3], dIIIvolt, 'red', label='Third time derivative')
        # plt.show()
        
        # Derivative estimates calculated with np.diff
        dIvoltage = np.diff(filteredV) / np.diff(time) # mv*ms
        dIIvoltage = np.diff(dIvoltage) / np.diff(time[:-1]) # mv*ms**-2
        dIIIvoltage = np.diff(dIIvoltage) / np.diff(time[:-2]) # mv*ms**-3   
        
        ## Plots
        # plt.plot(time[:-1], dIvoltage, 'blue', label='First time derivative')
        # plt.plot(time[:-2], dIIvoltage, 'green', label='Second time derivative')
        # plt.plot(time[:-3], dIIIvoltage, 'red', label='Third time derivative')
        # plt.show()
        
        if type(method) != None:
            
            if type(method) == str:
                
                if method == 'I':
                    ## Phase plot (First derivative vs voltage)
                    # plt.plot(voltage[:-3], dIvolt, 'blue')
                    # plt.show()
                    g = []
                    for d1, d2 in zip(dIvolt[limL:limR], dIIvolt[limL:limR]):
                            g.append(d2/d1) 
                    thI_index = otls.find_nearest(g, max(g))[1] + limL
                    thI_value = round(self.abf.sweepY[thI_index], 2)
                    return thI_value, thI_index 
                
                elif method == 'II':
                    h = []
                    for d1, d2, d3 in zip(dIvolt[limL:limR], dIIvolt[limL:limR],
                                          dIIIvolt[limL:limR]):
                        h.append((d3*d1 - (d2**2)) / d1**3)
                        
                    ## Plot h values versus voltages
                    # plt.plot(voltage[limL:limR], h, 'green')
                    # plt.show()
                    
                    thII_index = otls.find_nearest(h, max(h))[1] + limL
                    thII_value = round(self.abf.sweepY[thII_index], 2)
                    return thII_value, thII_index
                
                elif method == 'III':
                    # plt.plot(dIvolt, 'blue')
                    # plt.show()
                    adhocPC = [i <= .05 for i in dIvolt[limL:limR]]
                    thIII_index = otls.find_nearest(dIvolt[limL:limR], 
                                                    adhocPC[-1])[1] + limL
                    thIII_value = round(self.abf.sweepY[thIII_index], 2)
                    return thIII_value, thIII_index
                
                elif method == 'IV':
                    # plt.plot(dIIvolt)
                    # plt.show()
                    thIV_index = otls.find_nearest(dIIvolt[limL:limR],
                                                   max(dIIvolt[limL:limR]))[1] + limL
                    thIV_value = round(self.abf.sweepY[thIV_index], 2)
                    return thIV_value, thIV_index
                
                elif method == 'V':
                    # plt.plot(time[limL:limR], dIIIvolt[limL:limR])
                    # plt.show()
                    thV_index = otls.find_nearest(dIIIvolt[limL:limR], 
                                                  max(dIIIvolt[limL:limR]))[1] + limL
                    thV_value = round(self.abf.sweepY[thV_index], 2)
                    return thV_value, thV_index
                
                elif method == 'VI':
                    dvdt = dIvoltage[limL:limR]
                    thVI_index = otls.find_nearest(dvdt, min(dvdt))[1] + limL
                    thVI_value = round(self.abf.sweepY[thVI_index], 2)
                    return thVI_value, thVI_index
                
                elif method == 'VII':
                    kp = []
                    for d1, d2 in zip(dIvolt[limL:limR], dIIvolt[limL:limR]):
                        kp.append(d2*((1 + d1**2)**(-3/2)))
                    # plt.plot(kp)
                    # plt.show()
                    thVII_index = otls.find_nearest(kp, max(kp))[1] + limL
                    thVII_value = round(self.abf.sweepY[thVII_index], 2)
                    return thVII_value, thVII_index
                
                elif method == 'VIII':
                    localL = self.rp_1()[1] + self.sampleFactor(time_interval=.5)
                    localR = self.rp_2()[1] - self.sampleFactor(time_interval=.5)
    
                    # Right limit
                    dIIIminVal = otls.find_nearest(dIIIvoltage[localL:localR], 
                                                   min(dIIIvoltage[localL:localR]))[1] + localL
                    # Left limit
                    dIIImaxVal = otls.find_nearest(dIIIvoltage[localL:dIIIminVal], 
                                                   max(dIIIvoltage[localL:dIIIminVal]))[1] + localL
                    # Crossing X axis
                    crossXinterval = [abs(i) for i in dIIIvoltage[dIIImaxVal:dIIIminVal]]
                    thVIII_index = otls.find_nearest(crossXinterval, 
                                                     min(crossXinterval))[1] + dIIImaxVal
                    thVIII_value = round(self.abf.sweepY[thVIII_index], 2)

                    return thVIII_value, thVIII_index
                
                elif method == 'IX':
                    localL = self.rp_1()[1] + self.sampleFactor(time_interval=1)
                    localR = self.rp_2()[1] - self.sampleFactor(time_interval=1)
                    adhocPC = []
                    for index, value in enumerate(dIIvoltage[localL:localR]):   
                        if value >= 2.5:
                            adhocPC.append(index)
                    thIX_index = adhocPC[0] + localL
                    thIX_value = round(self.abf.sweepY[thIX_index], 2)
                    return thIX_value, thIX_index
                
                elif method == 'X':
                    localL = self.rp_1()[1] + self.sampleFactor(time_interval=1.5)
                    localR = self.rp_2()[1] - self.sampleFactor(time_interval=1)
                    # plt.plot(dIvoltage[localL:localR], 'blue')
                    # plt.show()
                    adhocPC = []
                    for index, value in enumerate(dIvoltage[localL:localR]):   
                        if value >= 10:
                            adhocPC.append(index)
                    thX_index = adhocPC[0] + localL
                    thX_value = round(self.abf.sweepY[thX_index], 2)
                    # Plot original trace filtered and first derivative
                    # plt.plot(time[localL:localR], filteredV[localL:localR])
                    # plt.plot(time[localL:localR], dIvoltage[localL:localR])
                    # plt.show()
                    return thX_value, thX_index
                
                else:
                    raise ValueError("Pick method from 'I' to 'X'.")
            else:
                raise TypeError("Method has to be string type.")
        else:
            print("Select a threshold method from 'I' to 'X'.")

   
    def overshoot(self):
        """Returns the positive voltage value at the AP peak (mV).

        Returns
        -------
        float
            AP peak voltage value in mV.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        ap_overshoot = self.abf.sweepY[self.current_peak()[1]]
        return round(ap_overshoot, 2)
    
    
    def afterhyperpolarization(self):
        """Returns the minimum voltage value detected in interval from rp2 
        to rp3, i.e. AHP detected value as the minimum voltage after falling
        phase.
        
        ### NOTE
        This method does not eliminate the problem of depolarizing 
        afetr-potential (DAP) that occurs due to the stimulus duration 
        in some neurons. In this case, if DAP peak value rise above 
        resting potential value it will be detected as RP3 or if the 
        anti-peak falls below AHP it will be considered AHP.

        Returns
        -------
        tuple
            float
                Minimum voltage point value in interval from rp2 to rp3, in mV.
            int
                Minimum voltage point index in interval from rp2 to rp3, in mV.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        ahp_int = self.abf.sweepY[self.rp_2()[1]:self.rp_3()[1]]        
        ahp_index = otls.find_nearest(ahp_int, min(ahp_int))[1] + self.rp_2()[1]
        ahp_value = round(self.abf.sweepY[ahp_index], 2)
        return ahp_value, ahp_index
    
    
    def afterhyperpolarization_at(self, percentage):
        """Returns the point where the ahp amplitude was recovered to 
        resting potential value, at a certain percentage.

        Parameters
        ----------
        percentage : int
            The procentage of ahp amplitude recovery.

        Returns
        -------
        float
            Voltage value at some procentage of recovery.
        int
            Index point for value.
        """ 
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        ahp_value = self.afterhyperpolarization()[0]
        
        limL = self.afterhyperpolarization()[1]
        limR = self.rp_3()[1]
        
        refValue = self.resting_potential()
        interval = self.abf.sweepY[limL:limR]
        ahp_amplitude = ahp_value - refValue
        procentageRec = (ahp_amplitude * percentage)/100
        ahpAmp_at_procentRec = ahp_value + abs(procentageRec)
        index = otls.find_nearest(array=interval, 
                                  value=ahpAmp_at_procentRec)[1]
        
        ahpIndex = index + limL
        ahpValue = round(self.abf.sweepY[ahpIndex], 2)    
        return ahpValue, ahpIndex
    
    
    def ahp_substracted_value(self):
        """The AHP value baselined at resting potential.

        Returns
        -------
        float
            AHP value from which resting potential value was substracted.
        """
        ahp = self.afterhyperpolarization()[0]
        rp = self.resting_potential()
        return round(abs(ahp - rp), 2)
    
    
    def total_amplitude(self):
        """Returns AP total amplitude or AP size by adding absolute resting
        potential value to the overshoot value (peak value).

        Returns
        -------
        float
            Total amplitude value, in mV.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        totalAmp = abs(self.rp_1()[0]) + self.overshoot()
        return round(totalAmp, 2)


    ### DURATION PARAMETERS ###

    def ahp_recovery_time_at(self, percentage):
        """Returns duration from AHP point to AHP value recovered 
        at a given percentage.

        Parameters
        ----------
        percentage : int
            AHP amplitude recovery percentage.

        Returns
        -------
        float
            Duration from AHP to AHP value recovered at a given percentage,
            in ms.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        ahpTime = self.abf.sweepX[self.afterhyperpolarization()[1]]
        ahpIndex_at = self.afterhyperpolarization_at(percentage=percentage)[1]
        ahpRec_time_at = self.abf.sweepX[ahpIndex_at]
        recTime = (ahpRec_time_at - ahpTime) * 1000 # ms
        return round(recTime, 2)
    
    
    def ahp_time_constant(self):
        """Isolates voltage signal from AHP to AHP80 and fit with 
        mono_exponential to find the ahp time constant.

        Returns
        -------
        float
            Decay time constant value in ms resulting from mono_exponential 
            fit parameteres.
        """
        # Limits
        fitlimL = self.afterhyperpolarization()[1]
        fitlimR = self.afterhyperpolarization_at(percentage=80)[1]
        
        endtime = int(self.ahp_recovery_time_at(percentage=80))
        # Filter the trace
        voltage = self.abf.sweepY[fitlimL:fitlimR]
        
        time = np.linspace(0, endtime, num=len(voltage))
        t = self.abf.sweepX[fitlimL:fitlimR]
        voltage_filtered = tools.Filters(array=voltage, cutoff_freq=1000, 
                                         sampling_freq=self.abf.sampleRate, 
                                         order=8, type='lowpass').bessel()
        # Fit with mono-exponential
        voltage_fit = tools.Fitting.mono_exponential(xdata=time, 
                                                     ydata=voltage_filtered)
        ahp_time_constat = round(voltage_fit[1][2], 2)
        return ahp_time_constat
    
    
    def duration_at(self, level):
        """Returns durations for different parameters of AP.

        Parameters
        ----------
        level : str
            Represents the level at which the measurement is made and can be:
            base, overshoot, half amplitude or 1/3 amplitude.

        Returns
        -------
        float
            Duration in ms for specified parameter.
        int
            Index of left point of measured parameter.
        int
            Index of right point of measured parameter.

        Raises
        ------
        ValueError
            Raise when the input for level is other than 'base', 'overshoot', 
            'halfAmp' or 'oneThirdAmp'.
        TypeError
            Raise when the input type for level is other than string type.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        limL = self.rp_1()[1]
        limM = self.current_peak()[1]
        limR = self.rp_2()[1]
        
        leftInt = self.abf.sweepY[limL:limM]
        rightInt = self.abf.sweepY[limM:limR]
        
        duration = []
        leftIndex = []
        rightIndex = []
        
        if type(level) == str:
            if level == 'base':
                leftIndex.append(limL)
                rightIndex.append(limR)
                duration.append(self.time_subtraction(a=limR, b=limL))
            elif level == 'overshoot':
                leftIndex.append(otls.find_nearest(leftInt, 0)[1] + limL)
                rightIndex.append(otls.find_nearest(rightInt, 0)[1] + limM)
                duration.append(self.time_subtraction(a=rightIndex, b=leftIndex))          
            elif level == 'halfAmp':
                halfAmp = self.rp_1()[0] + self.total_amplitude() / 2
                leftIndex.append(otls.find_nearest(leftInt, halfAmp)[1] + limL)
                rightIndex.append(otls.find_nearest(rightInt, halfAmp)[1] + limM)
                duration.append(self.time_subtraction(a=rightIndex, b=leftIndex))
            elif level == 'oneThirdAmp':
                oneThirdAmp = self.rp_1()[0] + self.total_amplitude() / 3
                leftIndex.append(otls.find_nearest(leftInt, oneThirdAmp)[1] + limL)
                rightIndex.append(otls.find_nearest(rightInt, oneThirdAmp)[1] + limM)
                duration.append(self.time_subtraction(a=rightIndex, b=leftIndex))
            else:
                raise ValueError("Invalid level. Specify between: 'base', "
                                 "'overshoot', 'halfAmp' or 'oneThirdAmp'.")
        else:
            raise TypeError("Level: string type.")
       
        return duration[0], leftIndex[0], rightIndex[0]
            

    def phase_time(self, region):
        """Returns durations for ascending (rising), descending (falling)
        phases and AHP.

        Parameters
        ----------
        region : str
            Region to perform time measurement.

        Returns
        -------
        float
            Phase time duration in ms.

        Raises
        ------
        ValueError
            Raise when the input for region is other than 'rising', 
            'falling', or 'ahp'.
        TypeError
            Raise when the input type for region is other than string type.
        """
        duration = []
        if type(region) == str:
            if region == 'rising':
                duration.append(self.time_subtraction(a=self.current_peak()[1], 
                                                      b=self.rp_1()[1]))
            elif region == 'falling':
                duration.append(self.time_subtraction(a=self.rp_2()[1], 
                                                      b=self.current_peak()[1]))
            elif region == 'ahp':
                duration.append(self.time_subtraction(a=self.rp_3()[1], 
                                                      b=self.afterhyperpolarization()[1]))
            else:
                raise ValueError("Invalid region phase."
                                 " Specify between: 'rising', 'falling' or 'ahp'.")
        else:
            TypeError("Region: string type.")

        phaseDuration = round(duration[0], 2)
        return phaseDuration
    

    ### RATE PARAMETERS ###

    def amplitude_over_time(self, region):
        """Returns the voltage change over time, for rising & falling phases,
        ahp 80% recovery and total recovery.

        Parameters
        ----------
        region : str
             Region to perform the amplitude over time measurement: 'rising',
             'falling', 'ahp80', 'ahp_full'.

        Returns
        -------
        float
            Voltage change in specified phase over time of phase (mV/ms).

        Raises
        ------
        ValueError
            Raise when the input for region is other than 'rising', 
            'falling', 'ahp80' or 'ahp_full'.
        TypeError
            Raise when the input type for region is other than string type.
        """
        dividend = [] # amplitude
        divisor = [] # time
        
        if type(region) == str:
            
            if region == 'rising':
                dividend.append(self.total_amplitude())
                divisor.append(self.phase_time(region='rising'))
            elif region == 'falling':
                dividend.append(self.total_amplitude())
                divisor.append(self.phase_time(region='falling'))
            elif region == 'ahp_full':
                ahpAmp = self.ahp_substracted_value()
                dividend.append(ahpAmp)
                divisor.append(self.phase_time(region='ahp'))
            elif region == 'ahp80':
                ahpAmp = self.ahp_substracted_value()
                dividend.append(ahpAmp)
                divisor.append(self.ahp_recovery_time_at(percentage=80))
            else:
                raise ValueError("Invalid region! Specify between: 'rising', "
                                 + "'falling', 'ahp80' or 'ahp_full'.")
        else:
            raise TypeError("Region was to be string type.") 
        rate = dividend[0] / divisor[0]
        return round(rate, 2)

    
    ### AREA ###

    def area(self, region):
        """Returns the area of the selected region.

        Parameters
        ----------
        region : str
            AP region where to calculate area.

        Returns
        -------
        float
            Area value in mV*ms.

        Raises
        ------
        ValueError
            Raise when the input for region is other than 'base', 'overshoot', 
            'rise', 'fall', 'upper-rise', 'upper-fall', 'lower-rise', 'lower-fall'.
        TypeError
            Raise when the input type for region is other than string type.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)       
        limL = []
        limR = []
        if type(region) == str:
            
            if region == 'base':
                limL.append(self.rp_1()[1])
                limR.append(self.rp_2()[1])
            elif region == 'overshoot':
                limL.append(self.duration_at(level='overshoot')[1])
                limR.append(self.duration_at(level='overshoot')[2])
            elif region == 'ahp':
                limL.append(self.rp_2()[1])
                limR.append(self.rp_3()[1])
            elif region == 'rise':
                limL.append(self.rp_1()[1])
                limR.append(self.current_peak()[1])
            elif region == 'fall':
                limL.append(self.current_peak()[1])
                limR.append(self.rp_2()[1])
            elif region == 'upper-rise':
                limL.append(self.duration_at(level='overshoot')[1])
                limR.append(self.current_peak()[1])
            elif region == 'upper-fall':
                limL.append(self.current_peak()[1])
                limR.append(self.duration_at(level='overshoot')[2])
            elif region == 'lower-rise':    
                limL.append(self.rp_1()[1])
                limR.append(self.duration_at(level='overshoot')[1])
            elif region == 'lower-fall':  
                limL.append(self.duration_at(level='overshoot')[2])
                limR.append(self.rp_2()[1])                   
            else:                
                raise ValueError("Invalid region. Select from: 'base', ",
                                 "'overshoot', 'rise', 'fall', 'upper-rise', ",
                                 "'upper-fall', 'lower-rise', 'lower-fall'.")                       
        else:            
            raise TypeError("'region': must be string type.")

        x = self.abf.sweepX[limL[0]:limR[0]] *1000 # ms        
        y = self.abf.sweepY[limL[0]:limR[0]]        
        dx = round(((x[-1] - x[0]) / len(x)), 2)
        
        # Make absolute resting potential value the baseline
        yI = []
        absRP = self.resting_potential()
        for value in y:
            yI.append(value - absRP) 
        area = round(sum(yI) * dx, 2)  # mV*ms
        return area
      
        
    ### SLOPES ###
  
    def maximal_slope(self, phase):
        """Returns the maximal slopes of rising and falling phases.

        Parameters
        ----------
        phase : str
            Region to perform slope calculation and maximal slope detection.

        Returns
        -------
        float
            Voltage value corresponding to maximal slope.
        int
            Index point of maximum slope on voltage.

        Raises
        ------
        ValueError
            Raise when the input for phae is other than 'rise' or 'decay'.
        TypeError
            Raise when the input type for phase is other than string type.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        limL = [] 
        limR = [] 
        if type(phase) == str:
            
            if phase == 'rise':
                limL.append(self.rp_1()[1])
                limR.append(self.current_peak()[1])
                
            elif phase == 'decay':
                limL.append(self.current_peak()[1] 
                            + self.sampleFactor(time_interval=.35))
                limR.append(self.rp_2()[1] 
                            - self.sampleFactor(time_interval=.35))
                
            elif phase not in ['rise', 'decay']:
                raise ValueError("'Phase' has to be 'rise' or 'decay'.")
            
        else:
            raise TypeError("'Phase' has to be string type.")
                
        voltInt = self.abf.sweepY[limL[0]:limR[0]]        
        timeInt = self.abf.sweepX[limL[0]:limR[0]] * 1000 # ms 

        deltaVs = np.diff(voltInt)       
        deltaTs = np.diff(timeInt)  

        derI = []
        for v, t in zip(deltaVs, deltaTs): derI.append(v / t)

        dImax = otls.find_nearest(array=derI, value=max(derI))[1]
        maxSlope_index = dImax + limL
        voltage_value = self.abf.sweepY[maxSlope_index]

        return voltage_value[0], maxSlope_index[0]
    

    ### DATA HANDLING ###
  
    def data_loader(self):
        """Returns lists with all parameteres and their titles.

        Returns
        -------
        list
            Column title information.
        list
            Row values.
        """
        # Set 1 - Amplitude parameters
        ampParams = [['Resting potential value (mV)', 
                      round(self.resting_potential(), 2)],                 
                     ['Threshold Method I (mV)', 
                      self.threshold(method='I')[0]],
                     ['Threshold Method II (mV)',
                      self.threshold(method='II')[0]], 
                     ['Threshold Method III (mV)',
                      self.threshold(method='III')[0]], 
                     ['Threshold Method IV (mV)',
                      self.threshold(method='IV')[0]], 
                     ['Threshold Method V (mV)',
                      self.threshold(method='V')[0]],
                     ['Threshold Method VI (mV)'
                      , self.threshold(method='VI')[0]],
                     ['Threshold Method VII (mV)'
                      , self.threshold(method='VII')[0]],
                     ['Threshold Method VIII (mV)'
                      , self.threshold(method='VIII')[0]],  
                     ['Threshold Method IX (mV)',
                      self.threshold(method='IX')[0]],
                     ['Threshold Method X (mV)',
                      self.threshold(method='X')[0]],                                
                     ['Overshoot (mV)',
                      round(self.overshoot(), 2)],                     
                     ['Total amplitude (mV)',
                      self.total_amplitude()],                   
                     ['Afterhyperpolarization (mV)',
                      self.afterhyperpolarization()[0]],  
                     ['AHP substracted value',
                      self.ahp_substracted_value()],     
                     ['AHP 25% recovered value (mV)', 
                      self.afterhyperpolarization_at(percentage=25)[0]],                    
                     ['AHP 50% recovered value (mV)', 
                      self.afterhyperpolarization_at(percentage=50)[0]],
                     ['AHP 80% recovered value (mV)', 
                      self.afterhyperpolarization_at(percentage=80)[0]]]
        
        # Set 2 - Duration parameters
        durParams = [['Duration at the base (ms)', 
                      round(self.duration_at(level='base')[0], 2)],
                     ['Duration at overshoot (ms)', 
                      round(self.duration_at(level='overshoot')[0][0], 2)],                    
                     ['Duration at half AP amplitude (ms)', 
                      round(self.duration_at(level='halfAmp')[0][0], 2)],                    
                     ['Duration at 1/3 AP amplitude (ms)', 
                      round(self.duration_at(level='oneThirdAmp')[0][0], 2)],                    
                     ['Rising time (ms)', 
                      self.phase_time(region='rising')],                     
                     ['Falling time (ms)', 
                      self.phase_time(region='falling')],                     
                     ['AHP time (ms)', 
                      self.phase_time(region='ahp')],                     
                     ['Time from AHP to 25 % of its value recovered (ms)', 
                      self.ahp_recovery_time_at(percentage=25)],
                     ['Time from AHP to 50 % of its value recovered (ms)', 
                      self.ahp_recovery_time_at(percentage=50)],
                     ['Time from AHP to 80 % of its value recovered (ms)', 
                      self.ahp_recovery_time_at(percentage=80)]]
                     
        # Set 3 - Rates
        rateParams = [['Rising phase amplitude over time (mV/ms)', 
                       self.amplitude_over_time(region='rising')],
                      ['Falling phase amplitude over time (mV/ms)', 
                       self.amplitude_over_time(region='falling')],
                      ['AHP full recovery phase amplitude over time (mV/ms)', 
                       self.amplitude_over_time(region='ahp_full')],
                      ['AHP 80 recovery amplitude over time (mV/ms)', 
                       self.amplitude_over_time(region='ahp80')]]
  
        # Set 4 - Areas
        areaParams = [['Area at AP base (mV*ms)', 
                       self.area(region='base')],
                      ['Area at AHP (mV*ms)', 
                       self.area(region='ahp')],
                      ['Area at AP overshoot (mV*ms)', 
                       self.area(region='overshoot')],
                      ['Area at AP rising phase (mV*ms)', 
                       self.area(region='rise')],
                      ['Area at AP falling phase (mV*ms)', 
                       self.area(region='fall')],
                      ['Area at upper-rise (mV*ms)', 
                       self.area(region='upper-rise')],
                      ['Area at upper-fall (mV*ms)', 
                       self.area(region='upper-fall')],
                      ['Area at lower-rise (mV*ms)', 
                       self.area(region='lower-rise')],
                      ['Area at lower-fall (mV*ms)', 
                       self.area(region='lower-fall')]]
        
        # Set 5 - Slopes
        slopesParams = [['Maximal rising phase slope point (mV)', 
                         self.maximal_slope(phase='rise')[0]],
                        ['Maximal falling phase slope point (mV)', 
                         self.maximal_slope(phase='decay')[0],]]
          
        allParams = ampParams+durParams+rateParams+areaParams+slopesParams
        
        column_list = ['File name']
        for n in range(0, len(allParams)):
            column_list.append(allParams[n][0])
            
        rowData = [self.abf_file_name]
        for index, value in enumerate(allParams):
            rowData.append(allParams[index][1])

        return rowData, column_list



class Plotting(Parameters):

    def __init__(self, abf_file, 
                 voltage_channel_number, 
                 current_channel_number, 
                 
                 absolute_rp_interval=None,
                 sweep_number=None, 
                 ap_number=0, 
                 peak_detection_threshold=None, 
                 
                 rp_1_det=None, 
                 rp_2_det=None, 
                 rp_3_det=None,
                 
                 rp_1_fixedP=None, 
                 rp_2_fixedP=None, 
                 rp_3_fixedP=None):
        """Use abf file voltage signal and action potential parameters
        to generate figures and plots. Plotting class inherits all the 
        methods and properties from Parameters class.
        
        Parameters
        ==========
        
        #### abf_file : str
            Abf file name or path.
            
        #### voltage_channel_number : int
            Channel of voltage signal (numbering 0, n-1).
            
        #### current_channel_number : int
            Channel of current signal (numbering 0, n-1).
            
        #### sweep_number : int, optional
            Sweep to analyze (numbering 0, n-1), by default last sweep is 
            analyzed.
            
        #### absolute_rp_interval : list[int], optional
            A list of 2 integers that represent the index boundaries of the 
            analysis region for absolute resting potential value. The default 
            interval is the first 100 values.
            
        #### ap_number : int, optional
            Which of the detected action potentials will be analyzed,
            by default 0 (first one).
            
        #### peak_detection_threshold : int, optional
            Voltage threshold for peak detection, by default None.
            
            
        ## RP points - second level of detection
    
        #### rp_1_det : list[int], optional
            List of 2 integers representing interval edges for rp1
            point detection, by default None.
            
        #### rp_2_det : list[int], optional
            List of 2 integers representing interval edges for rp2
            point detection, by default None.
            
        #### rp_3_det : list[int], optional
            List of 2 integers representing interval edges for rp3
            point detection, by default None.
            
            
        ## RP points - third level of detection
        
        #### rp_1_fixedP : int, optional
            Fixed point for rp1 point, by default None.
            
        #### rp_2_fixedP : int, optional
            Fixed point for rp2 point, by default None.
            
        #### rp_3_fixedP : int, optional
            Fixed point for rp3 point, by default None.
        
        
        Methods & Layout
        ================
        
        #### raw_recording(action, extension, current_sweep_only):
            Generates a plot (or save, or plot & save) with the raw
            content of the abf file, with the current channel (waveform)
            and the voltage channel data plotted in 2 different subplots.
        
        #### graph_3D(action, extension, text_box, rotation):
            Generates a 3D plot (or save, or plot & save) with the raw content 
            of the abf file, only the voltage channel data for all sweeps in 
            recording.
            
        #### gifs(action):
            Returns a gif animation with the action potential analyzed. 
            
        #### gif_3D():
            Returns sweeps plotted one by one in a 3D rotating graph.
            
        #### ap_plot(action, extension):
            Returns a figure with signal from abf file recording, reprezenting 
            the action potential analyzed with some parameters highlighted 
            with specific markers.
        """
      

        super().__init__(abf_file, 
                         voltage_channel_number, 
                         current_channel_number, 
                         
                         absolute_rp_interval, 
                         sweep_number, 
                         ap_number, 
                         peak_detection_threshold, 
                         
                         rp_1_det, 
                         rp_2_det,
                         rp_3_det, 
                         
                         rp_1_fixedP, 
                         rp_2_fixedP, 
                         rp_3_fixedP)

      
           
    def raw_recording(self, action, extension='.png', 
                      current_sweep_only=False):
        """Generates a plot (or save, or plot & save) with the raw content of
        the abf file, with the current channel (waveform) and the voltage 
        channel data plotted in 2 different subplots.

        Parameters
        ----------
        action : str
            User input describing the action to be performed by the method: 
            'plot', 'save' (which means saving the figure) and 'plot%save'.
        extension : str, optional
            Figure extension, as .extension (ex. '.tif', '.png'), 
            by default '.png'.

        Returns
        -------
        2D Axes plot

        Raises
        ------
        ValueError
            If input action is other than 'plot', 'save' or 'save&plot'.
        TypeError
             If input action is not str type.
        """
        fig = plt.figure(figsize=(14, 10), dpi=120)
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        timeMS = self.abf.sweepX * 1000
        
        if current_sweep_only == False:
            for sweepNumber in self.abf.sweepList:
                self.abf.setSweep(sweepNumber, self.current_channel_number)
                if sweepNumber != self.sweep_number:
                    ax1.plot(timeMS, self.abf.sweepY, color='black')
                else:
                    ax1.plot(timeMS, self.abf.sweepY, color='red')
                
            for sweepNumber in self.abf.sweepList:
                self.abf.setSweep(sweepNumber, self.voltage_channel_number)
                if sweepNumber != self.sweep_number:     
                    ax2.plot(timeMS, self.abf.sweepY, color='black')
                else:
                    ax2.plot(timeMS, self.abf.sweepY, color='red')

        elif current_sweep_only == True:
            self.abf.setSweep(self.sweep_number, self.current_channel_number)
            ax1.plot(timeMS, self.abf.sweepY, color='red')
            self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
            ax2.plot(timeMS, self.abf.sweepY, color='red')

        textbox = (f'Sweep selected: {self.sweep_number+1} of '
                   + f'{len(self.abf.sweepList)}. \n'
                   + f'{len(self.peaks()[1])} AP(s) detected in sweep '
                   + f'{self.sweep_number+1}.')
        
        props = dict(boxstyle='round', facecolor='#53868B', alpha=0.3)
        ax2.text(0.74, 0.85, textbox, transform=ax2.transAxes, fontsize=13,
        verticalalignment='top', bbox=props)
            
        ax1.set_title(self.abf_file_name, fontweight='bold', fontsize='large')      
        ax1.set_ylabel("Imemb (pA)", fontweight='bold', fontsize='large')   
        ax2.set_ylabel("VCOM (mV)", fontweight='bold', fontsize='large')
        ax2.set_xlabel("Time (ms)", fontweight='bold', fontsize='large')
        
        if type(action) == str:
            if action == 'plot':
                return plt.show() 
            elif action == 'save':
                return plt.savefig(self.abf_file + extension)
            elif action == 'save&plot':
                return plt.savefig(self.abf_file + extension), plt.show()

            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")
                
    
    def graph_3D(self, action, extension=None, text_box=False, rotation=False):
        """Generates a 3D plot (or save, or plot & save) with the raw content
        of the abf file, only the voltage channel data for all sweeps in 
        recording.

        Parameters
        ----------
        action : str
            User input describing the action to be performed by the method: 
            'plot', 'save' (which means saving the figure) and 'plot%save'. 
            If action contains 'save', the function also needs the extension 
            parameter.
        extension : str, optional
            Figure extension, as .extension (ex. '.tif', '.png'), 
            by default None.
        text_box : bool
            If True, plots a textbox on Z axis, going in X axis direction, 
            by default False.
        rotation : bool
            If True the graph rotate 360 degrees before freezing.
            
        Returns
        -------
        3D plot Axes

        Raises
        ------
        TypeError
            If action is 'save' or 'save&plot' but extension was not specified.
        TypeError
            If action is 'save' or 'save&plot' but extension was not specified.
        ValueError
            If input action is other than 'plot', 'save' or 'save&plot'.
        TypeError
             If input action is not str type.
        """       
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        zs = [round(i, 1) for i in range(1, len(self.abf.sweepList)+1)]
        timeMS = self.abf.sweepX * 1000
        
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, self.voltage_channel_number)
            if sweepNumber != self.sweep_number:
                ax.plot(timeMS, self.abf.sweepY, zs[sweepNumber], zdir='y', 
                        color='black')
            else:
                ax.plot(timeMS, self.abf.sweepY, zs[sweepNumber], zdir='y', 
                        color='red')

        if text_box is True:
            label = (f'Sweep: {self.sweep_number+1} of '
                     + f'{len(self.abf.sweepList)}. \n'
                     + f'{len(self.peaks()[1])} AP(s) detected in sw. '
                     + f'{self.sweep_number+1}.')
            
            props = dict(boxstyle='round', facecolor='#53868B', alpha=0.3)
            ax.text(250, 5, 10, label, 'x',  fontsize=10, bbox=props)
        else:
            pass
        
        ax.text2D(0.05, 0.95, self.abf_file_name,  transform=ax.transAxes)
        ax.set_xlabel('Time (ms)', fontweight='bold', fontsize='medium')
        ax.set_ylabel('Sweeps (no.)', fontweight='bold', fontsize='medium')
        ax.set_zlabel('Voltage (mV)', fontweight='bold', fontsize='medium')

        if type(action) == str:
            if action == 'plot':
                if rotation == True:
                    for angle in range(0, 360):
                        ax.view_init(25, angle)
                        plt.draw()
                        plt.pause(.001)
                else:
                    return plt.show()
            elif action == 'save':
                if type(extension) == str:
                    return plt.savefig(self.abf_file + extension)
                else:
                    raise TypeError("Specify figure extension.")
            elif action == 'save&plot':
                if type(extension) == str:
                    return plt.savefig(self.abf_file + extension), plt.show()
                else:
                    raise TypeError("Specify figure extension.")
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")        

    
    def gifs(self, action):
        """Returns a gif animation with current action potential analyzed.

        Parameters
        ----------
        action : str
            User input describing the action to be performed by the method: 
            'plot', 'save' (which means saving the figure) and 'plot%save'.

        Returns
        -------
        matplotlib animation

        Raises
        ------
        ValueError
            If input action is other than 'plot', 'save' or 'save&plot'.
        TypeError
             If input action is not str type.
        """
        
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        x=self.abf.sweepX * 1000
        y=self.abf.sweepY
        xred, yred = tools.OtherTools.data_reduction(xdata=x, ydata=y, 
                                                     method='max', 
                                                     reduction_factor=10)
        
        
        fig, ax = plt.subplots(figsize=(16, 6))
        line1, = ax.plot(xred, yred, color="black")
        
        def update(num, x, y, line1):
            line1.set_data(x[:num], y[:num])
            return [line1]

        ani = animation.FuncAnimation(fig, update, len(xred), 
                                      fargs=[xred, yred, line1],
                                      interval=1, blit=True)
        
        ax.set_ylabel("Voltage (mV)", fontweight='bold', fontsize='large')
        ax.set_xlabel("Time (ms)", fontweight='bold', fontsize='large')
        
        if type(action) == str:
            if action == 'plot':
                return plt.show() 
            elif action == 'save':
                return ani.save(self.abf_file + '.gif')
            elif action == 'save&plot':
                return ani.save(self.abf_file + '.gif')
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")
        
    
    def gif_3D(self):
        """Returns sweeps plotted one by one in a 3D rotating graph."""
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        zs = [int(i) for i in range(1, len(self.abf.sweepList)+1)]
        camera = Camera(fig)
        
        # for angle in range(0, 360):
            # ax.view_init(22, angle)
            # plt.draw()
            # plt.pause(.001)
  
        ax.set_title(self.abf_file_name)
        ax.set_xlabel('Time (ms)', fontweight='bold', fontsize='medium')
        ax.set_ylabel('Sweeps (no.)', fontweight='bold', fontsize='medium')
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel('Voltage (mV)', fontweight='bold', fontsize='medium', 
                      rotation=90)
        
        for sn in self.abf.sweepList:
            self.abf.setSweep(sn, self.voltage_channel_number)
            x=self.abf.sweepX * 1000
            y=self.abf.sweepY
            xred, yred = otls.data_reduction(xdata=x, ydata=y, 
                                             method='decimate', 
                                             reduction_factor=8)
            
            t = plt.plot(xred, yred, zs[sn], zdir='y', color='black')
            plt.legend(t, [f'Sweep {sn + 1}'], loc='best', facecolor=None, 
                       edgecolor=None, fontsize=8, fancybox=None )
            camera.snap()
            plt.plot(xred, yred, zs[sn], zdir='y', color='black')
            animation = camera.animate(interval=1250, repeat=True, 
                                       repeat_delay=5)

        camera.snap()
        animation.save(self.abf_file_name +'.gif')
        

    def thresholds(self, action, extension='.png'):
        """Returns a plot figure with signal from abf file recording, 
        reprezenting the voltage trace with all threshold values highlighted
        with specific markers.
        
        Parameters
        ----------
        action : str
            The action performed to the plot: 'plot', 'save' (save the figure),
            and 'plot%save'. 
         extension : str, optional
            Figure extension, as .extension (ex. '.tif', '.png'), 
            by default '.png'.

        Returns
        -------
        plt.Axes
            Plot the active sweep with current action potential analyzed.
            
        Raises
        ------
        ValueError
            Raise if the action parameter is other than 'plot', 'save' or 
            'save&plot.'
        TypeError
            Raise if action parameter is not string type.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        time = self.abf.sweepX * 1000
        voltage = self.abf.sweepY
 
        plt.subplots(figsize=(10,8), dpi=150)
        plt.subplots_adjust(bottom=0.25)
        
        markerdictII = {
            "item": [self.threshold(method='I')[1], 
                     self.threshold(method='II')[1], 
                     self.threshold(method='III')[1], 
                     self.threshold(method='IV')[1], 
                     self.threshold(method='V')[1], 
                     self.threshold(method='VI')[1],
                     self.threshold(method='VII')[1], 
                     self.threshold(method='VIII')[1], 
                     self.threshold(method='IX')[1], 
                     self.threshold(method='X')[1]],
            
            "labels":['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 
                      'X'],
            
            "mfc": ['#C0FF3E', '#D15FEE', '#000080', '#FF83FA', '#BBFFFF', 
                    '#9B30FF', '#33A1C9', '#388E8E', '#EE3A8C', '#FFFF00'],
            
            "mec": ('#CD3700',) * 10,
            "mkshape": ['>', 'D', 's', 8, 11, 'H', 'd', 'x', 'p', 6] }
        
        # Plot the first line
        plt.plot(time, voltage, color='#515151', linewidth=3.5, alpha=1)
        
        # Plot threshold markers
        for ms, marker, mf, me in zip(markerdictII["mkshape"], 
                                      markerdictII["item"], 
                                      markerdictII["mfc"], 
                                      markerdictII["mec"]):
            plt.plot(time[marker], voltage[marker], alpha=.75, marker=ms, 
                     markevery=marker, mfc=mf, mec=me, ms='12', mew='2.5')
        
        legend_lists = [[] for _ in range(0, len(markerdictII["labels"]))]
        
        for mk, mf, me, lb, index in zip(markerdictII["mkshape"], 
                                         markerdictII["mfc"],
                                         markerdictII["mec"], 
                                         markerdictII["labels"], 
                                         range(0, len(legend_lists))):
            legend_lists[index].append(mlines.Line2D([], [], marker=mk, 
                                                     markersize=10, 
                                                     markeredgewidth=1.5, 
                                                     color=mf, 
                                                     markeredgecolor=me, 
                                                     label=lb))
            
        ax1 = plt.gca()
        legend = plt.legend(handles=[legend_lists[0][0], legend_lists[1][0], 
                                     legend_lists[2][0], legend_lists[3][0],
                                     legend_lists[4][0], legend_lists[5][0], 
                                     legend_lists[6][0], legend_lists[7][0],
                                     legend_lists[8][0], legend_lists[9][0]], 
                            bbox_to_anchor=(.5,-.1), loc="upper center", 
                            bbox_transform=ax1.transAxes, 
                            title="Threshold methods", fontsize=12, ncol=10, 
                            handleheight=2.4, labelspacing=0.05)

        plt.setp(legend.get_title(), fontsize=16)
        plt.title(label=self.abf_file_name, loc="center", fontsize=22, 
                  fontweight='bold', fontstyle='italic', color="black")
        plt.ylabel("Voltage (mV)", fontweight='bold', fontsize='large')
        plt.xlabel("Time (ms)", fontweight='bold', fontsize='large')
        
        if type(action) == str:
            if action == 'plot':
                return plt.show() 
            elif action == 'save':
                return plt.savefig(self.abf_file + '_thresholds' + extension)
            elif action == 'save&plot':
                return plt.savefig(self.abf_file + '_thresholds' 
                                   + extension), plt.show()
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")
    
    
    def ap_plot(self, action, extension='.png'):
        """Returns a figure with signal from abf file recording, reprezenting 
        the voltage trace (AP analyzed) with some parameters highlighted
        with specific markers.

        Parameters
        ----------
        action : str
            The action performed to the plot: 'plot', 'save' (save the figure),
            and 'plot%save'. 
         extension : str, optional
            Figure extension, as .extension (ex. '.tif', '.png'), 
            by default '.png'.
       
        Returns
        -------
        plt.Axes
            Plot the active sweep with current action potential analyzed.

        Raises
        ------
        ValueError
            Raise if the action parameter is other than 'plot', 'save' or 
            'save&plot.'
        TypeError
            Raise if action parameter is not string type.
        """
        self.abf.setSweep(self.sweep_number, self.voltage_channel_number)
        
        plt.subplots(figsize=(12,10), dpi=150)
        plt.subplots_adjust(bottom=0.32)

        peak = [self.current_peak()[1]]
        rps = [self.rp_1()[1], self.rp_2()[1], self.rp_3()[1]]
        ahps = [self.afterhyperpolarization()[1], 
                self.afterhyperpolarization_at(percentage=25)[1],
                self.afterhyperpolarization_at(percentage=50)[1], 
                self.afterhyperpolarization_at(percentage=80)[1]]
        abs_rp = [self.absolute_rp_interval[0], self.absolute_rp_interval[1]]
        max_slopes = [self.maximal_slope(phase='rise')[1], 
                      self.maximal_slope(phase='decay')[1]]
       
        markerdictI = {
            "item": [peak, rps, ahps, abs_rp, max_slopes],
            "labels":['Peak', 'RP1, RP2, RP3', 'AHP, AHP25, AHP50, AHP80',  
                      'Sample interval for absRP resting potential', 
                      'Maximal slopes:\n rise, decay', 
                     ],
            "mfc": ['#8E388E', '#EE2C2C', '#FF4500', '#8B2500', 
                    '#EE7AE9'],
            "mec": ['#8B2252', '#030303', '#4B0082', '#8B4726', 
                    '#FFA500'],
            "mkshape": ['^', 'D', 'h', 'p', 'o']
            }
 
        # Plot the first line
        plt.plot(self.abf.sweepX*1000, self.abf.sweepY, color='#515151', 
                 linewidth=3.5, alpha=1)
        # Plot the RP1, RP2, RP3 values
        for item in rps:
            plt.plot(self.abf.sweepX[item]*1000, self.abf.sweepY[item], 
                     marker='D', markevery=item, mfc='#EE2C2C', mec='#030303',
                     ms='12', mew='2.5')
        # Plot the AP peak
        plt.plot(self.abf.sweepX[self.current_peak()[1]]*1000, 
                 self.abf.sweepY[self.current_peak()[1]], 
                 marker='^', markevery=self.current_peak()[1], mfc='#8E388E', 
                 mec='#8B2252', ms='12', mew='2.5')

        # Afterhyperpolarization and ahp25, ahp50, ahp80
        for item in ahps:
            plt.plot(self.abf.sweepX[item]*1000, self.abf.sweepY[item], 
                     marker='h', markevery=item, mfc='#FF4500', mec='#4B0082', 
                     ms='10', mew='2.5')
        # Maximal slopes
        for item in max_slopes:
            plt.plot(self.abf.sweepX[item]*1000, self.abf.sweepY[item], 
                     marker='o', markevery=item, mfc='#EE7AE9', mec='#FFA500',
                     ms='10', mew='2')
        # Resting potential absolute value
        for item in abs_rp:
            plt.plot(self.abf.sweepX[item]*1000, self.abf.sweepY[item], 
                     marker='p', markevery=item, mfc='#8B2500', mec='#8B4726',
                     ms='10', mew='2')
        plt.plot(self.abf.sweepX[abs_rp[0]:abs_rp[1]]*1000, 
                 self.abf.sweepY[abs_rp[0]:abs_rp[1]], 
                 color='#EE4000', linewidth=3, alpha=.8)
        
        # Areas
        def area_generator(limL:int, limR:int, value:float, color:str, alpha:float):
            """Fills areas in plot.

            Parameters
            ----------
            limL : int
                The limit on the left side, where the filling starts.
            limR : int
                Right limit, where filling ends.
            value : float
                Value defining the second curve.
            color : str
                Filled area color
            alpha : float
                Sets the transparency of the area.

            Returns
            -------
             PolyCollection
                Fills specific area.
            """
            x = self.abf.sweepX[limL:limR] * 1000
            y = self.abf.sweepY[limL:limR]
            return plt.fill_between(x, y, value, color=color, alpha=alpha,
                                    where=(x>self.abf.sweepX[limL]) &
                                    (x <= limR))
        # AfterHyperPolarization
        area_generator(limL=self.rp_2()[1], limR=self.rp_3()[1], 
                       value=self.rp_3()[0], color='#C5C1AA', alpha=.6)   
        # AP Base
        #area_generator(limL=self.rp_1()[1], limR=self.rp_2()[1], 
                       #value=self.rp_1()[0], color='#F4A460', alpha=.5)  
        # Rising phase
        area_generator(limL=self.rp_1()[1], limR=self.current_peak()[1]+1, 
                       value=self.rp_1()[0], color='#CD96CD', alpha=.4)
        # Falling phase
        area_generator(limL=self.current_peak()[1], limR=self.rp_2()[1], 
                       value=self.rp_1()[0], color='#872657', alpha=.4) 
        
        plt.title(label=self.abf_file_name, loc="center", fontsize=22, 
                  fontweight='bold', fontstyle='italic', color="black")
    
        legend_lists = [[] for _ in range(0, len(markerdictI["labels"]))]
        
        for mk, mf, me, lb, index in zip(markerdictI["mkshape"], 
                                         markerdictI["mfc"], 
                                         markerdictI["mec"], 
                                         markerdictI["labels"], 
                                         range(0, len(legend_lists))):
            legend_lists[index].append(mlines.Line2D([], [], marker=mk, 
                                                     markersize=10, 
                                                     markeredgewidth=1.5,
                                                     color=mf,
                                                     markeredgecolor=me, 
                                                     label=lb))
            
        ax1 = plt.gca()
        legend = plt.legend(handles=[legend_lists[0][0], legend_lists[1][0], 
                                     legend_lists[2][0], legend_lists[3][0],
                                     legend_lists[4][0]], 
                            loc="upper center",
                            bbox_to_anchor=(.5,-.16), 
                            bbox_transform=ax1.transAxes, title="Legend",
                            fontsize=17, ncol=3, handleheight=2.4, 
                            labelspacing=0.05)
        
        plt.ylabel("Voltage (mV)", fontweight='bold', fontsize=22)
        plt.xlabel("Time (ms)", fontweight='bold', fontsize=22)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.setp(legend.get_title(), fontsize=17)
        
        if type(action) == str:
            if action == 'plot':
                return plt.show() 
            elif action == 'save':
                return plt.savefig(self.abf_file + extension)
            elif action == 'save-transparent':
                return plt.savefig(self.abf_file + extension, transparent=True)
            elif action == 'save&plot':
                return plt.savefig(self.abf_file + extension), plt.show()
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")
