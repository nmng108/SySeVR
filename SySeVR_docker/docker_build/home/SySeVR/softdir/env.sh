#!/bin/bash
source /etc/profile
cd /home/SySeVR/joern-0.3.1
ant
ant tools #optional
echo "alias joern='java -jar $JOERN_HOME/bin/joern.jar'" >> ~/.bashrc
source ~/.bashrc
echo "source /etc/profile" >> ~/.bashrc

# Set up java command: 
update-alternatives --install "/usr/bin/java" "java" "/usr/java/jdk1.8.0_161/bin/java" 1
update-alternatives --install "/usr/bin/javac" "javac" "/usr/java/jdk1.8.0_161/bin/javac" 1
update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/java/jdk1.8.0_161/bin/javaws" 1
# && update-alternatives --set java /usr/local/java/jdk1.8.0_161/bin/java \
# && update-alternatives --set javac /usr/local/java/jdk1.8.0_161/bin/javac \
# && update-alternatives --set javaws /usr/local/java/jdk1.8.0_161/bin/javaws
# Due to the only version installed on this image, we don't need to run the 3 commented commands above

