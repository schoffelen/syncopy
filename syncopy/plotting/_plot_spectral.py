# -*- coding: utf-8 -*-
# 
# Outsourced plotting class methods from respective parent classes
# 
# Created: 2020-07-15 10:26:48
# Last modified by: Stefan Fuertinger [stefan.fuertinger@esi-frankfurt.de]
# Last modification time: <2020-08-05 16:55:51>

# Builtin/3rd party package imports
import os
import numpy as np

# Local imports
from syncopy.shared.errors import SPYValueError, SPYError, SPYTypeError, SPYWarning
from syncopy.shared.tools import layout_subplot_panels
from syncopy.shared.parsers import scalar_parser
from syncopy.plotting.spy_plotting import pltErrMsg, pltConfig, _compute_toilim_avg
from syncopy import __plt__
if __plt__:
    import matplotlib.pyplot as plt
    from matplotlib import colors

__all__ = []


def singlepanelplot(self, trials="all", channels="all", tapers="all", toilim=None, foilim=None,
                    avg_channels=True, avg_tapers=True, toi=None, foi=None,
                    interp="spline36", cmap="plasma", vmin=None, vmax=None, 
                    title=None, grid=None, fig=None, **kwargs):
    """
    Coming soon...
    
    overlay-plotting not supported for TF data
    
    TF data: to compare different objects, vmin and vmax should be set!
    """
    
    # import ipdb; ipdb.set_trace()
    inputArgs = locals()
    inputArgs.pop("self")
    (dimArrs, 
    dimCounts, 
    isTimeFrequency, 
    complexConversion, 
    pltDtype, 
    dataLbl) =  _prep_spectral_plots(self, "singlepanelplot", **inputArgs)
                                    #  "singlepanelplot", 
                                    #  trials, 
                                    #  channels, 
                                    #  tapers, 
                                    #  toilim, 
                                    #  foilim,
                                    #  avg_channels, 
                                    #  avg_tapers, 
                                    #  title, 
                                    #  grid,
                                    #  vmin,
                                    #  vmax)
                                    
    (nTrials, nChan, nFreq, nTap) = dimCounts
    (trList, chArr, freqArr, tpArr) = dimArrs
    
    import ipdb; ipdb.set_trace()
    
    # BEGIN OF >>> _prep_specral_plots(__name__, ...)
    
    # # Abort if matplotlib is not available
    # if not __plt__:
    #     raise SPYError(pltErrMsg.format("singlepanelplot"))
    
    # # Ensure our binary flags are actually binary
    # if not isinstance(avg_channels, bool):
    #     raise SPYTypeError(avg_channels, varname="avg_channels", expected="bool")
    # if not isinstance(avg_tapers, bool):
    #     raise SPYTypeError(avg_tapers, varname="avg_tapers", expected="bool")
    
    # # Pass provided selections on to `Selector` class which performs error 
    # # checking and generates required indexing arrays
    # self._selection = {"trials": trials, 
    #                    "channels": channels, 
    #                    "tapers": tapers,
    #                    "toilim": toilim,
    #                    "foilim": foilim}
    
    # # Ensure any optional keywords controlling plotting appearance make sense
    # if title is not None:
    #     if not isinstance(title, str):
    #         raise SPYTypeError(title, varname="title", expected="str")
    # if grid is not None:
    #     if not isinstance(grid, bool):
    #         raise SPYTypeError(grid, varname="grid", expected="bool")

    # # Get trial/channel/taper count
    # trList = self._selection.trials
    # nTrials = len(trList)
    # chArr = self.channel[self._selection.channel]
    # nChan = chArr.size
    # freqArr = self.freq[self._selection.freq]
    # nFreq = freqArr.size
    # tpArr = np.arange(self.taper.size)[self._selection.taper]
    # nTap = tpArr.size

    # # Determine whether we're dealing w/tf data
    # isTimeFrequency = False
    # if any([t.size > 1 for t in self.time]):
    #     isTimeFrequency = True
        
    # # Ensure provided min/max range for plotting TF data makes sense
    # vminmax = False
    # if vmin is not None:
    #     try:
    #         scalar_parser(vmin, varname="vmin")
    #     except Exception as exc:
    #         raise exc 
    #     vminmax = True
    # if vmax is not None:
    #     try:
    #         scalar_parser(vmin, varname="vmax")
    #     except Exception as exc:
    #         raise exc 
    #     vminmax = True
    # if vmin is not None and vmax is not None:
    #     if vmin >= vmax:
    #         lgl = "minimal data range bound to be less than provided maximum "
    #         act = "vmax < vmin"
    #         raise SPYValueError(legal=lgl, varname="vmin/vamx", actual=act)
    # if vminmax and not isTimeFrequency:
    #     msg = "`vmin` and `vmax` is only used for time-frequency visualizations"
    #     SPYWarning(msg)
        
    # # Check for complex entries in data and set datatype for plotting arrays 
    # # constructed below (always use floats w/same precision as data)
    # if "complex" in self.data.dtype.name:
    #     msg = "Found complex Fourier coefficients - visualization will use absolute values."
    #     SPYWarning(msg)
    #     complexConversion = lambda x: np.absolute(x).real
    #     pltDtype = "f{}".format(self.data.dtype.itemsize)
    #     dataLbl = "Absolute Frequency [dB]"
    # else:
    #     complexConversion = lambda x: x
    #     pltDtype = self.data.dtype
    #     dataLbl = "Power [dB]"
        
    # END OF >>> _prep_specral_plots(__name__, ...)
    
    # If we're overlaying, ensure data and plot type match up    
    if hasattr(fig, "objCount"): 
        if isTimeFrequency:
            msg = "Overlay plotting not supported for time-frequency data"
            raise SPYError(msg)
        if not hasattr(fig, "isSpectralPlot"):
            lgl = "figure visualizing data from a Syncopy `SpectralData` object"
            act = "visualization of other Syncopy data"
            raise SPYValueError(legal=lgl, varname="fig", actual=act)
        if hasattr(fig, "multipanelplot"):
            lgl = "single-panel figure generated by `singleplot`"
            act = "multi-panel figure generated by `multipanelplot`"
            raise SPYValueError(legal=lgl, varname="fig", actual=act)

    # No time-frequency shenanigans: this is a simple power-spectrum (line-plot)
    if not isTimeFrequency:
        
        # Generic titles for figures
        overlayTitle = "Overlay of {} datasets"
    
        # Either create new figure or fetch existing
        if fig is None:
            fig, ax = plt.subplots(1, tight_layout=True, squeeze=True,
                                   figsize=pltConfig["singleFigSize"])
            ax.set_xlabel("Frequency [Hz]", size=pltConfig["singleLabelSize"])            
            ax.set_ylabel(dataLbl, size=pltConfig["singleLabelSize"])            
            ax.tick_params(axis="both", labelsize=pltConfig["singleTickSize"])
            ax.autoscale(enable=True, axis="x", tight=True)
            fig.isSpectralPlot = True
            fig.singlepanelplot = True
            fig.objCount = 0
        else:
            ax, = fig.get_axes()        

        # Average across channels, tapers or both using local helper func
        nTime = 1
        if not avg_channels and not avg_tapers and nTap > 1:
            msg = "Either channels or trials need to be averaged for single-panel plot"
            SPYWarning(msg)
            return
        if avg_channels and not avg_tapers:
            panelTitle = "{} tapers averaged across {} channels and {} trials".format(nTap, nChan, nTrials)
            pltArr = _compute_pltArr(self, nFreq, nTap, nTime, complexConversion, pltDtype, 
                                     avg1="channel")
        if avg_tapers and not avg_channels:
            panelTitle = "{} channels averaged across {} tapers and {} trials".format(nChan, nTap, nTrials)
            pltArr = _compute_pltArr(self, nFreq, nChan, nTime, complexConversion, pltDtype, 
                                     avg1="taper")
        if avg_tapers and avg_channels:
            panelTitle = "Average of {} channels, {} tapers and {} trials".format(nChan, nTap, nTrials)
            pltArr = _compute_pltArr(self, nFreq, 1, nTime, complexConversion, pltDtype, 
                                     avg1="taper", avg2="channel")

        # Perform the actual plotting
        ax.plot(freqArr, np.log10(pltArr), label=os.path.basename(self.filename))
        ax.set_xlim([freqArr[0], freqArr[-1]])
        if grid is not None:
            ax.grid(grid)
                
        # Set plot title depending on dataset overlay
        if fig.objCount == 0:
            if title is None:
                title = panelTitle
            ax.set_title(title, size=pltConfig["singleTitleSize"])
        else:
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels)
            if title is None:
                title = overlayTitle.format(len(handles))
            ax.set_title(title, size=pltConfig["singleTitleSize"])
        
    else:
        
        # For a single-panel TF visualization, we need to average across both tapers + channels        
        if not avg_channels and (not avg_tapers and nTap > 1):
            msg = "Single-panel time-frequency visualization requires averaging " +\
                "across both tapers and channels"
            SPYWarning(msg)
            return
        
        # Compute (and verify) length of selected time intervals and assemble array for plotting
        panelTitle = "Average of {} channels, {} tapers and {} trials".format(nChan, nTap, nTrials)
        tLengths = _compute_toilim_avg(self)
        nTime = tLengths[0]
        pltArr = _compute_pltArr(self, nFreq, 1, nTime, complexConversion, pltDtype, 
                                 avg1="taper", avg2="channel")

        # Prepare figure
        # FIXME: fig, ax_arr, cax = setup_figure(npanels, nrow=None, ncol=None, include_colorbar=False, sharex=None, sharey=None)
        # FIXME: call here: fig, ax, cax = setup_figure(1, None, None, include_colorbar=True, sharex=False, sharey=False)
        fig, (ax, cax) = plt.subplots(1, 2, tight_layout=True, squeeze=True, 
                                      gridspec_kw={"wspace": 0.05, "width_ratios": [1, 0.025]},
                                      figsize=pltConfig["singleFigSize"])
        ax.set_xlabel("Time [s]", size=pltConfig["singleLabelSize"])            
        ax.set_ylabel("Frequency [Hz]", size=pltConfig["singleLabelSize"])            
        ax.tick_params(axis="both", labelsize=pltConfig["singleTickSize"])
        cax.tick_params(axis="both", labelsize=pltConfig["singleTickSize"])
        ax.autoscale(enable=True, axis="x", tight=True)
        fig.isSpectralPlot = True
        fig.singlepanelplot = True
        fig.objCount = 0
        
        # Use `imshow` to render array as image
        time = self.time[trList[0]][self._selection.time[0]]
        ax.imshow(pltArr, origin="lower", interpolation=interp, 
                  cmap=cmap, vmin=vmin, vmax=vmax,
                  extent=(time[0], time[-1], freqArr[0], freqArr[-1]), aspect="auto")
        # FIXME: cbar = setup_colorbar(axes, cax, label=None, outline=False, vmin=None, vmax=None)
        # FIXME: call here: cbar = setup_colorbar(ax.images[0], cax, label="Power")
        cbar = fig.colorbar(ax.images[0], cax=cax) 
        cbar.set_label(dataLbl, size=pltConfig["singleLabelSize"])
        cbar.outline.set_visible(False)
        if grid is not None:
            ax.grid(grid)
        if title is None:
            title = panelTitle
        ax.set_title(title, size=pltConfig["singleTitleSize"])

    # Increment overlay-counter and draw figure
    fig.objCount += 1
    plt.draw()
    self._selection = None
    return fig


