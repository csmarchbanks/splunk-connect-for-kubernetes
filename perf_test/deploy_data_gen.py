#!/usr/bin/python
import argparse
import collections
import logging
from kubernetes import client, config
from kubernetes.client.rest import ApiException


logging.basicConfig(level=logging.INFO)


KubernetesDeploymentParams = collections.namedtuple(
    'KubernetesDeploymentParams',
    ['message_count', 'message_size', 'output_stdout', 'eps',
     'namespace', 'number_of_replicas', 'deployment_name', 'k8s_object_name',
     'container_name', 'image_path', 'create_deployment', 'delete_deployment'])


class KubernetesDeployment(object):
    ''' Kubernetes Deployment class
    This class is used to create and delete kafka data gen deployments in kubernetes
    '''
    def __init__(self, config):
        self.message_count = config.message_count
        self.message_size = config.message_size
        self.output_stdout = config.output_stdout
        self.eps = config.eps
        self.namespace = config.namespace
        self.number_of_replicas = config.number_of_replicas
        self.deployment_name = config.deployment_name
        self.k8s_object_name = config.k8s_object_name
        self.container_name = config.container_name
        self.image_path = config.image_path
        self.create_deployment = config.create_deployment
        self.delete_deployment = config.delete_deployment


    def _create_deployment_object(self):
       '''
       Function to create kafka data gen deployment object
       '''
       # Configure Pod template container
       container = client.V1Container(
          name=str(self.container_name),
          image=str(self.image_path),
          command=["java"],
          args=["-jar", "kafka-data-gen.jar", "-message-count", str(self.message_count), "-message-size", str(self.message_size),
                "-output-stdout", str(self.output_stdout), "-eps", str(self.eps)])
       # Create and configurate a spec section
       template = client.V1PodTemplateSpec(
          metadata=client.V1ObjectMeta(labels={"app": str(self.k8s_object_name)}),
          spec=client.V1PodSpec(containers=[container]))
       # Create the specification of deployment
       spec = client.ExtensionsV1beta1DeploymentSpec(
          replicas=int(self.number_of_replicas),
          template=template)
       # Instantiate the deployment object
       self.deployment = client.ExtensionsV1beta1Deployment(
          api_version="extensions/v1beta1",
          kind="Deployment",
          metadata=client.V1ObjectMeta(name=str(self.deployment_name)),
          spec=spec)


    def _create_deployment(self, api_instance):
       '''
       Function to create kafka data gen deployment in kubernetes
       @param: api_instance
            api instance in the reference to the kubernetes extensions_v1beta1 api
       '''
       api_response = None
       try:
          api_response = api_instance.create_namespaced_deployment(
             body=self.deployment,
             namespace=self.namespace)
       except ApiException as e:
           logging.getLogger().info("Deployment could not be created: {0}".format(e))

       if api_response:
           logging.getLogger().info("Deployment created. status={0}".format(str(api_response.status)))


    def _delete_deployment(self, api_instance):
       '''
       Function to delete kafka data gen deployment in kubernetes
       @param: api_instance
            api instance in the reference to the kubernetes extensions_v1beta1 api
       '''
       api_response = None
       try:
          api_response = api_instance.delete_namespaced_deployment(
             name=str(self.deployment_name),
             namespace=str(self.namespace),
             body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
       except ApiException as e:
           logging.getLogger().info("Deployment could not be deleted: {0}".format(e))

       if api_response:
           logging.getLogger().info("Deployment deleted. status={0}".format(str(api_response.status)))


    def run(self):
        '''
        Function to run steps for creation/deletion of kafka data gen deployment
        '''
        extensions_v1beta1 = None
        try:
            # Initialize kubernetes python client
            config.load_kube_config()
            extensions_v1beta1 = client.ExtensionsV1beta1Api()
        except ApiException as e:
            logging.getLogger().info("Could not load kubeconfig or get "
                                     "access to extensions_v1beta1 kubernetes API : {0}".format(e))

        if self.create_deployment == "true":
           self._create_deployment_object()
           self._create_deployment(extensions_v1beta1)
        if self.delete_deployment == "true":
           self._delete_deployment(extensions_v1beta1)

        logging.getLogger().info("Finished creating/deleting kafka data gen deployment")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--message_count',default=1000000, required=False,
                        help='Message count')
    parser.add_argument('--message_size', default=256, required=False,
                        help='Message size')
    parser.add_argument('--output_stdout', default='true', required=False,
                        help='Should we output logs to stdout inside datagen')
    parser.add_argument('--eps', default=1000, required=False,
                        help='Events per second output')
    parser.add_argument('--namespace', default="default", required=False,
                        help='Namespace where the deployment is to be created')
    parser.add_argument('--number_of_replicas', default=1, required=False,
                        help='Number of datagen to be deployed')
    parser.add_argument('--deployment_name', default="kafkadatagen-deployment", required=False,
                        help='Name of the deployment')
    parser.add_argument('--k8s_object_name', default="kafkadatagen", required=False,
                        help='Name of the k8s object')
    parser.add_argument('--container_name', default="kafkadatagen", required=False,
                        help='Name of the container')
    parser.add_argument('--image_path', default="chaitanyaphalak/kafkadatagen:1.0-4-gca7f6d8", required=False,
                        help='Full path of the image to be used')
    parser.add_argument('--create_deployment', default="true", required=False,
                        help='Specify whether the script should create deployment')
    parser.add_argument('--delete_deployment', default="false", required=False,
                        help='Specify whether the script should delete deployment')

    args = parser.parse_args()
    deployment_manager = KubernetesDeployment(args)
    deployment_manager.run()


if __name__ == '__main__':
    main()
