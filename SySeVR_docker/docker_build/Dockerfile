FROM tensorflow/tensorflow:1.6.0-devel-gpu-py3
COPY ./home/ /home/
RUN mkdir /usr/java \
&& cp -r /home/SySeVR/softdir/jdk1.8.0_161 /usr/java \
&& mkdir /usr/ant \
&& cp -r /home/SySeVR/softdir/apache-ant-1.9.14 /usr/ant \
&& rm -rf /etc/apt/sources.list \
&& cp -r /home/SySeVR/softdir/sources.list /etc/apt/ \
&& rm -rf /etc/apt/sources.list.d \
&& apt-get clean 
RUN apt-get update \
&& rm -rf /etc/profile \
&& cp -r /home/SySeVR/softdir/profile /etc \
&& cd /home/SySeVR/softdir \
&& chmod +x env.sh \
&& ./env.sh \
&& apt-get install -y python3 \
&& apt-get install -y python-setuptools \
&& apt-get install -y python-dev \
&& apt-get install -y python-pip \
&& cd /home/SySeVR/softdir/py2neo-py2neo-2.0 \
&& python2 setup.py install \
&& cd /home/SySeVR/softdir/python-joern-0.3.1 \
&& python2 setup.py install \
&& apt-get install -y graphviz \
&& apt-get install -y libgraphviz-dev \
&& apt-get install -y pkg-config \
&& apt-get install -y python-igraph \
&& apt-get install -y python-virtualenv \
&& pip3 install xlrd \
&& pip3 install gensim==3.4
RUN rm -rf /home/SySeVR/softdir
RUN apt-get install -y nano
# Install pyyaml package:
RUN rm -rf /usr/local/lib/python3.5/dist-packages/certifi \
&& python3 -m pip uninstall -y requests \
&& python3 -m pip install requests==2.19.0 \
&& rm -rf /home/ssm-user/.local/lib/python3.5/site-packages/certifi \
&& python3 -m pip install certifi==2021.10.8 \ 
&& pip3 install pyyaml
RUN pip3 install -U scikit-learn==0.22 \
&& pip3 install imbalanced-learn==0.6.2
# Install joern-tools
RUN pip2 install chardet==3.0.4 \
&& pip2 install pygraphviz==1.5 \
&& git clone https://github.com/fabsx00/joern-tools /home/SySeVR \
&& cd /home/SySeVR/joern-tools \
&& python2 setup.py install


