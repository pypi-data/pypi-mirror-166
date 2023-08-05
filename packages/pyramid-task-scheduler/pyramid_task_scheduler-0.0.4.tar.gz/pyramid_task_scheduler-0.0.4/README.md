# pyramid_task_scheduler

[![Build Status](https://cloud.drone.io/api/badges/Eldhrimner/pyramid_task_scheduler/status.svg)](https://cloud.drone.io/Eldhrimner/pyramid_task_scheduler)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install

install packages
`pip install pyramid-task-scheduler`

or require in `setup.py`

add the follwing line to your `Configuratior` section of your pyramid application:
e.g
```python
    config = Configurator(settings=settings)
    config.include('pyramid_task_scheduler')  # Add this Line
```
## Modes

### json crontab

add the following two lines to your .ini file

```{ .ini }
pyramid_task_scheduler_mode = json
pyramid_task_scheduler_path = path_to/crontab.json
```

single cron crontab example:

```json
{
	"cron": [
		{
			"name": "first_cron",
			"import_script": "import_script",
			"exec_func": "function_to_execute",
			"crontab_time": "0 * * * *"
		}
	]
}
```

multiple crons crontab example:

```json
{
    "cron": [
        {
            "name": "first_cron",
            "import_script": "import_script",
            "exec_func": "function_to_execute",
            "crontab_time": "0 * * * *"
        },
        {
            "name": "second_cron",
            "import_script": "import_script",
            "exec_func": "function_to_execute",
            "crontab_time": "0 * * * *"
        }
    ]   
}
```

# NOTE

this package is alpha experimental. It is recommened to NOT use it for productional environments.
