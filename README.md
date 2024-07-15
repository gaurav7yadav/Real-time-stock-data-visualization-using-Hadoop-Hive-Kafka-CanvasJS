# PathFinder
Step-1: start hadoop

.\start-dfs.cmd
./start-yarn.cmd
jps

Step-2: start kafka 
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties 
.\bin\windows\kafka-server-start.bat .\config\server.properties 

Step-3: start Hive 
StartNetworkServer -h 0.0.0.0
 hive --service  schematool -dbType derby -initSchema
 hive


Step-4: create folder
hdfs dfs -mkdir -p /user/hadoopuser

create .json file
hdfs dfs -touchz /user/hadoopuser/air_quality_data.json

check file 
hdfs dfs -cat /user/hadoopuser/air_quality_data.json


Step-5: Important Links to check Json file on Hadoop

http://localhost:9870/dfshealth.html
http://localhost:9864/datanode.html
http://localhost:8088/cluster

Step-6: start Index.html file to see the Output

All of these are present in Hadoop+hive+kafka+frontend-->Output folder# New
# try
