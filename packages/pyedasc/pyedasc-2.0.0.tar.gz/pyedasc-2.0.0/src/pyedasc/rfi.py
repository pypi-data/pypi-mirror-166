"""

"""
import os
import pyabf
import numpy as np
import matplotlib.pyplot as plt

# local import
from pyedasc import tools
fit = tools.Fitting()

class RFI():

    def __init__(self, abf_file:str, 
                 current_channel_number:int, 
                 reference_int:list[int], 
                 recovery_int:list[int], 
                 baseline_interval:list[int],
                 t0_recovery:int,):

        self.abf_file = abf_file
        self.abf = pyabf.ABF(abf_file)
        self.abf_file_name = os.path.basename(os.path.normpath(self.abf_file))
        self.current_channel_number = current_channel_number
        self.reference_interval = reference_int
        self.recovery_interval = recovery_int
        self.baseline_interval = baseline_interval
        self.t0_recovery = t0_recovery

    def reference_peaks(self) -> list[float]:
        """This method extract the reference peaks, i.e. the first inward 
        peak generated with the first pulse applied. The extraction 
        is performed for all sweeps in the recording; interval provided in 
        `reference_interval` parameter.
        
        Returns
        -------
        list[float]
            A list of peak inward currents detected, in mV.
        """
        limL = self.reference_interval[0]
        limR = self.reference_interval[1]
        
        ref_peak_values = []
        for sweepNumber in self.abf.sweepList: 
            self.abf.setSweep(sweepNumber, self.current_channel_number)
            detection_interval = self.abf.sweepY[limL:limR]                                           
            ref_peak_values.append(min(detection_interval))
        return ref_peak_values
    
    
    def baseline_substraction(self) -> list[float]:
        """Extracts the average current value from a trace segment before 
        the recovery peaks region begin. Segment boundaries are specified 
        as an input list by `baseline_interval` attribute.

        Returns
        -------
        list[float]
            A list of mean current values for all traces in a region specified 
            by the `baseline_interval` attribute.
        """
        mean_current = []
        limL = self.baseline_interval[0]
        limR = self.baseline_interval[1]
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, self.current_channel_number)
            subtraction_interval = self.abf.sweepY[limL:limR]
            mean_current.append(np.mean(subtraction_interval))

        return mean_current
            
            
    def recovery_peaks_detected(self) -> tuple[list[float],list[float]]:
        """Detects negative current peaks in the range provided 
        by the `recovery_interval` parameter.

        Returns
        -------
        list[float]
            A list of current peaks detected, in mV. 
        """
        peak_values = []
        peak_indices = []

        limL = self.recovery_interval[0]
        limR = self.recovery_interval[1]

        for sweepNumber in self.abf.sweepList: 
            self.abf.setSweep(sweepNumber, self.current_channel_number)
            detection_interval = self.abf.sweepY[limL:limR]
            
            for index, value in enumerate(detection_interval): 
                if value == min(detection_interval):
                    peak_indices.append(index + limL)
                    peak_values.append(value)
             
        return peak_values, peak_indices
    
                    
    def recovery_peaks_baselined(self) -> list[float]:
        """Returns the values of the negative peaks in the range described 
        by the `recovery_int` parameter from which the mean baseline values 
        in the interval described by `baseline_interval` parameter were 
        substracted.

        Returns
        -------
        list[float]
            A list of recovery peak values from which the baseline value 
            was subtracted.
        """
        baseline = self.baseline_substraction()
        rec_peaks_det = self.recovery_peaks_detected()[0]
        peak_values_extracted = []
        for i, j in zip(rec_peaks_det, baseline):
            peak_values_extracted.append(i - j)
                    
        return peak_values_extracted

    
    def normalized_peaks_to_ref(self) -> list[float]:
        """Normalizes the recovery peak to the reference peak for all 
        sweeps in the recording.

        Returns
        -------
        list[float]
            A list of negative peak currents, representing the normalized 
            values of the recovery peaks to the reference ones, in mV.
        """
        ref_peaks= self.reference_peaks()
        rec_peaks = self.recovery_peaks_baselined()
        normalized_peaks = []
        for rec, ref in zip(rec_peaks, ref_peaks):
            normalized_peaks.append(rec / ref)
        return normalized_peaks
        
        
    def time_values(self) -> list[float]:   
        """Calculates the time interval values from each recovery peak to an 
        initial value, `t0_recovery`. T0 is chosen by the user and represents 
        the index of the starting point from the epoch in the recovery 
        waveform.

        Returns
        -------
        list[float]
            _description_
        """
        time_ms = [i * 1000 for i in self.abf.sweepX]
        t0_value = time_ms[self.t0_recovery]
        recovery_peaks_index = self.recovery_peaks_detected()[1]
        # Time values at each recovery peak
        peaks_times = []
        for i in recovery_peaks_index:
            peaks_times.append(time_ms[int(i)])
        # Difference between each recovery peak time and initial time   
        peaks_final = []
        for t in peaks_times:
            peaks_final.append(round(t - t0_value, 2))
        return peaks_final
    
    
    def tau_value(self) -> float:
        """Fits the normalized peaks at baselined time values with 
        mono-exponential fit and extracts tau constant.

        Returns
        -------
        float
            Tau value in ms.
        """
        x = self.time_values()
        y = self.normalized_peaks_to_ref()
        
        decay_constant = fit.mono_exponential(xdata=x, ydata=y)[1][2]
        return decay_constant
  
        
    def plotting(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        x = self.time_values()
        y = self.normalized_peaks_to_ref()
        fit_trace = fit.mono_exponential(xdata=x, ydata=y)[0]
        
        plt.figure(figsize=(12, 16), dpi=120)
        
        plt.title(label=f"{self.abf_file_name}", fontsize=18, fontweight='bold')
        plt.xlabel("Time (ms)", fontweight='bold', fontsize='large')
        plt.ylabel("Current peaks normalized to reference peaks", 
                   fontweight='bold', fontsize='large')
        
        plt.plot(x, y, 'o') 
        plt.plot(x, fit_trace) 
        
        return plt.show()
    
    def raw_plotting(self):
        
     
        fig = plt.figure(figsize=(20, 15), dpi=150)
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        timeMS = self.abf.sweepX * 1000

        for sweep in self.abf.sweepList:
            self.abf.setSweep(sweep, channel=0)
            ax1.plot(timeMS, self.abf.sweepY, color='k')

        
        
        fig.tight_layout(pad=3.0)

        return plt.show()

    