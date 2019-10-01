# -*- coding: utf-8 -*-
# 
# 
# 
# Created: 2019-10-01 11:39:36
# Last modified by: Joscha Schmiedt [joscha.schmiedt@esi-frankfurt.de]
# Last modification time: <2019-10-01 13:37:17>

import os
import numpy as np
import syncopy as spy
from tqdm import tqdm
from syncopy.shared.parsers import data_parser
import syncopy as spy

__all__ = ["timelockanalysis"]

def timelockanalysis(data, selected_trials=None):
    """Prototype function for averaging AnalogData across trials
    
    Parameters
    ----------
    data : :class:`syncopy.AnalogData` object
        Syncopy data object to be averaged across trials
    selected_trials : :class:`numpy.ndarray`
        Array of trial indices to be used for averaging
    
    Returns
    -------
    dict
        Dictionary with keys "avg", "var", "dof" "time", "channel" for average
        variance, degrees of freedom, time axis, and channel labels

    Note
    ----
    This function is merely a proof of concept for averaging across trials with
    an online algorithm. The final version for release will change severely. 
    FIXME: There are currently no tests for this function.
    FIXME: Check for non-standard dimord
    FIXME: Maybe we don't need to iterate over `data.trialdefinition` 
           but can use `selected_trials` directly to allocate a smaller `intTimeAxes` array
    FIXME: the output should be a "proper" Syncopy object
    """
    
    try:
        data_parser(data, varname="data", empty=False, dataclass=spy.AnalogData)
    except Exception as exc:
        raise exc

    
    if selected_trials is None:
        selected_trials = np.arange(len(data.trials))

    intTimeAxes = [(np.arange(0, stop - start) + offset)
                for (start, stop, offset) in data.trialdefinition[:, :3]]
    intervals = np.array([(x.min(), x.max()) for x in intTimeAxes])

    avgTimeAxis = np.arange(start=intervals.min(),
                            stop=intervals.max()+1)                        

    targetShape = (avgTimeAxis.size, len(data.channel))
    avg = np.zeros(targetShape)
    var = np.zeros(targetShape)
    dof = np.zeros(targetShape)
    oldAvg = np.zeros(targetShape)

    nTrial = len(data.trials)

    fullArray = np.empty((avgTimeAxis.size, len(data.channel), nTrial))
    fullArray[:] = np.nan

    # Welford's online method for computing-variance
    # http://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/

    for iTrial in tqdm(selected_trials):
        x = data.trials[iTrial]
        trialTimeAxis = intTimeAxes[iTrial]
            
        targetIndex = np.in1d(avgTimeAxis, trialTimeAxis, assume_unique=True)
        dof[targetIndex, :] += 1
        oldAvg = avg.copy()
        avg[targetIndex, :] += (x-avg[targetIndex, :]) / (dof[targetIndex, :])
        var[targetIndex, :] += (x-avg[targetIndex, :]) * (x - oldAvg[targetIndex, :])    
        if np.mod(iTrial, 10) == 0:
            data.clear()    

    dof -= 1
    var /= dof+1
    
    result = spy.StructDict()
    result.avg = avg
    result.var = var
    result.dof = dof
    result.channel = data.channel    
    result.time = avgTimeAxis
    
    return result


if __name__ == "__main__":
    analogData = spy.load("~/testdata.spy")
    conditions = np.unique(analogData.trialinfo)
    tl = []
    for condition in conditions:
        selection = np.nonzero(analogData.trialinfo == condition)[0]
        tl.append(timelockanalysis(analogData, selection))
    chan = list(analogData.channel).index("vprobeMUA_020")

    from scipy.signal import savgol_filter
    import matplotlib.pyplot as plt
    for t in tl:
        plt.plot(t.time,  savgol_filter(t.avg[:, chan], 71, 3))    
        plt.fill_between(t.time, 
                        t.avg[:, chan] + np.sqrt(t.var[:, chan]/t.dof[:, chan]**2),
                        t.avg[:, chan] - np.sqrt(t.var[:, chan]/t.dof[:, chan]**2), 
                        alpha=0.5)
    plt.show()


