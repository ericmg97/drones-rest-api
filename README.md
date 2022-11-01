# DRONES MANAGEMENT WITH DJANGO REST API
:scroll: **START**

## Introduction

There is a major new technology that is destined to be a disruptive force in the field of transportation: **the drone**. Just as the mobile phone allowed developing countries to leapfrog older technologies for personal communication, the drone has the potential to leapfrog traditional transportation infrastructure.

Useful drone functions include delivery of small items that are (urgently) needed in locations with difficult access.

---

## Task description

We have a fleet of **10 drones**. A drone is capable of carrying devices, other than cameras, and capable of delivering small loads. For our use case **the load is medications**.

A **Drone** has:
  
- serial number (100 characters max);
- model (Lightweight, Middleweight, Cruiserweight, Heavyweight);
- weight limit (500gr max);
- battery capacity (percentage);
- state (IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING).

Each **Medication** has:

- name (allowed only letters, numbers, ‘-‘, ‘_’);
- weight;
- code (allowed only upper case letters, underscore and numbers);
- image (picture of the medication case).

Develop a service via REST API that allows clients to communicate with the drones (i.e. **dispatch controller**). The specific communicaiton with the drone is outside the scope of this task.

The service should allow:

- registering a drone;
- loading a drone with medication items;
- checking loaded medication items for a given drone;
- checking available drones for loading;
- check drone battery level for a given drone;

> Feel free to make assumptions for the design approach.

---

### Requirements

While implementing your solution **please take care of the following requirements**:

#### Functional requirements

- There is no need for UI;
- Prevent the drone from being loaded with more weight that it can carry;
- Prevent the drone from being in LOADING state if the battery level is **below 25%**;
- Introduce a periodic task to check drones battery levels and create history/audit event log for this.

---

#### Non-functional requirements

- Input/output data must be in JSON format;
- Your project must be buildable and runnable;
- Your project must have a README file with build/run/test instructions (use DB that can be run locally, e.g. in-memory, via container);
- Required data must be preloaded in the database.
- JUnit tests are optional but advisable (if you have time);
- Advice: Show us how you work through your commit history.

---

## Installation

To build and install this solution you just need to setup **docker** and **docker-compose**. Optionally, you can add them to your *system path*.

### Docker

