import json

class Response:

    @classmethod
    def aws(cls, data: dict):

        data['data'] = data.get('data', [])
        data['error'] = data.get('error', False)

        return {
            "statusCode": data['statusCode'],
            "headers": {
                'Content-Type': 'application/json'
            },
            "body": json.dumps(data)
        }
    
    @classmethod
    def error(cls, data = [],  message: str = 'Error del cliente'):
        data = {
            'statusCode': 400,
            'error': True,
            'data': data,
            'message': message,
        }
        return cls.aws(data)

    @classmethod
    def success(cls, data: list = [], message: str = 'Petición exitosa', pagination: dict = {}):
        response = {
            'statusCode': 200,
            'data': data,
            'message': message
        }
        if pagination:
            response['pagination'] = pagination
        return cls.aws(response)
    
    @classmethod
    def not_found(cls, message: str = 'Recurso no encontrado'):
        data = {
            'statusCode': 404,
            'error': True,
            'data': [],
            'message': message,
        }
        return cls.aws(data)

    @classmethod
    def internal_server_error(cls):
        data = {
            'statusCode': 500,
            'error': True,
            'data': [],
            'message': 'Error interno del servidor',
        }
        return cls.aws(data)