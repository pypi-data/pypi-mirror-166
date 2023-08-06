"""Provide some useful tools used in ap, ca and rfi modules.

Layout
------
#### 1. `Filters()` 

#### 2. `Fitting()`

#### 3. `OtherTools()`
    In this class there are methods that provide tools that are not related to 
    filtering or fitting (ex. data reduction solutions).
"""
import numpy as np
from scipy import signal
from scipy import interpolate
from scipy.optimize import curve_fit


class Filters():

    def __init__(self, array:np.ndarray, cutoff_freq:int, sampling_freq:int, 
                 order:int, type:str) -> None:
        """`_summary_` 
        
    

        Parameters
        ----------
        array : np.ndarray
            The array on which the filtering will be performed.
        cutoff_freq : int
            _description_
        sampling_freq : int
            _description_
        order : int
            _description_
        type : str
            The type of filter, same as in scipy.signal methods.
        """
        self.array = array
        self.cutoff_freq = cutoff_freq
        self.sampling_freq = sampling_freq
        self.order = order
        self.type = type

    
    
    def butterworth(self) -> np.ndarray:
        """_summary_

        Returns
        -------
        np.ndarray
            _description_
        """
        nyquist = self.sampling_freq / 2
        b, a = signal.butter(self.order, self.cutoff_freq / nyquist, 
                             btype=self.type)
        result = signal.filtfilt(b, a, np.array(self.array).copy())
        return result
    
    
    def bessel(self) -> np.ndarray:
        """Returns the result of signal.bessel filtering.
        
        Examples
        --------
        
        >>> bessel_filtered_array = tools.Filters(array=a, cutoff_freq=1250, 
                                                  sampling_freq=self.abf.sampleRate, 
                                                  order=8, type='lowpass').bessel()
        >>>
        
        """
        nyquist = self.sampling_freq / 2
        b, a = signal.bessel(self.order, self.cutoff_freq / nyquist, 
                             btype=self.type)
        result = signal.filtfilt(b, a, np.array(self.array).copy())
        return result



class Fitting():
    
    def __init__(self):
        pass
    
    def boltzmann(self, xdata:np.ndarray, ydata:np.ndarray) -> tuple[np.ndarray, list[float]]:
        """_summary_

        Parameters
        ----------
        xdata : np.ndarray
            _description_
        ydata : np.ndarray
            _description_

        Returns
        -------
        np.ndarray
            _description_
        list

        """
        def func(x, A1, A2, x0, dx):
            y = (((A1 - A2) / (1 + np.exp((x - x0) / dx))) + A2) 
            return y
        p0 = [ydata[0], ydata[-1], np.median(xdata), 1,] 
        popt, pcov = curve_fit(func, xdata, ydata, p0)
        
        residuals = ydata- func(xdata, *popt)
        ss_res = np.sum(residuals**2)
        
        return func(xdata, *popt), popt
    
    def boltzmann_R(self, xdata, ydata) -> tuple[np.ndarray, list[float]]:
        """_summary_

        Parameters
        ----------
        xdata : np.ndarray
            _description_
        ydata : np.ndarray
            _description_

        Returns
        -------
        np.ndarray
            _description_
        list

        """
        def func(x, A1, A2, x0, dx):
            y = (((A1 - A2) / (1 + np.exp((x - x0) / dx))) + A2) 
            return y
        p0 = [ydata[0], ydata[-1], np.median(xdata), 1,] 
        popt, pcov = curve_fit(func, xdata, ydata, p0)
        
        residuals = ydata - func(xdata, *popt)
        ss_res = np.sum(residuals**2)
        
        ss_tot = np.sum((ydata-np.mean(ydata))**2)
        
        r_squared = 1 - (ss_res / ss_tot)
        
        return r_squared
    
    
    
    
    
    
    def mono_exponential(self, xdata, ydata):
        """_summary_

        Parameters
        ----------
        xdata : np.ndarray
            _description_
        ydata : np.ndarray
            _description_

        Returns
        -------
        tuple[np.ndarray, list]
            np.ndarray
                Fitting line.
            list
                Parameters resulting from fitting.
        """
        def func(x ,x0, A1, t, y0): 
            return A1 * np.exp(-(x-x0) / t) + y0
        p0 = (xdata[0], -1, 1, ydata[-1])
        popt, pcov = curve_fit(func, xdata,  ydata, p0)
        # popt = x0, A1, t, y0
        return func(xdata, *popt), popt
    
    
    def bi_exponential(self, xdata:np.ndarray, ydata:np.ndarray) -> tuple[np.ndarray, list]:
        """_summary_

        Parameters
        ----------
        xdata : np.ndarray
            _description_
        ydata : np.ndarray
            _description_

        Returns
        -------
        tuple[np.ndarray, list]
            np.ndarray
                Fitting line.
            list
                Parameters resulting from fitting.
        """
        def func(x ,x0, A1, t1, y0, A2, t2): 
            return A1 * np.exp(-(x-x0) / t1) + y0 + A2 * np.exp(-(x-x0) / t2)
        p0 = (xdata[0], -1, 1, ydata[-1], -1, 10)
        popt, pcov = curve_fit(func, xdata,  ydata, p0)
        return func(xdata, *popt), popt
    
  
