'''
If package is to be run. This will scale the service until terminated.
'''

from auto_scaler import AutoScaler

def main():
    WEBAUTOSCALER = AutoScaler(
        image_name="erihanase/php-web:latest",
        service_name="php-web-service",
        placement_constraints=['node.role==worker']
    )



if __name__ == "__main__":
    main()