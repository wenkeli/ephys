import os;

import matplotlib;
matplotlib.use("Qt4Agg");
import matplotlib.pyplot as pp;

from ..fileIO.loadOpenEphysSPikes import readSpikes;

from ..data.spikes import SpikesData;

    
fileName="/mnt/FastData/spikes_data/mCD__2014-05-01_16-07-49__acq9/Tetrode10.spikes";

file=open(fileName, "rb");

fileStat=os.stat(fileName);

fileSize=fileStat.st_size;

data=readSpike(file, fileSize, 1024, "=Bq3H", "H", "H", 2, "H", 3, 4);

file.close();

# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][0]["waveForm"][100000:101000, :].T);
# fig.show();
#   
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][1]["waveForm"][100000:101000, :].T);
# fig.show();
#   
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][2]["waveForm"][100000:101000, :].T);
# fig.show();
#   
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][3]["waveForm"][100000:101000, :].T);
# fig.show();


# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][0]["waveForm"][117545, :].T);
# fig.show();
#   
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][1]["waveForm"][117545, :].T);
# fig.show();
#   
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][2]["waveForm"][117545, :].T);
# fig.show();
#   
# fig=pp.figure(); ax=fig.add_axes([0.15, 0.15, 0.7, 0.7]);
# ax.plot(data["channels"][3]["waveForm"][117545, :].T);
# fig.show();

waveMaxBools=np.zeros(data["channels"][0]["gain"].shape, dtype="bool");
waveMaxIndBools=np.zeros(waveMaxBools.shape, dtype="bool");
waveCombBools=np.zeros(waveMaxBools.shape, dtype="bool");

for i in np.r_[0:4]:
    curMaxBools=(np.max(data["channels"][i]["waveForm"][:, 4:10], 1)>25);
    waveMaxBools=waveMaxBools | curMaxBools;
    
    maxInds=np.argmax(data["channels"][i]["waveForm"][:, 0:15], 1);
    curMaxIndBools=(maxInds>=7) & (maxInds<10);
    waveMaxIndBools=waveMaxIndBools | curMaxIndBools;
    waveCombBools=waveCombBools | (curMaxBools & curMaxIndBools);
    
    
print(str(np.sum(waveMaxBools)));
print(str(np.sum(waveMaxIndBools)));
print(str(np.sum(waveCombBools)));