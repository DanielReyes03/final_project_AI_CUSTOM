class ContextStore:
    def __init__(self):
        self._store = {}  # {user_id: {key: value}}

    def save(self, user_id, key, value):
        if user_id not in self._store:
            self._store[user_id] = {}
        self._store[user_id][key] = value
        return True

    def list_for_user(self, user_id):
        entries = self._store.get(user_id, {})
        return [{"key": k, "value": v} for k, v in entries.items()]
