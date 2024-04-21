from fastapi.responses import JSONResponse

class Response:

    @classmethod
    def error(cls, data=None, message: str = 'Error del cliente'):
        return cls._make_response(status_code=400, data=data, message=message, error=True)

    @classmethod
    def success(cls, data=None, message: str = 'Petición exitosa'):
        return cls._make_response(status_code=200, data=data, message=message, error=False)

    @classmethod
    def not_found(cls, message: str = 'Recurso no encontrado'):
        return cls._make_response(status_code=404, data=None, message=message, error=True)

    @classmethod
    def internal_server_error(cls, message: str = 'Error interno del servidor'):
        return cls._make_response(status_code=500, data=None, message=message, error=True)

    @classmethod
    def _make_response(cls, status_code: int, data, message: str, error: bool):
        content = {
            'statusCode': status_code,
            'error': error,
            'data': data if data is not None else [],
            'message': message
        }
        return JSONResponse(content=content, status_code=status_code)