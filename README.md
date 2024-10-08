# neuromorpho_downloader
This is a downloading tool intended to download neuron metadata and swc files from [Neuromorpho.org](https://neuromorpho.org/). This is one of the easiest tools to use to download neuron morphology data.

## Installation
Were you expecting insane installation guides? Well, all you need for this is python>3.7

## Usage
Use the following command for running the tool.

```
python download.py --data_root=./home --archive=Jacobs --species=Baboon --fetch --download
```

1. ```data_root```: Define data download location. If you want the same directory as the repository, ommit the parameter.
2. ```archive```: Specify archive name. Make sure they are as in [Neuromorpho.org](https://neuromorpho.org/).
3. ```species```: Specify species name. Make sure they are as in [Neuromorpho.org](https://neuromorpho.org/).
4. ```fetch```: Use this to download metadata. Ommit if you already have metadata.
5. ```download```: Use this to download swc files. Ommit if not using code for download.

## Acknowledgement
The tool was developed with the help of [Neuromorpho.org](https://neuromorpho.org/) and their admins. Please use the following citation:

```
@article{ascoli2007neuromorpho,
  title={NeuroMorpho. Org: a central resource for neuronal morphologies},
  author={Ascoli, Giorgio A and Donohue, Duncan E and Halavi, Maryam},
  journal={Journal of Neuroscience},
  volume={27},
  number={35},
  pages={9247--9251},
  year={2007},
  publisher={Soc Neuroscience}
}
```

to credit the original creators for using their database. Consult their webpage for more details as to the origin of the specific neuron files. Please contact [nmadmin@gmu.edu](nmadmin@gmu.edu) in case of any issues with their website and consult [API](https://neuromorpho.org/apiReference.html) for a complete guide on using their API. Please credit the tool in case it helps you in your research or any kind of project whatsoever using the following:

```
@misc{Bhattacharya2024,
  author = {Bhattacharya, Rajarshi},
  title = {Neuromorpho Data Downloading Tool},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/rB080/neuromorpho_downloader.git}}
}
```
