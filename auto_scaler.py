'''
Module auto_scaler
'''

import docker
import time
import urllib2


CONTAINER_CAPACITY = 5
'''
How many connections per second each container can handle.
'''

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

    def get_connection_rate(self):
        '''
        Gets HAproxy stats. The 3rd from the call to the stat page returns
        http-in frontend stats, and the 47th column contains HTTP requests per
        second over last elapsed second (req_rate)
        See https://cbonte.github.io/haproxy-dconv/1.6/management.html#9.1 for
        more information.
        '''
        fd = urllib2.urlopen('http://localhost:7000/haproxy?stats;csv')
        conn_rate = fd.read().split('\n')[3].split(',')[47] # <- ???
        return conn_rate

    def run_auto_scaler(self, poll_interval=10):
        '''
        Runs the auto-scaler until the program is stopped. The auto-scaler
        updates every @poll_interval seconds.
        '''
        desired_replica_count = 1
        while True:
        # Calculate desired value
            # Get current load
            connection_rate = self.get_connection_rate()
            # Set desired_replica_count
            desired_replica_count = (connection_rate / CONTAINER_CAPACITY) + 1
            # Do scaling
            scale_service(desired_replica_count)
            time.sleep(poll_interval)


