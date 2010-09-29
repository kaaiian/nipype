# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""

Interfaces to functionality from nitime for time-series analysis of fmri data 

- nitime.analysis.CoherenceAnalyzer: Coherence/y 
- nitime.fmri.io:  
- nitime.viz.drawmatrix_channels

"""


from nipype.utils.misc import package_check
package_check('nitime')
package_check('matplotlib')


from nipype.interfaces.base import (TraitedSpec, File, InputMultiPath,
                                    OutputMultiPath, Undefined, traits,
                                    BaseInterface)
from nitime.analysis import CoherenceAnalyzer
from nitime.timeseries import TimeSeries

from matplotlib.mlab import csv2rec
    
class CoherenceAnalyzerInputSpec(TraitedSpec):

    #Input either csv file, or time-series object and use _xor_inputs to
    #discriminate
    _xor_inputs=('in_file','in_TS')
    in_file = File(desc=('csv file with ROIs on the columns and ',
                   'time-points on the rows. ROI names at the top row'),
                   exists=True,
                   requires=('TR',))
    
    #If you gave just a file name, you need to specify the sampling_rate:
    TR = traits.Float(desc=('The TR used to collect the data',
                            'in your csv file <in_file>'))

    in_TS = traits.Any(desc='a nitime TimeSeries object')

    NFFT = traits.Range(low=32,value=64,
                        desc=('This is the size of the window used for ',
                        'the spectral estimation. Use values between ',
                        '32 and the number of samples in your time-series.',
                        '(Defaults to 64.)'))
    n_overlap = traits.Range(low=0,value=0,
                             desc=('The number of samples which overlap',
                             'between subsequent windows.(Defaults to 0)'))
    
    frequency_range = traits.ListFloat(value=[0.02, 0.15],
                                       minlen=2,
                                       maxlen=2,
                                       desc=('The range of frequencies over',
                                             'which the analysis will average.',
                                             '[low,high] (Default [0.02,0.15]'))

    output_csv_file = traits.File(desc='File to write output')
    output_figure_file = traits.File(desc='File to write output figures')
    figure_type = traits.Enum('matrix','network',
                              desc=("The type of plot to generate, where ",
                                    "'matrix' denotes a matrix image and",
                                    "'network' denotes a graph representation"))
    
class CoherenceAnalyzerOutputSpec(TraitedSpec):
    coherence_array = traits.Array(desc=('The pairwise coherence values between',
                                   'the ROIs'))
    timedelay_array = traits.Array(desc=('The pairwise time delays between the',
                                         'ROIs (in seconds)'))

    coherence_csv = traits.File(desc = ('A csv file containing the pairwise ',
                                        'coherence values'))
    timedelay_csv = traits.File(desc = ('A csv file containing the pairwise ',
                                        'time delay values'))

    coherence_fig = traits.File(desc = ('Figure representing coherence values'))
    timedelay_fig = traits.File(desc = ('Figure representing coherence values'))

    
class CoherenceAnalyzer(BaseInterface):

    input_spec = CoherenceAnalyzerInputSpec
    output_spec = CoherenceAnalyzerOutputSpec

    def _read_csv(self):
        """ Read from csv in_file and return a rec array """
        #Check that input conforms to expectations:
        first_row = open(self.inputs.in_file).readline()
        if not first_row[1].isalpha():
            raise ValueError("First row of in_file should contain ROI names as strings of characters")

        rec_array=csv2rec(self.inputs.in_file)
        return rec_array

    def _csv2ts(self):
        """ Read data from the in_file and generate a nitime TimeSeries object"""
        rec_array = self._read_csv()
        roi_names= data_rec.dtype.names
        n_samples = data_rec.shape[0]
        for n_idx in range(len(roi_names)):
            data[n_idx] = data_rec[roi_names[n_idx]]

        TS = TimeSeries(data=data,sampling_interval=TR,time_unit='s')

        return TimeSeries(data=data
                          
        
        
    #Rewrite _run_interface, but not run
    def _run_interface(self,runtime):
        lb, ub = self.inputs.frequency_range

        if self.inputs.in_TS is Undefined:
            # get TS form csv and inputs.TR
            # calls _csv2ts
            
        else:
            # get TS from inputs.in_TS
            
            
        #Get the coherence matrix from the analyzer
        self.coherence = A.coherence

        if isdefined(self.inputs.output_csv_file):
            #write to a csv file and assign a value to self.coherence_file (a
            #file name + path)
            
    #Rewrite _list_outputs (look at BET)
    def _list_outputs(self):
        outputs = self.output_spec().get()

        #Always defined:
        outputs['coherence']=self.coherence #The array 
        #Conditional
        if isdefined(self.inputs.output_csv_file):
            outputs['coherence_csv']=self.coherence_file

        return outputs
    
class GetTimeSeriesInputSpec():
    pass
class GetTimeSeriesOutputSpec():
    pass
class GetTimeSeries():
    # getting time series data from nifti files and ROIs
    pass