Follow instructions for installing **docker** and **docker-compose**, this can be found [here](https://www.docker.com/).

Make sure that docker is correctly configured on your machine by running the following command:

```bash
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
d1725b59e92d: Pull complete 
Digest: sha256:0add3ace90ecb4adbf7777e9aacf18357296e799f81cabc9fde470971e499788
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

---

## Build and Run Instructions

To build and run this project, you just have to execute the following commands inside the root folder of the project:

```bash
docker-compose build
$ docker-compose up
[+] Running 5/4
 - Network drones-rest-api_default       Created                                                                   0.0s
 - Volume "drones-rest-api_dev-data"     Created                                                                   0.0s
 - Volume "drones-rest-api_dev-db-data"  Created                                                                   0.0s
 - Container drones-rest-api-db-1        Created                                                                   0.0s
 - Container drones-rest-api-app-1       Created                                                                   0.1s
Attaching to drones-rest-api-app-1, drones-rest-api-db-1
drones-rest-api-db-1   | The files belonging to this database system will be owned by user "postgres".
drones-rest-api-db-1   | This user must also own the server process.
drones-rest-api-db-1   |
drones-rest-api-db-1   | The database cluster will be initialized with locale "en_US.utf8".
drones-rest-api-db-1   | The default database encoding has accordingly been set to "UTF8".
drones-rest-api-db-1   | The default text search configuration will be set to "english".
drones-rest-api-db-1   |
drones-rest-api-db-1   | Data page checksums are disabled.
drones-rest-api-db-1   |
drones-rest-api-db-1   | fixing permissions on existing directory /var/lib/postgresql/data ... ok
drones-rest-api-db-1   | creating subdirectories ... ok
drones-rest-api-db-1   | selecting dynamic shared memory implementation ... posix
drones-rest-api-db-1   | selecting default max_connections ... 100
drones-rest-api-db-1   | selecting default shared_buffers ... 128MB
drones-rest-api-db-1   | selecting default time zone ... UTC
drones-rest-api-db-1   | creating configuration files ... ok
drones-rest-api-db-1   | running bootstrap script ... ok
drones-rest-api-db-1   | performing post-bootstrap initialization ... sh: locale: not found
drones-rest-api-db-1   | 2022-10-31 23:40:32.898 UTC [30] WARNING:  no usable system locales were found
drones-rest-api-db-1   | ok
drones-rest-api-db-1   | syncing data to disk ... ok
drones-rest-api-db-1   |
drones-rest-api-db-1   |
drones-rest-api-db-1   | Success. You can now start the database server using:
drones-rest-api-db-1   |
drones-rest-api-db-1   |     pg_ctl -D /var/lib/postgresql/data -l logfile start
drones-rest-api-db-1   |
drones-rest-api-db-1   | initdb: warning: enabling "trust" authentication for local connections
drones-rest-api-db-1   | You can change this by editing pg_hba.conf or using the option -A, or
drones-rest-api-db-1   | --auth-local and --auth-host, the next time you run initdb.
drones-rest-api-db-1   | waiting for server to start....2022-10-31 23:40:33.775 UTC [36] LOG:  starting PostgreSQL 13.8 on x86_64-pc-linux-musl, compiled by gcc (Alpine 11.2.1_git20220219) 11.2.1 20220219, 64-bit
drones-rest-api-db-1   | 2022-10-31 23:40:33.776 UTC [36] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
drones-rest-api-db-1   | 2022-10-31 23:40:33.780 UTC [37] LOG:  database system was shut down at 2022-10-31 23:40:33 UTC
drones-rest-api-db-1   | 2022-10-31 23:40:33.784 UTC [36] LOG:  database system is ready to accept connections
drones-rest-api-db-1   |  done
drones-rest-api-db-1   | server started
drones-rest-api-db-1   | CREATE DATABASE
drones-rest-api-db-1   |
drones-rest-api-db-1   |
drones-rest-api-db-1   | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
drones-rest-api-db-1   |
drones-rest-api-db-1   | waiting for server to shut down...2022-10-31 23:40:34.028 UTC [36] LOG:  received fast shutdown request
drones-rest-api-db-1   | .2022-10-31 23:40:34.029 UTC [36] LOG:  aborting any active transactions
drones-rest-api-db-1   | 2022-10-31 23:40:34.030 UTC [36] LOG:  background worker "logical replication launcher" (PID 43) exited with exit code 1
drones-rest-api-db-1   | 2022-10-31 23:40:34.031 UTC [38] LOG:  shutting down
drones-rest-api-db-1   | 2022-10-31 23:40:34.044 UTC [36] LOG:  database system is shut down
drones-rest-api-db-1   |  done
drones-rest-api-db-1   | server stopped
drones-rest-api-db-1   |
drones-rest-api-db-1   | PostgreSQL init process complete; ready for start up.
drones-rest-api-db-1   |
drones-rest-api-db-1   | 2022-10-31 23:40:34.147 UTC [1] LOG:  starting PostgreSQL 13.8 on x86_64-pc-linux-musl, compiled by gcc (Alpine 11.2.1_git20220219) 11.2.1 20220219, 64-bit
drones-rest-api-db-1   | 2022-10-31 23:40:34.148 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
drones-rest-api-db-1   | 2022-10-31 23:40:34.148 UTC [1] LOG:  listening on IPv6 address "::", port 5432
drones-rest-api-db-1   | 2022-10-31 23:40:34.152 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
drones-rest-api-db-1   | 2022-10-31 23:40:34.157 UTC [50] LOG:  database system was shut down at 2022-10-31 23:40:34 UTC
drones-rest-api-db-1   | 2022-10-31 23:40:34.160 UTC [1] LOG:  database system is ready to accept connections
drones-rest-api-app-1  | Waiting for database...
drones-rest-api-app-1  | Database available!
drones-rest-api-app-1  | Operations to perform:
drones-rest-api-app-1  |   Apply all migrations: admin, auth, authtoken, contenttypes, core, sessions
drones-rest-api-app-1  | Running migrations:
drones-rest-api-app-1  |   Applying contenttypes.0001_initial... OK
drones-rest-api-app-1  |   Applying contenttypes.0002_remove_content_type_name... OK
drones-rest-api-app-1  |   Applying auth.0001_initial... OK
drones-rest-api-app-1  |   Applying auth.0002_alter_permission_name_max_length... OK
drones-rest-api-app-1  |   Applying auth.0003_alter_user_email_max_length... OK
drones-rest-api-app-1  |   Applying auth.0004_alter_user_username_opts... OK
drones-rest-api-app-1  |   Applying auth.0005_alter_user_last_login_null... OK
drones-rest-api-app-1  |   Applying auth.0006_require_contenttypes_0002... OK
drones-rest-api-app-1  |   Applying auth.0007_alter_validators_add_error_messages... OK
drones-rest-api-app-1  |   Applying auth.0008_alter_user_username_max_length... OK
drones-rest-api-app-1  |   Applying auth.0009_alter_user_last_name_max_length... OK
drones-rest-api-app-1  |   Applying auth.0010_alter_group_name_max_length... OK
drones-rest-api-app-1  |   Applying auth.0011_update_proxy_permissions... OK
drones-rest-api-app-1  |   Applying auth.0012_alter_user_first_name_max_length... OK
drones-rest-api-app-1  |   Applying core.0001_initial... OK
drones-rest-api-app-1  |   Applying admin.0001_initial... OK
drones-rest-api-app-1  |   Applying admin.0002_logentry_remove_auto_add... OK
drones-rest-api-app-1  |   Applying admin.0003_logentry_add_action_flag_choices... OK
drones-rest-api-app-1  |   Applying authtoken.0001_initial... OK
drones-rest-api-app-1  |   Applying authtoken.0002_auto_20160226_1747... OK
drones-rest-api-app-1  |   Applying authtoken.0003_tokenproxy... OK
drones-rest-api-app-1  |   Applying core.0002_auto_20221029_1826... OK
drones-rest-api-app-1  |   Applying core.0003_auto_20221029_1827... OK
drones-rest-api-app-1  |   Applying core.0004_alter_drone_weight_limit... OK
drones-rest-api-app-1  |   Applying core.0005_medication_image... OK
drones-rest-api-app-1  |   Applying sessions.0001_initial... OK
drones-rest-api-app-1  | Installed 16 object(s) from 1 fixture(s)
drones-rest-api-app-1  | Watching for file changes with StatReloader
drones-rest-api-app-1  | Performing system checks...
drones-rest-api-app-1  |
drones-rest-api-app-1  | System check identified no issues (0 silenced).
drones-rest-api-app-1  | October 31, 2022 - 23:40:39
drones-rest-api-app-1  | Django version 4.0.8, using settings 'app.settings'
drones-rest-api-app-1  | Starting development server at http://0.0.0.0:8000/
drones-rest-api-app-1  | Quit the server with CONTROL-C.
```

Once the commands are executed and the output is the same as shown above, the server will be available at:
> <http://127.0.0.1:8000> and
> <http://localhost:8000>

---

## Configuration and Testing

When you start the server for the first time, it will automatically generate some data and an administration user.

You can access the administration site located at the url <http://127.0.0.1:8000/admin/> with the following credentials:

```bash
Email: admin@example.com
Password: Example1
```

Swagger View of API:
![image](https://user-images.githubusercontent.com/39969751/199131772-1514e337-2d31-47c7-adff-c5800acd72f7.png)

A Swagger server will be enabled at <http://127.0.0.1/api/docs> to facilitate use and experimentation with the API. In order to use the API functionalities, you must first generate an authentication token with the user mentioned above through a *post request* to the </api/user/token> endpoint and adding it on each request that you make. Swagger has a built in functionality for this on the up right corner of the webpage:

![image](https://user-images.githubusercontent.com/39969751/199132224-0ea48ca6-4d38-4db8-a6b0-1e22b9bf1d83.png).

Once you have successfully added the security token, you will be able to use all API endpoints.

:scroll: **END**