class OtherTools():
    """In this class there are methods that provide tools that are not related 
    to filtering or fitting (ex. data reduction solutions).
    
        Methods
        ------
        
        data_reduction(xdata:np.ndarray, ydata:np.ndarray, method:str, 
                       reduction_factor:int) -> tuple[list, list]
            Performs data reduction on xdata and ydata by several methods.
            
        find_nearest(array: np.ndarray, value) -> tuple[float, int]
            Return the nearest (value, index) of an element in array to a 
            given value.
    
    """
    def data_reduction(self, xdata, ydata, method:str, reduction_factor:int):
        """Performs data reduction on xdata and ydata by several methods.

        Parameters
        ----------
        xdata : ndarray
            Raw x-data array.
        ydata : ndarray
            Raw y-data array.
        method : str
            Specify the method performed for data reduction.
            
                Method I: 'decimate'
                    Eliminates the last element in the subset i.e. the n-th 
                    element, where n is the reduction factor value.
                Method II: 'average'
                    The resulting element represents an average of items 
                    in the set.
                Method III: 'max'
                    Maximum value in set is retained.  
                Method IV: 'min'
                    Minimum value in set is retained.               
                Method V: 'min/max'
                    The min and max values in each successive set of n 
                    reduction points are retained.

        reduction_factor : int
            Describes the size of the subsets to which the data reduction 
            method will be applied.

        Returns
        -------
        tuple[list, list]
            list
                The resulting x array after data reduction.
            list
                The resulting y array after data reduction.

        Raises
        ------
        ValueError
            Raise if in 'min/max' method selected reduction factor is smaller 
            than 2.
        ValueError
            Raise if method provided value is other than 'deciamte', 'average',
            'min', 'max', 'min/max'.
        TypeError
            Raise if specified method is not string type.        
        """        
        if type(method) == str:
            
            # Method I: Decimate
            if method == 'decimate':
                xreduced = xdata[::reduction_factor]
                yreduced = ydata[::reduction_factor]
                return xreduced, yreduced

            # Method II: Substitute average
            elif method == 'average':
                xsa = np.mean(xdata.reshape(-1, reduction_factor), axis=1)
                ysa = np.mean(ydata.reshape(-1, reduction_factor), axis=1)
                return xsa, ysa
            
            # Method III: Minimum
            elif method == 'min':
                xmin = np.amin(xdata.reshape(-1, reduction_factor), axis=1)
                ymin = np.amin(ydata.reshape(-1, reduction_factor), axis=1)
                return xmin, ymin
            
            # Merhod IV: Maximum
            elif method == 'max':        
                xmax = np.amax(xdata.reshape(-1, reduction_factor), axis=1)
                ymax = np.amax(ydata.reshape(-1, reduction_factor), axis=1)
                return xmax, ymax
            
            # Method V: Min/Max
            elif method == 'min/max':
                if reduction_factor >= 2:
                    xminvals = np.amin(xdata.reshape(-1, reduction_factor), axis=1)
                    xmaxvals = np.amax(xdata.reshape(-1, reduction_factor), axis=1)
                    yminvals = np.amin(ydata.reshape(-1, reduction_factor), axis=1)
                    ymaxvals = np.amax(ydata.reshape(-1, reduction_factor), axis=1)
      
                    xminmax = []
                    yminmax = []
                    for x, y in zip(xminvals, xmaxvals):
                        xminmax.append(x)
                        xminmax.append(y)
                    for m, n in zip(yminvals, ymaxvals):
                        yminmax.append(m)
                        yminmax.append(n)
                    return xminmax, yminmax
                else:
                    raise ValueError("For this method the reduction factor must"
                                     + "be greater than or equal to 2.")
            else:
                raise ValueError("Available methods: 'deciamte', 'average', "
                                 + "'min', 'max', 'min/max'.")
        else:
            raise TypeError("Specified method has to be string type.")
    
    
    def find_nearest(self, array, value) -> tuple[float, int]:
        """Return the nearest (value, index) of an element in array to a given 
        value.
        
        Parameters
        ----------
        array : ndarray
            Array where detection is performed.
        value : float / int
            The given value which needs to be detected in array.
            
        Returns
        -------
        float / int
            The value of the element in the array closest to the parameter value.
        int
            The index of the element in the array, closest to the parameter value.
        """
        array = np.asarray(array)
        index = (np.abs(array - value)).argmin()
        return array[index], index


    def interpolation(self, xdata:np.ndarray, ydata:np.ndarray, method:str, 
                      interpolation_factor:int) -> tuple[np.ndarray, np.ndarray]:
        """_summary_

        Parameters
        ----------
        xdata : np.ndarray
            _description_
        ydata : np.ndarray
            _description_
        method : str
            _description_
        interpolation_factor : int
            _description_

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            _description_

        Raises
        ------
        ValueError
            _description_
            
        Examples
        --------
        >>> from tools import OtherTools

        >>> x = np.array([3.65, 6.5, 9.5, 12.45, 15.45, 18.45, 21.45, 24.45, 
                          27.45, 30.4, 33.4, 36.4, 39.4, 42.4, 45.4, 48.4, 51.4,
                          54.4, 57.4, 60.4, 63.4, 66.4, 69.4, 72.4, 75.4])
        >>> 
        >>> y = np.array([0.23537354, 0.53641695, 0.6974953, 0.77202374, 
                          0.81588846, 0.8479286, 0.8605062, 0.88016427, 
                          0.8894128, 0.898398, 0.90049815, 0.9071902, 
                          0.91407007, 0.9220623, 0.92449445, 0.92127657, 
                          0.9244174, 0.9324494, 0.93014866, 0.9375539, 
                          0.9359525, 0.93972915, 0.94234294, 0.9395922, 
                          0.9452315])
        >>>        
        >>>
        >>> interpolation_factor=10
        >>> cs = OtherTools.interpolation(xdata=x, ydata=y, 
        >>>                               method='cubic-spline', 
        >>>                               interpolation_factor=interpolation_factor)
        >>> 
        >>> ln = OtherTools.interpolation(xdata=x, ydata=y, 
        >>>                               method='linear', 
        >>>                               interpolation_factor=interpolation_factor)
        >>>
        >>> plt.plot(x, y, 'o', color='black', markersize=10, label='Original data')
        >>> plt.plot(cs[0], cs[1], 'o', color='orange', alpha=.75, 
        label='Cubic-spline interpolation')
        >>> plt.plot(ln[0], ln[1], 'o', color='green', alpha=.75, label='Linear interpolation')
        >>> plt.legend()
        >>> plt.show()
        >>>
        >>> print(f'Original data lenght: {len(y)}')
        >>> print(f'Cubic-spline interpolation new data lenght: {len(cs[1])}')
        >>> print(f'Linear interpolation new data lenght: {len(ln[1])}.')
        """
        new_len = len(xdata) * interpolation_factor
        new_xdata = np.linspace(start=xdata[0], stop=xdata[-1], num=new_len)
        
        if method == 'cubic-spline':
            cs = interpolate.CubicSpline(xdata, ydata)
            return new_xdata, cs(new_xdata)
        
        elif method == 'linear':
            ln = interpolate.interp1d(xdata, ydata)
            return new_xdata, ln(new_xdata)
        
        else:
            raise ValueError("Interpolation method can be 'cubic-spline' or 'linear'.")
