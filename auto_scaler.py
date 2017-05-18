'''
Module auto_scaler
'''

import docker

class AutoScaler(object):
    '''
    Contains properties and methods necessary for scaling a service in Docker.
    '''
    def __init__(self, image_name, service_name, placement_constraints):
        self.image_name = image_name
        self.service_name = service_name
        self.placement_constraints = placement_constraints
        self.client = docker.from_env()

    def get_service(self, service_name):
        '''
        Returns the service this @AutoScaler runs for.
        '''
        return self.client.services.list(
            filters={'name':service_name}
        )[0]

    def scale_service(self, new_service_replica_count):
        '''
        Scales the service so that the service has @new_service_replica_count
        amount of containers.
        '''
        service = self.get_service(self.service_name)
        service.update(
            image=self.image_name,
            name=self.service_name,
            constraints=self.placement_constraints,
            mode={'replicated':{'replicas':new_service_replica_count}}
        )

    def run_auto_scaler(self, func, poll_interval=10):
        '''
        Runs the auto-scaler until the program is stopped. The auto-scaler
        updates every @poll_interval seconds.
        '''
        func()
        while True:
            pass
