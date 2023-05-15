import os


if os.environ.get('PY_ASSIMILATOR_MESSAGE', None) is None:
    print(f"""
                 ___              _           _ __      __            
    ____  __  __/   |  __________(_)___ ___  (_) /___ _/ /_____  _____
   / __ \/ / / / /| | / ___/ ___/ / __ `__ \/ / / __ `/ __/ __ \/ ___/
  / /_/ / /_/ / ___ |(__  |__  ) / / / / / / / / /_/ / /_/ /_/ / /    
 / .___/\__, /_/  |_/____/____/_/_/ /_/ /_/_/_/\__,_/\__/\____/_/     
/_/    /____/


    Thank you for using PyAssimilator!
    Documentation is available here: https://knucklesuganda.github.io/py_assimilator/
    Star this library on GitHub and get perks: https://github.com/knucklesuganda/py_assimilator

    If you want to turn off this text, add an environment variable:
    1) You can add this code BEFORE all of your imports:
        import os
        os.environ['PY_ASSIMILATOR_MESSAGE'] = 'False'

    2) You can add it within your system or in your .env file: PY_ASSIMILATOR_MESSAGE=False
    """)
