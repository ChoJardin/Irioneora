# JVM

ubuntu@ip-172-26-6-204 ~ $ java -version
openjdk version "1.8.0_292"
OpenJDK Runtime Environment (build 1.8.0_292-8u292-b10-0ubuntu1~20.04-b10)
OpenJDK 64-Bit Server VM (build 25.292-b10, mixed mode)



# Nginx

nginx   1.18.0-0ubuntu1.2



# Hadoop

core-site.xml

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://172.26.6.204:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hadoop/hadoop_tmp</value>
    </property>
</configuration>
```

hdfs-site.xml

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.rpc-bind-host</name>
        <value>0.0.0.0</value>
    </property>
        <property>
        <name>dfs.namenode.http-address</name>
        <value>0.0.0.0:50070</value>
        </property>
        <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>0.0.0.0:50090</value>
        </property>
        <property>
        <name>dfs.datanode.address</name>
        <value>0.0.0.0:50010</value>
        </property>
        <property>
        <name>dfs.datanode.http.address</name>
        <value>0.0.0.0:50075</value>
        </property>
        <property>
        <name>dfs.datanode.ipc.address</name>
        <value>0.0.0.0:50020</value>
        </property>
</configuration>
```

.bashrc

```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME="/usr/local/hadoop"
export PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"
```



#  Spark

version 3.1.2

[Spark Standalone Mode - Spark 3.1.2 Documentation (apache.org)](https://spark.apache.org/docs/latest/spark-standalone.html)



.bashrc

```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export SPARK_MASTER_WEBUI_PORT=8088
export SPARK_MASTER_IP=3.36.130.57
```



