class NotFound(Exception):
    """Exception para informar que um valor não foi encontrado"""
    def __init__(self, message="Recurso não encontrado"):
        self.message = message
        super().__init__(self.message)

class InvalidOperation(Exception):
    """Exception para operações inválidas """
    def __init__(self, message="Operação inválida"):
        self.message = message
        super().__init__(self.message)
