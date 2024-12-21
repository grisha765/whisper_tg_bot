import os

class Config:
    log_level: str = "INFO"
    mode: str = "bot"
    tg_id: str = '1'
    tg_hash: str = 'b6b154c3707471f5339bd661645ed3d6'
    tg_token: str = 'None'
    model_size: str = 'tiny' #tiny, tiny.en, base, base.en, small, small.en, medium, medium.en, large-v1, large-v2, large-v3, or large
    cpu_threads: str = '4'
    sessions_path: str = './'
    
    @classmethod
    def load_from_env(cls):
        for key, value in cls.__annotations__.items():
            env_value = os.getenv(key.upper())
            if env_value is not None:
                if isinstance(value, int):
                    setattr(cls, key, int(env_value))
                elif isinstance(value, list):
                    setattr(cls, key, env_value.split(","))
                else:
                    setattr(cls, key, env_value)

Config.load_from_env()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
