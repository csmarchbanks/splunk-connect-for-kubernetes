# Prerequsite - Python should be installed and its version must be > 3.x

# Testing Instructions
0. (Optional) Use a virtual environment for the test  
    `virtualenv --python=python3.6 venv`  
    `source venv/bin/activate`
1. Install the dependencies  
    `pip install -r requirements.txt`  
2. Start the test with the required options configured
    `python deploy_data_gen.py <options>`

    **Options are:**
    --message_count
    * Description: Message CountNamespace where the deployment is to be created
    * Default: 1000000

    --output_stdout
    * Description: Should we output logs to stdout inside datagen
    * Default: true

    --message_size
    * Description: Message Size
    * Default: 256

    --eps
    * Description: Events per second output
    * Default: 1000

    --namespace
    * Description: Namespace where the deployment is to be created
    * Default: default

    --number_of_replicas
    * Description: Number of datagen to be deployed
    * Default: 1

    --deployment_name
    * Description: Name of the deployment
    * Default: kafkadatagen-deployment

    --k8s_object_name
    * Description: Name of the k8s object
    * Default: kafkadatagen

    --container_name
    * Description: Name of the container
    * Default: kafkadatagen

    --image_path
    * Description: Full path of the image to be used
    * Default: chaitanyaphalak/kafkadatagen:1.0-4-gca7f6d8

    --create_deployment
    * Description: Specify whether the script should create deployment
    * Default: true

    --delete_deployment
    * Description: Specify whether the script should delete deployment
    * Default: false
