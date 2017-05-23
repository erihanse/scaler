'''
Module auto_scaler
'''

import docker
import time
import urllib2
import logging
import sys
import csv

from StringIO import StringIO


CONTAINER_CAPACITY = 5
'''
How many connections per second each container can handle.
'''

class AutoScaler(object):
    '''
    Contains properties and methods necessary for scaling a service in Docker.
    Set loglevel=logging.INFO for logging to screen when running the auto
    scaler. We cannot put service as property of our AutoScaler, even though
    there is a 1:1 relationship between AutoScaler and docker.models.services.
     Service. This seems to be because the object changes whenever scaling is
    done.
    '''
    def __init__(
        self,
        image_name,
        service_name,
        placement_constraints,
        loglevel=logging.INFO
    ):
        self.image_name = image_name
        self.service_name = service_name
        self.placement_constraints = placement_constraints
        self.client = docker.from_env()

        logging.basicConfig(stream=sys.stderr, level=loglevel)


    def get_service(self):
        return self.client.services.list(
            filters={'name':self.service_name}
        )[0]

    def scale_service(self, new_service_replica_count):
        '''
        Scales the service so that the service has @new_service_replica_count
        amount of containers.
        '''
        self.get_service().update(
            image=self.image_name,
            name=self.service_name,
            constraints=self.placement_constraints,
            mode={'replicated':{'replicas':new_service_replica_count}}
        )

    def get_connection_rate(self):
        '''
        See https://cbonte.github.io/haproxy-dconv/1.6/management.html#9.1 for
        more information.
        '''
        # Originally did it this way, but prettier to use DictReader
        # conn_rate = fd.read().split('\n')[3].split(',')[46]

        # Start by getting stats from haproxy
        content = urllib2.urlopen('http://localhost:7000/haproxy?stats;csv')
        iocontent = StringIO(content)
        fieldnames = content.split('\n')[0].split(',')
        reader = csv.DictReader(iocontent, fieldnames)

        for row in reader:
            if 'http-in' in row['pxname']:
                return int(row['req_rate'])

    def run_auto_scaler(self, poll_interval=5):
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

            logging.info("connection_rate: " + str(connection_rate))
            logging.info("desired_replica_count: " + \
                str(desired_replica_count))
            # Do scaling

            self.scale_service(desired_replica_count)
            time.sleep(poll_interval)
