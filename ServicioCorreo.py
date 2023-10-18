import logging
import threading

from concurrent import futures

class Correo:
    def __init__(self, destinatario, asunto, cuerpo):
        self.id = None
        self.destinatario = destinatario
        self.asunto = asunto
        self.cuerpo = cuerpo

    def __repr__(self):
        return f"Correo({self.id}, {self.destinatario}, {self.asunto}, {self.cuerpo})"


class ServicioCorreo:
    def enviar_correo_simple(self, correo):
        print(f"Enviando correo a {correo.destinatario}")
        return True


class RetryableServicioCorreo(ServicioCorreo):
    def enviar_correo(self, correo):
        with futures.ThreadPoolExecutor() as executor:
            executor.submit(self._enviar_correo_con_reintento, correo)

    def _enviar_correo_con_reintento(self, correo):
        for i in range(max_intentos):
            try:
                return self._enviar_correo_simple(correo)
            except Exception as e:
                logging.error(e)
        else:
            raise Exception("No se pudo enviar el correo")


class CorreoFacada:
    def enviar_correo(self, correo):
        return RetryableServicioCorreo().enviar_correo(correo)


class CorreoLogger(logging.Logger):
    def __init__(self, name="correo_logger"):
        super().__init__(name)

    def informe_envio_correo(self, correo):
        logging.info("Se envió el correo a {}", correo.destinatario)


class CorreoCache:
    def __init__(self):
        self.cache = {}

    def get(self, correo):
        return self.cache.get(correo.id)

    def set(self, correo, resultado):
        correo.id = uuid.uuid4()
        self.cache[correo.id] = resultado


def main():
    servicio_correo = CorreoFacada()

    correo = Correo("jp@example.com", "Hello, world!", "This is the body of the email.")
    servicio_correo.enviar_correo(correo)

    CorreoLogger().informe_envio_correo(correo)

    correo = Correo("jp@example.com", "Hello, world!", "This is the body of the email.")
    resultado = CorreoCache().get(correo)