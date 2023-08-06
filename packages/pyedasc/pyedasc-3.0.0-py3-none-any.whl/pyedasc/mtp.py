"""Code here extracts the membrane test parameters from '.sta' files. 
The only class in module is `Extractor()` which open the '.sta' files as text 
files and process the columns for value extraction.

Layout:
-------

`Extractor(reading_range:list[int]=None)`

1. `process_text_file(file)` : this method open the '.sta' file as a text file 
and prepare extraction.

2. `cm(file)`, `rm(file)`, `ra(file)`, `tau(file)`, `hold(file)`, 
`diameter(file)` : methods used for individual extraction of parameters from 
different columns in the processed file. 
"""
import os
import math
import numpy as np


class Extractor():

    def __init__(self, reading_range=None):
        """Object used to extract test membrane parameters from different 
        columns of the '.sta' file.

        Parameters
        ==========
        #### reading_range : list[int], optional
            A list of 2 integers representing the indices of the interval on 
            the column in which to mediate the values, by default None and 
            reading range is from the 20th to 100th value in column.
        
        Methods
        ==========
        #### process_text_file(file) -> list[list]
            Processes the '.sta' file as a text file to extract only the values
            from the columns. 
            
        #### cm(file) -> float
            Extracts membrane capacitance value from column 2. 
            
        #### rm(file) -> float
            Extracts membrane resistance value from column 3. 
            
        #### ra(file) -> float
            Extracts access resistance capacitance value from column 4. 
            
        #### tau(file) -> float
            Extracts tau value from column 5.
            
        #### hold(file) -> float
            Extracts holding current value from column 6.
            
        #### diameter(file) -> float
            Calculates diameter value from starting from membrane capacitance.
        """
        if reading_range == None:
            self.reading_range = [20, 100]
        elif type(reading_range) == list:
            self.reading_range = [reading_range[0], reading_range[1]]

    
    def process_text_file(self, file):
        """Open the '.sta' file as a text file and prepare the columns for 
        data extraction.

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters.

        Returns
        -------
        list[list]
            List of lists with processed '.sta' file columns.
        """
        f=open(file, "r")
        lines = f.readlines()
        
        proccesed_text_lines = []
        for x in lines:
            proccesed_text_lines.append([x.split() for x in open(file).readlines()])
            f.close()
        return proccesed_text_lines[0]
     

    def cm(self, file):
        """Returns membrane capacitance mean value in reading range, 
        from second column in proccesed '.sta' file.

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters

        Returns
        -------
        float
            Membrane capacitance mean value in pF (picofarads).
        """
        cm_list = []
        processed_file = self.process_text_file(file)
        for i in range(self.reading_range[0], self.reading_range[1]):
            cm_list.append(float(processed_file[i][1]))
        cm = round(np.mean(cm_list), 2)
        return cm
    
    
    def rm(self, file):
        """Returns membrane resistance mean value in reading range, 
        from third column in proccesed '.sta' file.

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters

        Returns
        -------
        float
            Membrane resistance mean value in MΩ (megaohms).
        """
        rm_ghom_list = []
        processed_file = self.process_text_file(file)
        for i in range(self.reading_range[0], self.reading_range[1]):
            rm_ghom_list.append(float(processed_file[i][2]))
        rm = round(np.mean(rm_ghom_list)*1000, 2)
        return rm
    
    
    def ra(self, file):
        """Returns access resistance mean value in reading range, 
        from fourth column in proccesed '.sta' file.

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters.

        Returns
        -------
        float
            Access resistance mean value MΩ (megaohms).
        """
        ra_list = []
        processed_file = self.process_text_file(file)
        for i in range(self.reading_range[0], self.reading_range[1]):   
            ra_list.append(float(processed_file[i][3]))
        ra = round(np.mean(ra_list), 2)
        return ra
    
    
    def tau(self, file):
        """Returns tau (membrane time constant) mean value in reading range, 
        from fifth column in proccesed '.sta' file. 

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters.

        Returns
        -------
        float
            Tau mean value in μs (microseconds).
        """
        tau_list = []
        processed_file = self.process_text_file(file)
        for i in range(self.reading_range[0], self.reading_range[1]):
            tau_list.append(float(processed_file[i][4]))
        tau = round(np.mean(tau_list), 2)
        return tau
    
    
    def hold(self, file):
        """Returns the steady state (holding current - hold) mean value in 
        reading range, from sixth column in proccesed '.sta' file. 

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters.

        Returns
        -------
        float
            Hold mean value in pA (picoamphers).
        """
        hold_list = []
        processed_file = self.process_text_file(file)
        for i in range(self.reading_range[0], self.reading_range[1]):
            hold_list.append(float(processed_file[i][5])) 
        hold = round(np.mean(hold_list), 2)
        return hold
    
    
    def diameter(self, file):
        """Returns the cell diameter starting from the value of the membrane 
        capacitance. 
        The area was calculated considering 0.01 pF / μm2 (square micrometers) 
        which is equivalent to 1 pF / 100 μm2. 
        
        As a result:
        
        #### area (in μm2) = cm (in pF) * 100  
        
        #### radius (in μm) = sqrt(area / (4 * pi))
            
        and
        
        #### diameter (in μm) = radius * 2

        Parameters
        ----------
        file : '.sta' file
            '.sta' file that contains membrane test parameters.

        Returns
        -------
        float
            Diameter value in μm (micrometers).
        """
        cm = self.cm(file)
        area = cm * 100
        radius = math.sqrt(area / (4 * math.pi))
        dm = round((radius * 2), 2)
        return dm
    
