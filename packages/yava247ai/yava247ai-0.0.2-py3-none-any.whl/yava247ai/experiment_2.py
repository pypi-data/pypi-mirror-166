import sys
import subprocess
import os

import sklearn
import tensorflow as tf
import mlflow
import mlflow.tensorflow
import mlflow.sklearn

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

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

'''    
def log_artifacts(local_dir):
    return mlflow.log_artifacts(local_dir)
'''        
     
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='mlflow wrapper for yava247ai.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2', help="show library version number.")
    
    subparsers = parser.add_subparsers(title='functions', description='training library', help='set_experiment_uri("http://localhost:1234", "<NOTEBOOKID>", "<training_library>")')
    subparsers.add_parser('tensorflow')
    subparsers.add_parser('sklearn')
    args = parser.parse_args()
    print("args:", args)