def multipanelplot(self, trials="all", channels="all", tapers="all", toilim=None, foilim=None,
                   avg_channels=True, avg_tapers=True, avg_trials=False, panels="channels",
                   interp="spline36", cmap="plasma", title=None, grid=None, fig=None, **kwargs):
    """
    Coming soon...
    
    overlay-plotting not supported (at all)
    
    use `availablePanels` in Parameters section!
    """

    #: available panel settings for :func:`~syncopy.multipanelplot`
    availablePanels = tuple(["channels", "trials", "tapers"])
                            
    # >>> _prep_specral_plots(__name__, ...)
    
    # Abort if matplotlib is not available
    if not __plt__:
        raise SPYError(pltErrMsg.format("singlepanelplot"))
    
    # Ensure our binary flags are actually binary
    if not isinstance(avg_channels, bool):
        raise SPYTypeError(avg_channels, varname="avg_channels", expected="bool")
    if not isinstance(avg_tapers, bool):
        raise SPYTypeError(avg_tapers, varname="avg_tapers", expected="bool")
    
    # Pass provided selections on to `Selector` class which performs error 
    # checking and generates required indexing arrays
    self._selection = {"trials": trials, 
                       "channels": channels, 
                       "tapers": tapers,
                       "toilim": toilim,
                       "foilim": foilim}
    
    # Ensure any optional keywords controlling plotting appearance make sense
    if title is not None:
        if not isinstance(title, str):
            raise SPYTypeError(title, varname="title", expected="str")
    if grid is not None:
        if not isinstance(grid, bool):
            raise SPYTypeError(grid, varname="grid", expected="bool")

    # Get trial/channel/taper count
    trList = list(self._selection.trials)
    nTrials = len(trList)
    chArr = self.channel[self._selection.channel]
    nChan = chArr.size
    freqArr = self.freq[self._selection.freq]
    nFreq = freqArr.size
    tpArr = np.arange(self.taper.size)[self._selection.taper]
    nTap = tpArr.size
        
    # Determine whether we're dealing w/tf data
    isTimeFrequency = False
    if any([t.size > 1 for t in self.time]):
        isTimeFrequency = True
        
    # Check for complex entries in data and set datatype for plotting arrays 
    # constructed below (always use floats w/same precision as data)
    if "complex" in self.data.dtype.name:
        msg = "Found complex Fourier coefficients - visualization will use absolute values."
        SPYWarning(msg)
        complexConversion = lambda x: np.absolute(x).real
        pltDtype = "f{}".format(self.data.dtype.itemsize)
        dataLbl = "Absolute Frequency [dB]"
    else:
        complexConversion = lambda x: x
        pltDtype = self.data.dtype
        dataLbl = "Power [dB]"
        
    # END OF >>> _prep_specral_plots(__name__, ...)

    # No overlaying here...
    if hasattr(fig, "objCount"): 
        msg = "Overlays of multi-panel `SpectralData` plots not supported"
        raise SPYError(msg)
        
    # Ensure panel-specification makes sense and is compatible w/averaging selection        
    if not isinstance(panels, str):
        raise SPYTypeError(panels, varname="panels", expected="str")
    if panels not in availablePanels:
        lgl = "'" + "or '".join(opt + "' " for opt in availablePanels)
        raise SPYValueError(legal=lgl, varname="panels", actual=panels)
    if (panels == "channels" and avg_channels) or (panels == "trials" and avg_trials) \
        or (panels == "tapers" and avg_tapers):
        msg = "Cannot use `panels = {}` and average across {} at the same time. "
        SPYWarning(msg.format(panels, panels))
        return

    # Ensure the proper amount of averaging was specified
    avgFlags = [avg_channels, avg_trials, avg_tapers]
    if sum(avgFlags) == 0 and nTap * nTrials > 1:
        msg = "Need to average across at least one of tapers, channels or trials " +\
            "for visualization. "
        SPYWarning(msg)
        return
    if sum(avgFlags) == 3:
        msg = "Averaging across trials, channels and tapers results in " +\
            "single-panel plot. Please use `singlepanelplot` instead"
        SPYWarning(msg)
        return
    if isTimeFrequency:
        if sum(avgFlags) != 2:
            msg = "Multi-panel time-frequency visualization requires averaging across " +\
                "two out of three dimensions (tapers, channels trials)"
            SPYWarning(msg)
            return
        
    # Prepare figure (same for all cases)
    if panels == "channels":
        npanels = nChan
    elif panels == "trials":
        npanels = nTrials
    else:   # ``panels == "tapers"``
        npanels = nTap
    
    # Construct subplot panel layout or vet provided layout
    # FIXME: fix, ax_arr, cax = setup_figure(npanels, nrow, ncol, include_colorbar=True, sharex=None, sharey=None)
    nrow, ncol = layout_subplot_panels(npanels, 
                                       nrow=kwargs.get("nrow", None), 
                                       ncol=kwargs.get("ncol", None))
    if not isTimeFrequency:
        (fig, ax_arr) = plt.subplots(nrow, ncol, constrained_layout=False,
                                     gridspec_kw={"wspace": 0, "hspace": 0.35,
                                                  "left": 0.05, "right": 0.97},
                                     figsize=pltConfig["multiFigSize"],
                                     sharex=True, sharey=True, squeeze=False)
    else:
        (fig, ax_arr) = plt.subplots(nrow, ncol, constrained_layout=False,
                                     gridspec_kw={"wspace": 0, "hspace": 0.35,
                                                  "left": 0.05, "right": 0.94},
                                     figsize=pltConfig["multiFigSize"],
                                     sharex=True, sharey=True, squeeze=False)
        gs = fig.add_gridspec(nrows=nrow, ncols=1, left=0.945, right=0.955)
        cax = fig.add_subplot(gs[:, 0])
        cax.tick_params(axis="both", labelsize=pltConfig["multiTickSize"])

    # Show xlabel only on bottom row of panels
    if isTimeFrequency:
        xLabel = "Time [s]"
        yLabel = "Frequency [Hz]"
    else:
        xLabel = "Frequency [Hz]"
        yLabel = dataLbl.replace(" [dB]", "")
    for col in range(ncol):
        ax_arr[-1, col].set_xlabel(xLabel, size=pltConfig["multiLabelSize"])
        
    # Omit first x-tick in all panels except first panel-row, show ylabel only 
    # on left border of first panel column
    for row in range(nrow):
        for col in range(1, ncol):
            ax_arr[row, col].xaxis.get_major_locator().set_params(prune="lower")
        ax_arr[row, 0].set_ylabel(yLabel, size=pltConfig["multiLabelSize"])
                
    # Flatten axis array to make counting a little easier in here and make
    # any surplus panels as unobtrusive as possible
    ax_arr = ax_arr.flatten(order="C")
    for ax in ax_arr:
        ax.tick_params(axis="both", labelsize=pltConfig["multiTickSize"])
        ax.autoscale(enable=True, axis="x", tight=True)
    for k in range(npanels, nrow * ncol):
        ax_arr[k].set_xticks([])
        ax_arr[k].set_yticks([])
        ax_arr[k].set_xlabel("")
        for spine in ax_arr[k].spines.values():
            spine.set_visible(False)
    ax_arr[min(npanels, nrow * ncol - 1)].spines["left"].set_visible(True)
    
    # Monkey-patch object-counter to newly created figure
    fig.isSpectralPlot = True
    fig.multipanelplot = True
    fig.objCount = 0

    # Start with the "simple" case: "regular" spectra, no time involved
    if not isTimeFrequency:

        # We're not dealing w/TF data here
        nTime = 1
        N = 1

        # For each panel stratification, set corresponding positional and 
        # keyword args for iteratively calling `_compute_pltArr`        
        if panels == "channels":
            
            panelVar = "channel"
            panelValues = chArr
            panelTitles = chArr
            
            if not avg_trials and avg_tapers:
                avgDim1 = "taper"
                avgDim2 = None
                innerVar = "trial"
                innerValues = trList
                majorTitle = "{} trials averaged across {} tapers".format(nTrials, nTap)
                showLegend = True
            elif avg_trials and not avg_tapers:
                avgDim1 = None
                avgDim2 = None
                innerVar = "taper"
                innerValues = tpArr
                majorTitle = "{} tapers averaged across {} trials".format(nTap, nTrials)
                showLegend = True
            else:   # `avg_trials` and `avg_tapers`
                avgDim1 = "taper"
                avgDim2 = None
                innerVar = "trial"
                innerValues = ["all"]
                majorTitle = " Average of {} tapers and {} trials".format(nTap, nTrials)
                showLegend = False
        
        elif panels == "trials":
            
            panelVar = "trial"
            panelValues = trList
            panelTitles = ["Trial #{}".format(trlno) for trlno in trList]
            
            if not avg_channels and avg_tapers:
                avgDim1 = "taper"
                avgDim2 = None
                innerVar = "channel"
                innerValues = chArr
                majorTitle = "{} channels averaged across {} tapers".format(nChan, nTap)
                showLegend = True
            elif avg_channels and not avg_tapers:
                avgDim1 = "channel"
                avgDim2 = None
                innerVar = "taper"
                innerValues = tpArr
                majorTitle = "{} tapers averaged across {} channels".format(nTap, nChan)
                showLegend = True
            else:   # `avg_channels` and `avg_tapers`
                avgDim1 = "taper"
                avgDim2 = "channel"
                innerVar = "trial"
                innerValues = ["all"]
                majorTitle = " Average of {} channels and {} tapers".format(nChan, nTap)
                showLegend = False
                    
        else:  # panels = "tapers"
            
            panelVar = "taper"
            panelValues = tpArr
            panelTitles = ["Taper #{}".format(tpno) for tpno in tpArr]
            
            if not avg_trials and avg_channels:
                avgDim1 = "channel"
                avgDim2 = None
                innerVar = "trial"
                innerValues = trList
                majorTitle = "{} trials averaged across {} channels".format(nTrials, nChan)
                showLegend = True
            elif avg_trials and not avg_channels:
                avgDim1 = None
                avgDim2 = None
                innerVar = "channel"
                innerValues = chArr
                majorTitle = "{} channels averaged across {} trials".format(nChan, nTrials)
                showLegend = True
            else:   # `avg_trials` and `avg_channels`
                avgDim1 = "channel"
                avgDim2 = None
                innerVar = "trial"
                innerValues = ["all"]
                majorTitle = " Average of {} channels and {} trials".format(nChan, nTrials)
                showLegend = False

        # Loop over panels, within each panel, loop over `innerValues` to (potentially)
        # plot multiple spectra per panel        
        kwargs = {"avg1": avgDim1, "avg2": avgDim2}
        for panelCount, panelVal in enumerate(panelValues):
            kwargs[panelVar] = panelVal
            for innerVal in innerValues:
                kwargs[innerVar] = innerVal
                pltArr = _compute_pltArr(self, nFreq, N, nTime, complexConversion, pltDtype, **kwargs)
                ax_arr[panelCount].plot(freqArr, np.log10(pltArr), 
                                        label=innerVar.capitalize() + " " + str(innerVal))
            ax_arr[panelCount].set_title(panelTitles[panelCount], size=pltConfig["multiTitleSize"])
            if grid is not None:
                ax_arr[panelCount].grid(grid)
        if showLegend:
            handles, labels = ax_arr[0].get_legend_handles_labels()
            ax_arr[0].legend(handles, labels)
        if title is None:
            fig.suptitle(majorTitle, size=pltConfig["singleTitleSize"])

    # Now, multi-panel time-frequency visualizations
    else:
        
        # Compute (and verify) length of selected time intervals
        tLengths = _compute_toilim_avg(self)
        nTime = tLengths[0]
        time = self.time[trList[0]][self._selection.time[0]]
        N = 1
        
        if panels == "channels":
            panelVar = "channel"
            panelValues = chArr
            panelTitles = chArr
            majorTitle = " Average of {} tapers and {} trials".format(nTap, nTrials)
            avgDim1 = "taper"
            avgDim2 = None
            
        elif panels == "trials":
            panelVar = "trial"
            panelValues = trList
            panelTitles = ["Trial #{}".format(trlno) for trlno in trList]
            majorTitle = " Average of {} channels and {} tapers".format(nChan, nTap)
            avgDim1 = "taper"
            avgDim2 = "channel"

        else:  # panels = "tapers"
            panelVar = "taper"
            panelValues = tpArr
            panelTitles = ["Taper #{}".format(tpno) for tpno in tpArr]
            majorTitle = " Average of {} channels and {} trials".format(nChan, nTrials)
            avgDim1 = "channel"
            avgDim2 = None

        # Loop over panels, within each panel, loop over `innerValues` to (potentially)
        # plot multiple spectra per panel        
        kwargs = {"avg1": avgDim1, "avg2": avgDim2}
        vmins = []
        vmaxs = []
        for panelCount, panelVal in enumerate(panelValues):
            kwargs[panelVar] = panelVal
            pltArr = _compute_pltArr(self, nFreq, N, nTime, complexConversion, pltDtype, **kwargs)
            vmins.append(pltArr.min())
            vmaxs.append(pltArr.max())
            ax_arr[panelCount].imshow(pltArr, origin="lower", interpolation=interp, cmap=cmap, 
                                      extent=(time[0], time[-1], freqArr[0], freqArr[-1]), 
                                      aspect="auto")
            ax_arr[panelCount].set_title(panelTitles[panelCount], size=pltConfig["multiTitleSize"])
            if grid is not None:
                ax_arr[panelCount].grid(grid)
                
        norm = colors.Normalize(vmin=min(vmins), vmax=max(vmaxs))
        for k in range(npanels):
            ax_arr[k].images[0].set_norm(norm)
        cbar = fig.colorbar(ax_arr[0].images[0], cax=cax)
        cbar.set_label(dataLbl, size=pltConfig["multiLabelSize"])
        cbar.outline.set_visible(False)
        if title is None:
            fig.suptitle(majorTitle, size=pltConfig["singleTitleSize"])

    # Increment overlay-counter and draw figure
    fig.objCount += 1
    plt.draw()
    self._selection = None
    return fig
    
