import os;

import matplotlib;
matplotlib.use("Qt4Agg");
import matplotlib.pyplot as pp;

from ..fileIO.loadOpenEphysSpikes import readSamples, readSpikeFile;

from ..data.samples import SamplesData;

import numpy as np;

    
# fileName="/mnt/FastData/spikes_data/mCD__2014-05-01_16-07-49__acq9/Tetrode10.spikes";
fileName="/mnt/FastData/spikes_data/test__2015-05-19_14-48-44__1/TT9.spikes";

file=open(fileName, "rb");

fileStat=os.stat(fileName);

fileSize=fileStat.st_size;

data=readSpikeFile(file, fileName);

file.close();

samples=SamplesData(data["waveforms"], data["gains"], data["thresholds"], 
                    data["timestamps"], data["samplingHz"], data["triggerChs"]);

# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["waveforms"][100000:101000, :].T);
# fig.show();

# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(spikes.waveforms[0, 0:10, :].T);
# fig.show();
# 
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(spikes.waveforms[1, 0:10, :].T);
# fig.show();
# 
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(spikes.waveforms[2, 0:10, :].T);
# fig.show();
# 
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(spikes.waveforms[3, 0:10, :].T);
# fig.show();

# spikeInds=np.r_[0:spikes.numSpikes];
# 
# rands=np.random.random(10);
# 
# failInds=spikeInds[spikes.triggerCh<0];
# randFailInds=failInds[np.int32(rands*failInds.size)];
# 
# succInds=spikeInds[spikes.triggerCh>=0];
# randSuccInds=succInds[np.int32(rands*succInds.size)];

# for i in randFailInds:
#     fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
#     ax.plot(spikes.waveforms[:, i, :].T);
#     fig.show();
# 
# for i in randSuccInds:
#     fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
#     pp.hold(True);
#     ax.plot(spikes.waveforms[:, i, :].T);
#     ax.plot(spikes.waveforms[spikes.triggerCh[i], i, :], color="k", linewidth=2);
#     pp.hold(False);
#     fig.show();
    
    
    