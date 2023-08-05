import logging

import requests

LOGGER = logging.getLogger(__name__)


class IBGE:
    IBGE_API_URL = "https://servicodados.ibge.gov.br/api"
    PARAMS = {"view": "nivelado", "orderBy": "nome"}

    @classmethod
    def get_states(cls):
        url = f"{cls.IBGE_API_URL}/v1/localidades/estados"
        response = requests.get(url=url, params=cls.PARAMS)
        if response.ok:
            return response.json()

        LOGGER.warning(
            "get_states error: response=%s",
            response.text,
        )
        return {"errors": response.text}

    @classmethod
    def get_cities(cls, uf: str):
        url = f"{cls.IBGE_API_URL}/v1/localidades/estados/{uf}/distritos"
        response = requests.get(url=url, params=cls.PARAMS)
        if response.ok:
            return response.json()

        LOGGER.warning(
            "get_cities error: response=%s",
            response.text,
        )
        return {"errors": response.text}