def _compute_pltArr(self, nFreq, N, nTime, complexConversion, pltDtype,
                    avg1="channel", avg2=None, trial="all", channel="all", 
                    freq="all", taper="all"):
    """
    Local helper
    
    N = nChan, nTap or 1
    
    trial, channel, freq and taper have to be single-entity identifiers! 
    """
    
    # Prepare indexing list respecting potential non-default `dimord`s
    idx = [slice(None), slice(None), slice(None), slice(None)]
    timeIdx = self.dimord.index("time")
    chanIdx = self.dimord.index("channel")
    freqIdx = self.dimord.index("freq")
    taperIdx = self.dimord.index("taper")
    
    if trial == "all":
        trList = self._selection.trials
    else:
        trList = [trial]
    nTrls = len(trList)
    useFancy = self._selection._useFancy
    if channel == "all":
        idx[chanIdx] = self._selection.channel
    else:
        idx[chanIdx] = np.where(self.channel == channel)[0]
        useFancy = True
    if freq ==  "all":       
        idx[freqIdx] = self._selection.freq
    else:
        idx[freqIdx] = np.where(self.freq == freq)[0]
        useFancy = True
    if taper == "all":
        idx[taperIdx] = self._selection.taper
    else:
        idx[taperIdx] = [taper]
        useFancy = True
        
    if nTime == 1:
        pltArr = np.zeros((nFreq, N), dtype=pltDtype).squeeze()         # `squeeze` in case `N = 1`
    else:
        pltArr = np.zeros((nFreq, nTime, N), dtype=pltDtype).squeeze()  # `squeeze` for `singlepanelplot`

    for trlno in trList:
        trlArr = complexConversion(self._get_trial(trlno))
        if not useFancy:
            trlArr = trlArr[tuple(idx)]
        else:
            trlArr = trlArr[idx[0], ...][:, idx[1], ...][:, :, idx[2], :][..., idx[3]]
        if avg1:
            trlArr = trlArr.mean(axis=self.dimord.index(avg1), keepdims=True)
        if avg2:
            trlArr = trlArr.mean(axis=self.dimord.index(avg2), keepdims=True)
        pltArr += np.swapaxes(trlArr, freqIdx, 0).squeeze()
    return pltArr / len(trList)


