# PingMyStuff

A simple Python script that pings your websites for their status and notifies you if necessary.

## Installation

```bash
# Clone this repository
$ git clone https://github.com/larssont/PingMyStuff.git

# Go into the repository
$ cd PingMyStuff
```

You can now either install all requirements directly and start `main.py` or you can create a venv and run it from there. I'll do the latter.

```bash
#  Create venv named env
$ python3 -m venv env

# Activate venv
$ source env/bin/activate

# Install all requirements.txt
$ pip install -r requirements.txt

# Exit venv
$ deactivate
```

## Configuration

Before you can run the program you need to configure `config.yml`.

### Options

#### message

| Name  | Type   | Default  | Description  |
|---    |---     |---       |---           |
| up    | string | required | Message to send when site is up  |
| down  | string | required | Message to send when site is down  |

The following variables can be inserted into your message.

  - `{{ status }}` HTTP status code
  - `{{ name }}` Site name
  - `{{ address }}` Site address

See `config.yml` for an example.

#### notifiers

| Name       | Type            | Default  | Description       |
|---         |---              |---       |---                |
| address    | string          | required | Webhook URL (POST request)  |
| msgDataKey | string          | required | Name of the message data key in the request |
| sites      | list (string)   | required | Sites that the notifier sends updates about  |
| data       | dict            | optional | Additional data to be passed |


#### sites

| Name        | Type                    | Default  | Description       |
|---          |---                      |---       |---                |
| address     | string                  | required | Site URL          |
| consider_up | list (integer)          | required | HTTP status codes for when site should be consired up |

> **NOTE:**  Each site will get a `status` key containing it's latest status code when the program has been run. There's no need to modify or remove this since it's automatically updated.

## Running

The easiest way to run the program is by using the `start.sh` script that's included in this repo (given that you created a python venv).


If you want to continuously monitor your websites, you can use cron to run the program at an interval.

```bash
# Edit user crontab
$ crontab -e
```

In the editor that opened up can you insert the following line to run the program every 5 minutes. Replace `/path/to/PingMyStuff` with the actual path.

```bash
*/5 * * * * cd /path/to/PingMyStuff && bash start.sh
```

To generate your own cron schedule expression you can use https://crontab.guru/ for example.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.