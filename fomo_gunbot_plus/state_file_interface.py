from .constants import STATE_PATH
import toml


class StateFileInterface:

    def __init__(self):
        self.current_file_state = []
        self._read_file_state()

    def _read_file_state(self):
        try:
            with open(STATE_PATH, 'r') as f:
                self.current_file_state = toml.loads(f.read())
        except json.decoder.JSONDecodeError:
            print('Doesnt Exists')  # TODO: logger
            self._write_blank_file_state()
            with open(STATE_PATH, 'r') as f:
                self.current_file_state = toml.loads(f.read())

    def _write_blank_file_state(self):
        data = dict()
        data['hot'] = []
        data['cold'] = []
        data['frozen'] = []
        data['exists'] = []
        print('Creating Default Statefile')  # TODO: logger
        with open(STATE_PATH, 'w') as f:
            f.write(toml.dumps(data))

    def _set_state(self, asset, state):
        assert isinstance(asset, str)
        assert 'BTC-' in asset, 'Must be a BTC trade pair.'

        if asset in self.current_file_state[state]:
            print(f'Already in {state}.')
            return

        self.current_file_state[state] += [asset]

        with open(STATE_PATH, 'w') as f:
            f.write(toml.dumps(self.current_file_state))
        return True

    def set_hot(self, asset):
        self._set_state(asset, 'hot')

    def set_cold(self, asset):
        self._set_state(asset, 'cold')

    def set_frozen(self, asset):
        self._set_state(asset, 'frozen')

    def set_exists(self, asset):
        self._set_state(asset, 'exists')

    def _remove_state(self, asset, state):
        assert isinstance(asset, str)
        assert 'BTC-' in asset, 'Must be a BTC trade pair.'
        if asset not in self.current_file_state[state]:
            print(f'Not in {state}.')
            return

        self.current_file_state[state].remove(asset)

        with open(STATE_PATH, 'w') as f:
            f.write(toml.dumps(self.current_file_state))
        return True

    def remove_hot(self, asset):
        self._remove_state(asset, 'hot')

    def remove_cold(self, asset):
        self._remove_state(asset, 'cold')

    def remove_frozen(self, asset):
        self._remove_state(asset, 'frozen')

    def remove_exists(self, asset):
        self._remove_state(asset, 'exists')