def _prep_spectral_plots(self, name, **inputArgs):
    """
    Local helper
    """
    
    # Abort if matplotlib is not available
    if not __plt__:
        raise SPYError(pltErrMsg.format(name))
    
    # Ensure our binary flags are actually binary
    if not isinstance(inputArgs["avg_channels"], bool):
        raise SPYTypeError(inputArgs["avg_channels"], varname="avg_channels", expected="bool")
    if not isinstance(inputArgs["avg_tapers"], bool):
        raise SPYTypeError(inputArgs["avg_tapers"], varname="avg_tapers", expected="bool")
    if not isinstance(inputArgs.get("avg_trials", True), bool):
        raise SPYTypeError(inputArgs["avg_trials"], varname="avg_trials", expected="bool")
    
    # Pass provided selections on to `Selector` class which performs error 
    # checking and generates required indexing arrays
    self._selection = {"trials": inputArgs["trials"], 
                       "channels": inputArgs["channels"], 
                       "tapers": inputArgs["tapers"],
                       "toilim": inputArgs["toilim"],
                       "foilim": inputArgs["foilim"]}
    
    # Ensure any optional keywords controlling plotting appearance make sense
    if inputArgs["title"] is not None:
        if not isinstance(inputArgs["title"], str):
            raise SPYTypeError(inputArgs["title"], varname="title", expected="str")
    if inputArgs["grid"] is not None:
        if not isinstance(inputArgs["grid"], bool):
            raise SPYTypeError(inputArgs["grid"], varname="grid", expected="bool")

    # Get trial/channel/taper count
    trList = self._selection.trials
    nTrials = len(trList)
    chArr = self.channel[self._selection.channel]
    nChan = chArr.size
    freqArr = self.freq[self._selection.freq]
    nFreq = freqArr.size
    tpArr = np.arange(self.taper.size)[self._selection.taper]
    nTap = tpArr.size
    
    dimCounts = (nTrials, nChan, nFreq, nTap)
    dimArrs = (trList, chArr, freqArr, tpArr)

    # Determine whether we're dealing w/tf data
    isTimeFrequency = False
    if any([t.size > 1 for t in self.time]):
        isTimeFrequency = True
        
    # Ensure provided min/max range for plotting TF data makes sense
    vminmax = False
    if inputArgs["vmin"] is not None:
        try:
            scalar_parser(inputArgs["vmin"], varname="vmin")
        except Exception as exc:
            raise exc 
        vminmax = True
    if inputArgs["vmax"] is not None:
        try:
            scalar_parser(inputArgs["vmax"], varname="vmax")
        except Exception as exc:
            raise exc 
        vminmax = True
    if inputArgs["vmin"] is not None and inputArgs["vmax"] is not None:
        if inputArgs["vmin"] >= inputArgs["vmax"]:
            lgl = "minimal data range bound to be less than provided maximum "
            act = "vmax < vmin"
            raise SPYValueError(legal=lgl, varname="vmin/vamx", actual=act)
    if vminmax and not isTimeFrequency:
        msg = "`vmin` and `vmax` is only used for time-frequency visualizations"
        SPYWarning(msg)
        
    # Check for complex entries in data and set datatype for plotting arrays 
    # constructed below (always use floats w/same precision as data)
    if "complex" in self.data.dtype.name:
        msg = "Found complex Fourier coefficients - visualization will use absolute values."
        SPYWarning(msg)
        complexConversion = lambda x: np.absolute(x).real
        pltDtype = "f{}".format(self.data.dtype.itemsize)
        dataLbl = "Absolute Frequency [dB]"
    else:
        complexConversion = lambda x: x
        pltDtype = self.data.dtype
        dataLbl = "Power [dB]"
    
    return dimArrs, dimCounts, isTimeFrequency, complexConversion, pltDtype, dataLbl
