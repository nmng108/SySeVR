# SySeVR docker image instructions

*Reminder: the device needs nvdia graphics card support, and docker and nvidia-docker2 have been installed in Linux system*

```bash
# You may copy Implementation and Program data(will be changed to 'data') folders to another location
mkdir [Target Dir]/SySeVR
cp -r [Source Dir]/SySeVR/Implementation [Target Dir]/SySeVR/Implementation
cp -r [Source Dir]/SySeVR/Program data  [Target Dir]/SySeVR/data
```


## 0) Pull (and run) image

If doing this step, we will ignore the step 1 & 2.
We can either execute (to pull and run):

```bash
docker run -itd --gpus all -p 7474:7474 --name=sysevr -v [Target Dir]/Implementation:/home/SySeVR/Implementation -v [Target Dir]/data:/home/SySeVR/data nmng108/sysevr:v1.0 /bin/bash
```

or (to pull image):

```bash
docker pull nmng108/sysevr:v1.0
```


## 1) Build image

The docker_build folder is the working folder where the image is created.

Enter docker_ Build folder, execute command:

```bash
docker build -t sysevr:v1.0 .
```

"sysevr: v1.0" is the name of the created image.


## 2) Run container

execute command:

```bash
docker run -itd --gpus all --name=sysevr -v [Target Dir]/Implementation:/home/SySeVR/Implementation -v [Target Dir]/data:/home/SySeVR/data sysevr:v1.0 /bin/bash
```
in which [Target Dir] is the directory in your host OS that contains 2 project's directories above. 

E.g: 

```bash 
docker run -it --gpus all --name=sysevr \
-v /home/[user]/coding/projects/SySeVR/Implementation:/home/SySeVR/Implementation \
-v /home/[user]/coding/projects/SySeVR/data:/home/SySeVR/data nmng108/sysevr:v1.0 /bin/bash
```
Explanation:

"--name=sysevr",sysevr is the container name.

"sysevr:v1.0" is the image name obtained in the previous step.

"-v source:target" : create anonymous volume, map source code and data folders to container's project directory.

"-gpus all" option is available only for machines that exist external graphic cards.


After entering the container, the folders of Joern and neo4j software required by sysevr are under the path of / home/sysevr.

Other required dependencies have been installed and configured.


## 3) Then open container's shell and run the following commands: (Done, ignore this step)

```bash
rm -rf /usr/local/lib/python3.5/dist-packages/certifi
python3 -m pip uninstall requests
python3 -m pip install requests==2.19.0   # This reinstalls certifi-2022.6.15-py3-none-any.whl which breaks in python 3.5
rm -rf /home/ssm-user/.local/lib/python3.5/site-packages/certifi
python3 -m pip install certifi==2021.10.8
python3 -m pip install pyyaml
```
where ``python3 -m pip`` may be replaced by ``pip`` or ``pip3``.


## 4) Install text editor like nano first (Done - ignore this step)

`` apt-get install -y nano ``

Edit ~/.bashrc file: 
```bash
alias joern='java -jar $JOERN_HOME/bin/joern.jar' (may be already correct)

source /etc/profile
```


## 5) Install joern-tools: (May ignore this step if those packages are installed from Dockerfile)

```bash
pip2 install chardet==3.0.4 \
&& pip2 install pygraphviz==1.5

git clone https://github.com/fabsx00/joern-tools /home/SySeVR
cd /home/SySeVR/joern-tools \
&& python2 setup.py install
```

## Notes:

- Removed pip-9.0.1 and updated to 20.3.4
