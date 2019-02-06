import yaml


class Config:
    def load_config(self, config_root):
        config_path = f'{config_root}/config.yml'

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)


config = Config()
