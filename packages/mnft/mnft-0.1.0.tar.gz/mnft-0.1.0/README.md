# NFT-Pytorch-Callback

Generously supported by the Algovera Community. See more details [here](https://forum.algovera.ai/t/proposal-pytorch-nft-checkpoint/100).

A custom pytorch NFT-checkpoint that hashes the current network weights, some metadata (data, accuracy, etc…) and your eth address (could be turned into some kind of standard later) every N epoch, which proves who did the network training.

This NFT could represent a tradable license of some sort for example.

### MINT

Take your hash and mint your model NFT at `m-nft.com`

### Installation

```
pip3 install nftc
```

**Description of the project and what problem is it solving**: Trying to determine who actually did the training of a machine learning model is currently very hard. Looking at open-source model zoos today it is nearly impossible to determine who trained which model. The Pytorch NFT checkpoint solves this problem.

A custom NFT is generated each epoch, which proves who generated which network weights. This could be used as a badge of honor or turned into a tradable license.

You can also watch me presenting the idea in the video below (timestamp 1:34).


<a href="http://www.youtube.com/watch?feature=player_embedded&v=Avs9NMRBvJk
" target="_blank"><img src="http://img.youtube.com/vi/Avs9NMRBvJk/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
