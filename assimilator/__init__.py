from contextlib import contextmanager

import assimilator.core.database
import assimilator.core.patterns
import assimilator.internal


@contextmanager
def optional_dependencies(error: str = "ignore"):
    assert error in {"raise", "warn", "ignore"}
    try:
        yield None
    except ImportError as e:
        if error == "raise":
            raise e
        if error == "warn":
            msg = f'Missing optional dependency "{e.name}". Use pip or conda to install.'
            print(f'Warning: {msg}')


with optional_dependencies():
    import assimilator.alchemy

with optional_dependencies():
    import assimilator.kafka
