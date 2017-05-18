'''
If package is to be run. This will scale the service until terminated.
'''

from auto_scaler import AutoScaler

def jalla():
    print "hei"

def main():
    webautoscaler = AutoScaler(
        image_name="erihanase/php-web:latest",
        service_name="php-web-service",
        placement_constraints=['node.role==worker']
    )

    webautoscaler.run_auto_scaler(jalla)



if __name__ == "__main__":
    main()