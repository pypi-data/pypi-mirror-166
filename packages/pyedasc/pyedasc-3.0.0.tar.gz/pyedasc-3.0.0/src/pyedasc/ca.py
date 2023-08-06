"""The code here aims to detect and analyze current traces, current-voltage
relationship, conductance, conductance & current densities in the .abf files. 
The only object in ca module is Parameters. It includes methods for current 
detection in specified region from signal, conductance and other parameters 
calculation. 

Objects
-------
Parameters(abf_file:str, current_channel_number:int, voltage_channel_number:int, 
           imemb_region:list[int], vcom_region:list[int], peak_polarity:str,
           liquid_junction_potential=None, erev_calculated:float=None, 
           erev_fit_region:list[int]=[None,None], access_resistance=None, 
           membrane_capacitance=None, membrane_resistance=None, 
           memb_time_constant=None, holding_current=None, diameter=None
"""
import os
import pyabf
import numpy as np
import matplotlib.pyplot as plt

# Local modules
from pyedasc import tools 
fit = tools.Fitting()

class Parameters():
    
    def __init__(self, abf_file:str, 
                 current_channel_number:int, 
                 voltage_channel_number:int,
                 
                 imemb_region:list[int], 
                 vcom_region:list[int], 
                 
                 peak_polarity:str,
                 liquid_junction_potential=None,
                 erev_fit_region=None, 
                 
                 access_resistance=None, 
                 membrane_capacitance=None, 
                 membrane_resistance=None, 
                 memb_time_constant=None, 
                 holding_current=None, 
                 diameter=None) -> None:
        
        """This object contains methods for extracting and analyzing parameters
        related to current analysis.

        Parameters
        ==========
        
        #### abf_file : str
            ABF file name or complete path to abf file to analyze.
            
        #### current_channel_number : int
            The number of the channel on which the current signal was recorded, 
            commonly noted and imemb. Numbering starts from 0 to n-1.
            
        #### voltage_channel_number : int
            The number of the channel on which the voltage signal was recorded, 
            commonly noted and vcom. Numbering with starts from 0 to n-1.
        
        #### imemb_region : list
            A list with 2 integers representing the interval index of the 
            current signal in which the analysis is performed.
            
        #### vcom_region : list
            A list with 2 integers representing the interval index of the 
            voltage signal in which the analysis is performed.
            
        #### peak_polarity : str
            Polarity of the current value extracted from the imemb region 
            positive, negative or mean.
            
        #### liquid_junction_potential : float / int, optional.
            Liquid junction potential calculated elsewhere, by default None.
            If passed, it is used to calculate the corrected voltage.
            
        #### erev_fit_region : list[int,int], optional
            The indices of the region on the IV relationship where to 
            extrapolate to determine the reversal potential by calculation, 
            by default None.
            
        #### access_resistance : float / int, optional
            Membrane parameter, obtained from Membrane Test parameters or 
            elsewhere. Used in Correction for Series Resistance, 
            by default None.
            
        #### membrane_capacitance : float / int, optional
            Membrane parameter, obtained from Membrane Test parameters or 
            elsewhere. Used in densities calculation, by default None.
            
        #### membrane_resistance : float / int, optional
            Membrane parameter, obtained from Membrane Test parameters or 
            elsewhere, by default None.
            
        #### memb_time_constant : float / int, optional.
            Membrane parameter, obtained from Membrane Test parameters or 
            elsewhere, by default None.
            
        #### holding_current : float / int, optional
            Membrane parameter, obtained from Membrane Test parameters or 
            elsewhere, by default None.
            
        #### diameter : float / int, optional
            Membrane parameter, obtained from Membrane Test parameters or 
            elsewhere, by default None. Used in cell area determination.
            
        Methods
        =======
        
        #### current_detection() -> list[float]:
            Returns the result of detected current in the range specified as input in 
            `imemb_region` parameter.
        
        #### voltage_steps_measured() -> list[float]:
            Returns the average voltage detected in the range specified as the 
            input in vcom_region parameter.
        
        #### voltage_steps_waveform() -> list[float]:
            Returns the voltage step values at vcom_region[0] in 
            waveform channel.

        #### voltage_steps_corrected() -> list[float]:
            Returns voltage values corrected for liquid_junction_potential and 
            access resistance, i.e series resistance, if parameters are 
            provided by user.
        
        #### reversal_potential() -> float:
            Returns the reversal potential value, calculated or provided.
            
        #### driving_force() -> list[float]:
            Returns driving force as voltage - reversal potential for every 
            voltage step in trace.
        
        #### chord_conductance() -> list[float]:
            Returns the chord conductance values for all voltage steps.
        
        #### slope_conductance() -> tuple: 
            Returns the slope conductance values for all voltage steps and 
            new x axis:
            
        #### current_density(units:str='pA/um2') -> list[float]:
            Returns current density values for all voltage steps, using 
            2 methods depending on the unit of measurement reported in 
            `units` parameter.    
            
        #### conductance_density(method:str, conductance_type:str='chord'):
            Returns conductance density for all voltage steps by 
            2 different methods. 
    
        #### plotting(parameter:str, action:str, extension:str='.png'):
            Returns a plot with x-axis the voltage steps corrected and 
            different y-axis depending on the selected parameter.
        
        """
        # ABF file initialization
        self.abf_file = abf_file
        self.abf = pyabf.ABF(self.abf_file)  
        self.abf_file_name = os.path.basename(os.path.normpath(self.abf_file))
        self.allSweeps = len(self.abf.sweepList)
        
        # Active channels
        self.current_channel_number = current_channel_number        
        self.voltage_channel_number = voltage_channel_number 
        self.ljp = liquid_junction_potential   
        self.peak_polarity = peak_polarity  
        
        # Index for the analysis interval [start, end]   
        self.imemb_region = imemb_region     
        self.vcom_region = vcom_region  
        
        # Reversal potential: index the region on IV for fitting
        self.erev_fit_region = erev_fit_region
        
        # Membrane test parameters
        self.access_resistance = access_resistance
        self.membrane_capacitance = membrane_capacitance
        self.membrane_resistance = membrane_resistance
        self.time_constant = memb_time_constant
        self.holding_current = holding_current
        self.diameter = diameter
        
        # Other parameters
        # The lowest sampling rate / signal. 1 Hz = 1/1s or 1_000_000 us
        self.sampleHz = 1_000_000 
        self.sampleInterval = int(self.sampleHz / self.abf.sampleRate)
        self.totalPoints = len(self.abf.sweepX)
        self.recTime = (self.sampleInterval * self.totalPoints) / 1000 # ms
        
        
    def current_detection(self) -> list[float]:
        """Returns the detected current in the range specified as input in 
        `imemb_region` parameter. Depending on peak_polarity the method 
        returns maximum current ('positive'), minimum current ('negative') 
        or average current ('mean'). 

        Returns
        -------
        list[float]
            Current values extracted from all sweeps in trace.  
        """     
        peak_values = []
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, self.current_channel_number)
            interval = self.abf.sweepY[self.imemb_region[0]:self.imemb_region[1]]
            if self.peak_polarity == 'positive':
                peak_values.append(max(interval))
            elif self.peak_polarity == 'negative':
                peak_values.append(min(interval))
            elif self.peak_polarity == 'mean':
                peak_values.append(np.mean(interval))
        return peak_values 
    

    def voltage_steps_measured(self) -> list[float]:
        """Returns the average voltage detected in the range specified as the 
        input in `vcom_region` parameter.
                
        Returns
        -------
        list[float]
             Mean voltage values extracted from all sweeps in trace.
        """
        voltage_steps = []
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, channel=self.voltage_channel_number)
            v_mean = np.mean(self.abf.sweepY[self.vcom_region[0]
                                             :self.vcom_region[1]])
            voltage_steps.append(v_mean)
        return voltage_steps
    
    
    def voltage_steps_waveform(self) -> list[float]:
        """Returns the voltage step values at `vcom_region[0]`
        in waveform channel.

        Returns
        -------
        list[float]
            Voltage steps values from waveform channel.
        """
        voltage_steps = []
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, channel=0)
            voltage_steps.append(self.abf.sweepC[self.vcom_region[0]])
        return voltage_steps
        
    
    def voltage_steps_corrected(self) -> list[float]:
        """Returns voltage values corrected for liquid junction potential and 
        access resistance, i.e series resistance, if parameters are provided 
        by user.
        
        First, the correction for ljp:
        
        Vcorrected = Vcom - ljp
        
        Optional, the correction for series resistance, if not allready 
        corrected by the amplifier:
        
        Vcorrected = Vcom - ljp - VRs
                
        Return
        ------
        list[float]
            Voltage step values corrected for ljp and Rs.

        """       
        vstep_values = self.voltage_steps_measured()
        
        # Correction for liquid junction potential
        if self.ljp != None:
            vstepts_corrected_LJP = []
            for v in vstep_values:
                if v < 0:
                    vstepts_corrected_LJP.append(-(abs(v) - self.ljp))
                elif v >= 0:
                    vstepts_corrected_LJP.append(v - self.ljp)
        
            # Correction for Series Resistance
            if self.access_resistance != None:
                currents = self.current_detection()
                rsCorrections = []
                for i in currents:
                    rsCorrections.append(i*self.access_resistance*0.001) 
                vstepts_corrected_LJP_Rs = []
                for v, vrs in zip(vstepts_corrected_LJP, rsCorrections):
                    vstepts_corrected_LJP_Rs.append(v - vrs)
                return vstepts_corrected_LJP_Rs
            else:
                return vstepts_corrected_LJP
        else:
            return vstep_values
         
    
    def reversal_potential(self) -> float:
        """Returns the reversal potential value, calculated by intrapolation.
        
        Method I:
            `erev_fit_region` as parameter: reversal potential is calculated by 
            extrapolation, fitting a region in IV plot (current-voltage).
            
        Returns
        -------
        float
            Reversal potential value, in mV.
        """
        rev = []
        if self.erev_fit_region != None:
            if type(self.erev_fit_region) == list and len(self.erev_fit_region) == 2:
                limL = self.erev_fit_region[0]
                limR = self.erev_fit_region[1]
                v_fit = self.voltage_steps_corrected()[limL:limR]
                i_fit = self.current_detection()[limL:limR]
                slope, intercept = np.polyfit(v_fit, i_fit, 1)
                # Extrapolation
                rev.append(-intercept / slope)
        return rev[0]
                                 
    
    def driving_force(self) -> list[float]:
        """Returns driving force as voltage - reversal potential for every 
        voltage step in trace.
        
        df = corV - revP
        
        where:
        
        df -driving force
        corV - corrected voltage
        revP - reversal potential
        
        Returns
        ------
        list[float]
            Driving force values.
        """
        vstep_values = self.voltage_steps_corrected()  
        revP = self.reversal_potential()
        driving_force = []
        for v in vstep_values:
            if self.peak_polarity == 'positive':
                if v < 0:
                    driving_force.append(-(abs(v) - revP))
                elif v >= 0:
                    driving_force.append(v - revP)
            elif self.peak_polarity == 'negative':
                driving_force.append(v - revP)
        return driving_force
    
    
    def chord_conductance(self) -> list[float]:
        """Returns the chord conductance values for all voltage steps as a list:
    
        g = (I / df)
        
        where:
    
        g - conductance 
        
        I - current
        
        df - driving force
        
        and df is: 
        
        df = voltage step - reversal potential
        
        Returns
        --------
        list[float]
            Chord conductance values.
        
        """
        peak_values = self.current_detection()
        driving_force = self.driving_force()
        conductance = []
  
        for i, df in zip(peak_values, driving_force):
            if self.peak_polarity == 'positive':
                if df < 0:
                    conductance.append((i / abs(df)))
                elif df >= 0:
                    conductance.append(i / df)
            elif self.peak_polarity == 'negative':
                conductance.append(i / df)
        return conductance
    
    
    def slope_conductance(self) -> tuple: 
        """Returns the slope conductance values for all voltage steps and 
        new x axis:
    
        g = deltaI / deltaV
        
        where:
    
        g - slope conductance 
        
        deltaI - current slopes
        
        deltaV - voltage slopes 
        
        Returns
        --------
        tuple
            list[float]
                Slope conductance values.
            list[float]
                New voltage values for x axis as averages,
                between every 2 consecutive voltage steps.
        """
        vsteps = self.voltage_steps_corrected()
        xAxisSlope = []
        for index in range(0, len(vsteps)-1):
            xAxisSlope.append((vsteps[index] + vsteps[index+1])/2)
            
        currentDiffs = np.diff(self.current_detection())
        voltageDiffs = np.diff(vsteps)
        
        slope_conductance = []
        for i, v in zip(currentDiffs, voltageDiffs):
            slope_conductance.append(i / v)
            
        return slope_conductance, xAxisSlope
            
    
    def current_density(self, units:str='pA/um2') -> list[float]:
        """Returns current density values for all voltage steps, 
        using 2 methods depending on the unit of measurement reported 
        in units parameter.


        Parameters
        ----------
        units : str, optional
            Describe the units in which current density is calculated 
            and reported, by default 'pA/um2'.
            
        * If 'units' parameter is 'pA/um2', by default, current density j is:
        
            j = I / A
            
            where:
            
            j - current density
            
            I - current detected
            
            A - area 
        
            Area has been deducted from membrane capacitance value 
            (given in pF) and converted as 1 μF / cm2, equivalent 
            to 0.01 pF / μm2 or 1 pF / 100 μm2.
        
        * If 'units' is 'pA/pF', current density j is:
        
            j = I / cm
            
            where: 
            
            cm - membrane capacitance

        Returns
        -------
        list[float]
            Current density values for all voltage steps in sweep.

        Raises
        ------
        ValueError
            Raise if 'units' parameter is other than 'pA / pF' or 'pA / um2'.
        TypeError
            Raise if 'units' parameter is not given as string type.
        TypeError
            Raise if membrane_capacitance parameter is not given.
        """
        current_values = self.current_detection()
        current_density = []
        
        if self.membrane_capacitance != None:
            area = self.membrane_capacitance * 100
            for i in current_values:
                if type(units) == str:
                    if units == 'pA/um2':
                        current_density.append(i / area)
                    elif units == 'pA/pF':
                        current_density.append(i / self.membrane_capacitance)
                    else:
                        raise ValueError("The current density must be "
                                         + "reported as input in 'units' "
                                         + "parameter, in one of the "
                                         + "2 methods: 'pA / pF' or " 
                                         +"'pA / um2'.")
                else:
                    raise TypeError("'units' parameter must be string type.")
        else:
            raise TypeError(f"Membrane capacitance not given. "
                            + f"Provide membrane_capacitance, {self} "
                            + f"class parameter, None by default.")
   
        return current_density
    
    
    def conductance_density(self) -> list[float]:
        """Returns conductance density for all voltage steps. 
        Conductance density is obtained by dividing the current 
        density values (nS/pF) by driving force values 
        (current density / driving force).
        
        To add: conductance / area Conductance density is obtained by 
        dividing the conductance values by the cell area.
       
        Returns
        -------
        list[float]
            Conductance density values.
        """
        conductance_density = []
        
        driving_force = self.driving_force()
        current_density = self.current_density(units='pA/pF')
        for j, df in zip(current_density, driving_force):
            conductance_density.append(abs(j / df))
        return conductance_density
    
    
    def fitted_parameter(self, xdata, ydata):
        """_summary_

        Parameters
        ----------
        xdata : nd.array
            _description_
        ydata : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        bz_plot = fit.boltzmann(xdata=xdata, ydata=ydata)[0]
        pz_params = fit.boltzmann(xdata=xdata, ydata=ydata)[1]
        r_squared = fit.boltzmann_R(xdata=xdata, ydata=ydata)
        
        plt.plot(xdata, ydata, '.')
        plt.plot(xdata, bz_plot)
        plt.show()
        return pz_params, r_squared
              
 
    def data_loader(self, data_to_load:str) -> list[list[float]]:
        """Creates a list of lists with the length equal to the number of 
        sweeps and assigns in each of the created lists the individual values 
        resulting from the chosen data_to_load parameter. 
        This method is used when working with several files simultaneously, 
        files acquired with the same protocol and is suitable for analysis on 
        each voltage step separately.

        Parameters
        ----------
        data_to_load : str
            Specifies the method used for value extraction.
                        
        Returns
        -------
        list[list[float]]
            Returns a list of lists, each list containing floating values 
            from the selected parameter.
            
        Raises
        ------
        ValueError
            Raise if the specified method in data_to_load parameter is invalid.
        TypeError   
            Raise if membrane_capacitance Parameters parameter is not given.
        TypeError
            Raise if method parameter is not string type.
        """
        data = []
        if type(data_to_load) == str:
            if data_to_load == 'current':
                data.append(self.current_detection())
                
            if data_to_load == 'voltage-measured':
                data.append(self.voltage_steps_measured())
                
            if data_to_load == 'voltage-corrected':
                data.append(self.voltage_steps_corrected())
                
            elif data_to_load == 'chord-conductance':
                data.append(self.chord_conductance())
                
            elif data_to_load == 'slope-conductance':
                data.append(self.slope_conductance()[0])
                
            elif data_to_load == 'current-density-pA/pF':
                data.append(self.current_density(units ='pA/pF'))
                
            elif data_to_load == 'current-density-pA/um2':
                data.append(self.current_density(units ='pA/um2'))
                
            elif data_to_load == 'conductance-density':
                data.append(self.conductance_density())
                
            else:
                raise ValueError("Specified method in data_to_load parameter is invalid.")
        else:
            raise TypeError()
           
        data_list = [[] for _ in range(self.allSweeps)]
        values = data[0]
        for i in range(0, len(data_list)-1):
            data_list[i].append(values[i])
        return(data_list)
        
                
    def plotting(self, parameter:str, action:str, extension:str='.png'):
        """Returns a plot with x-axis the voltage steps corrected and 
        different y-axis depending on the selected parameter.

        Parameters
        ----------
        parameter : str
            Selected parameter to be plotted:
                'current' : IV plot
                'chord-conductance' : GV where G is chord conductance and V is 
                                      corrected voltage.
                'slope-conductance' : GV where G is slope conductance and V is corrected voltage
                'current-density-area' : Current density given in pA/um2
                'current-density-cm' : Current density given in pA/pF
       
              
                
        action : str
            Describes the action to be performed by the method: 'plot', 'save' 
            or 'plot&save'.
        extension : str
            Describes the extension uset when the file is saved. If action
            parameter contains 'save', the function also use the extension 
            parameter, which is by default '.png'.

        Returns
        -------
        plt.Axes
            Plotting desired paramter.

        Raises
        ------
        ValueError
            Raise if the specified method in parameter is invalid.
        ValueError
            Raise if the action parameter is other than 'plot', 'save' or 
            'save&plot.'
        TypeError
            Raise if action parameter is not string type.
        """
        xaxis = []
        yaxis = []
        ylabel = []
        if parameter == 'current':
            yaxis.append(self.current_detection())
            xaxis.append(self.voltage_steps_measured())
            ylabel.append("Current (pA)")
            
        elif parameter == 'chord-conductance':
            yaxis.append(self.chord_conductance())
            xaxis.append(self.voltage_steps_corrected())
            ylabel.append("Conductance (pS)")
            
        elif parameter == 'slope-conductance':
            yaxis.append(self.slope_conductance()[0])
            xaxis.append(self.slope_conductance()[1])
            ylabel.append("Conductance (pS)")
            
        elif parameter == 'current-density-area':
            yaxis.append(self.current_density(units='pA/um2'))
            xaxis.append(self.voltage_steps_corrected())
            ylabel.append("Current density ($pA/\u03BCm^2$)")
            
        elif parameter == 'current-density-cm':
            yaxis.append(self.current_density(units='pA/pF'))
            xaxis.append(self.voltage_steps_corrected())
            ylabel.append("Current density ($pA/pF$)")
            
        elif parameter == 'conductance-density':
            yaxis.append(self.conductance_density())
            xaxis.append(self.voltage_steps_corrected())
            ylabel.append("Conductance density ($pS/\u03BCm^2$)")
            
        else:
            raise ValueError("Specified method in data_to_load parameter is invalid."
                             + " Select from: 'current', 'chord-conductance', "
                             + "'slope-conductance', 'current-density-area', "
                             + "'current-density-cm', conductance-density'. ")
            
        plt.plot(xaxis[0], yaxis[0], color='black', marker='o', linewidth=1.2)
        plt.ylabel(ylabel[0], fontweight='bold', fontsize='large')
        plt.xlabel("Voltage steps (mV)", fontweight='bold', fontsize='large')
        plt.title(label=self.abf_file_name, fontsize=22, fontweight='bold', 
                  fontstyle='italic', color="black")
        
        if type(action) == str:
            if action == 'plot':
                return plt.show()
            elif action == 'save':
                return plt.savefig(self.abf_file_name + extension)
            elif action == 'save&plot':
                return plt.savefig(self.abf_file_name + extension), plt.show()
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action must be string type.")
        
        