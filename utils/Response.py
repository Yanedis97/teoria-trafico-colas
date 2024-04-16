import json

class Response:
    
    @classmethod
    def error(cls, data = [],  message: str = 'Error del cliente'):
        data = {
            'statusCode': 400,
            'error': True,
            'data': data,
            'message': message,
        }
        return data

    @classmethod
    def success(cls, data: list = [], message: str = 'Petición exitosa', pagination: dict = {}):
        response = {
            'statusCode': 200,
            'data': data,
            'message': message
        }
        if pagination:
            response['pagination'] = pagination
        return response
    
    @classmethod
    def not_found(cls, message: str = 'Recurso no encontrado'):
        data = {
            'statusCode': 404,
            'error': True,
            'data': [],
            'message': message,
        }
        return data

    @classmethod
    def internal_server_error(cls):
        data = {
            'statusCode': 500,
            'error': True,
            'data': [],
            'message': 'Error interno del servidor',
        }
        return data