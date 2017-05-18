'''
Package auto_scaler
'''

from . import AutoScaler

__all__ = ['auto_scaler']


# if __name__ == "__main__":
#     # Create service
#     WEBAUTOSCALER = AutoScaler(
#         image_name="erihanase/php-web:latest",
#         service_name="php-web-service",
#         placement_constraints=['node.role==worker']
#     )
