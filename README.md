# Getting Started with Pulsar

This repo is an example of using Apache Pulsar. It's made to help you better understand how Pulsar works in a local environmen so you can test all kinds of features of Pulsar.

### Requirements

- Python3.7 installed (The `pulsar-client` requires 3.7)
- Docker & Docker Compost installed

## 1. Clone repo

```
git clone https://github.com/codingforentrepreneurs/getting-started-with-pulsar
cd getting-started-with-pulsar
```

## 2. Create python3.7 Venv & Install Requirements

Yes, you have to use Python3.7 to leverage the python pulsar-client

```
python3.7 -m venv venv
```

Activate it (mac/linux)

```
source venv/bin/activate
```

Windows:

```
.\venv\Scripts\activate
```

```
$(venv) python3.7 -m pip install pip --upgrade
$(venv) python3.7 -m pip install -r requirements.txt
```

## 3. Run docker-compose

```
docker compose up --build
```

- replace `docker compose` with `docker-compose` where necessary
- Run with `-d` once you have the who repo working.
- Our pulsar conatiner is named `gs_pulsar` so we can more easily run commands

## 4. Now we'll create a new tenant, namespace, and topic

Here are the details for our tenant:

- tenant name: `cfe-tenant`
- namespace: `example-namespace` (think of it as `cfe-tenant/example-namespace`)
- topics:
  - `input-topic` (think of this as `persistent://cfe-tenant/example-namespace/input-topic`)
  - `output-topic` (think of this as `persistent://cfe-tenant/example-namespace/output-topic`)

Here are the commands:

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants create cfe-tenant
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin namespaces create cfe-tenant/example-namespace

docker exec -it gs_pulsar /pulsar/bin/pulsar-admin topics create persistent://cfe-tenant/example-namespace/input-topic
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin topics create persistent://cfe-tenant/example-namespace/output-topic
```

> The Puslar/Docker command references are below

## 5. Create a Pulsar Function

Functions give us the ability to modify data from an input topic and send it to an output topic.

In our local repo, we have the directory `example_functions` that contains `cfemain.py` which contains a class called `EchoFunction` which contains a method called `process`. Please review this method to understand the logic behind it.

In our above example we remember that we have:

- tenant name: `cfe-tenant`
- namespace: `example-namespace` (think of it as `cfe-tenant/example-namespace`)
- topics:
  - `input-topic` (think of this as `persistent://cfe-tenant/example-namespace/input-topic`)
  - `output-topic` (think of this as `persistent://cfe-tenant/example-namespace/output-topic`)

To create a function we need all the above plus

- An actual python class or function to handle input data (it can be a Java function too)
- A docker container path to the actual function (`/pulsar/example_functions/cfemain.py`). Remember that `example_functions/` is being mounted within our Docker container at `/pulsar/example_functions/`. This mounting was done manually within `docker-compose.yaml`

Here's the command:

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin functions create \
  --py /pulsar/example_functions/cfemain.py \
  --classname cfemain.EchoFunction \
  --tenant cfe-tenant \
  --namespace example-namespace \
  --name cfe-echo-function \
  --inputs persistent://cfe-tenant/example-namespace/input-topic \
  --output persistent://cfe-tenant/example-namespace/output-topic
```

Personally, when updating this function, I find it easiest to just delete it and start over. To delete it just use:

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin functions delete \
  --tenant cfe-tenant \
  --namespace example-namespace \
  --name cfe-echo-function
```

## 6. Consumer and Producer

Assuming you completed everything above, we can now run our consumer and producer.

## 7. Pulsar Admin Reference Commands

### Tenant List

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants list
```

We should see:

```
"public"
"pulsar"
"sample"
```

### Tenant Create (`create`)

Create a new Tenant

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants create cfe-example
```

> The format is `docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants create <tenant name>`

### Tenant Detail (`get`)

Get Tenant

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants get public
```

> The format is `docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants get <tenant name>`

### Tenant Delete (`delete`)

Delete Tenant

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants delete cfe-example
```

> The format is `docker exec -it gs_pulsar /pulsar/bin/pulsar-admin tenants delete <tenant name>`

### Create Function

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin functions create \
  --py /pulsar/example_functions/cfemain.py \
  --classname cfemain.EchoFunction \
  --tenant cfe-tenant \
  --namespace example-namespace \
  --name cfe-echo-function \
  --inputs persistent://cfe-tenant/example-namespace/input-topic \
  --output persistent://cfe-tenant/example-namespace/output-topic
```

### Delete Function

```
docker exec -it gs_pulsar /pulsar/bin/pulsar-admin functions delete \
  --tenant cfe-tenant \
  --namespace example-namespace \
  --name cfe-echo-function
```
