import sys
import subprocess
import os
#from subprocess import PIPE
#import pyarrow as pa
#import pyarrow.parquet as pq
#cmd = ["locate", "-l", "1", "libhdfs.so"]
#libhdfsso_path = subprocess.Popen(cmd, stdout=PIPE).stdout.read().rstrip()
os.environ["ARROW_LIBHDFS_DIR"] = "/usr/yava/3.0.0.0-0000/hadoop/lib/native/"
#cmd = ["/usr/bin/hdfs", "classpath", "--glob"]
#hadoop_cp = subprocess.Popen(cmd, stdout=PIPE).stdout.read().rstrip()
#os.environ["CLASSPATH"] = hadoop_cp.decode("utf-8")
#os.environ["HADOOP_USER_NAME"] = "hdfs"
#nameNodeHost = 'vm02gpu.solusi247.com'
#nameNodeIPCPort = 8020

import sklearn
import tensorflow as tf
#from tensorflow import keras
import mlflow.tensorflow
import mlflow.sklearn

def set_experiment_uri(uri, experiment_name, method):
    if method == 'tensorflow':
        mlflow.set_tracking_uri(uri)
        mlflow.tensorflow.autolog()
        mlflow.set_experiment(experiment_name)
    elif method == 'sklearn':
        mlflow.set_tracking_uri(uri)
        mlflow.sklearn.autolog()
        mlflow.set_experiment(experiment_name)
    else:
        print("Please fill method parameter: 'tensorflow' or 'sklearn'")
        print('example: set_experiment_uri("http://localhost:1234", "NOTEBOOKID", "tensorflow")')
        
def log_artifact(local_path):
    return mlflow.log_artifact(local_path)
    
def log_artifacts(local_dir):
    return mlflow.log_artifacts(local_dir)
        
if __name__ == "__main__":
    print("this is wrapper")