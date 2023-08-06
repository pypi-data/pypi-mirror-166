import logging
from redis_sessions.session import SessionStore as RedisSessionStore

from .redis import KeycloakSessionStorage

logger = logging.getLogger(__name__)


class SessionStore(RedisSessionStore):
    def cycle_key(self):
        """
        Create a new session key, while retaining the current session data.
        """
        data = self._session
        key = self.session_key
        keycloak_session_id = data.get("keycloak_session_id")
        self.create()
        self._session_cache = data

        if key:
            self.delete(key)

        if keycloak_session_id:
            logger.debug("Cycling key for keycloak session %s", keycloak_session_id)
            keycloak_session = KeycloakSessionStorage(
                keycloak_session_id,
                self.session_key,
                key
            )
            keycloak_session.create_or_update()
