<div align="center">
<img width="60px" src="https://pts-project.org/android-chrome-512x512.png">
<h1>Python 3 Colander REST client</h1>
<p>
Brings your project the ability to populate your <a href="https://github.com/PiRogueToolSuite/colander" alt="Colander repository">Colander</a> server with collected data.
</p>
<p>
License: GPLv3
</p>
<p>
<a href="https://pts-project.org">Website</a> | 
<a href="https://pts-project.org/docs/colander/overview/">Documentation</a> | 
<a href="https://discord.gg/qGX73GYNdp">Support</a>
</p>
</div>

## Installation

```
pip install colander-client
```

## Project status

* Cases : Query / Create
* Devices : Query / Create
* Observables : Query / Create
* PiRogueExperiment : Query / Create
* Artifacts : Query / Create
* Teams : Query

_Refer to Colander documentation for data type explanation._

_For a quick overview of changes, take a look at [revisions](#Revisions)_ 

> [!WARNING]
> Deprecation warnings have been introduced.
> Keep an eye on those. Backward compatibilities support will be dropped sooner of later.  

## Usage example

### Instancing

```python
from colander_client.client import Client

base_url = 'https://my-colander-server'
api_key = 'my-user-api-key'

client = Client(base_url=base_url, api_key=api_key)
```

The library also support the following environment variables :
* `COLANDER_PYTHON_CLIENT_BASE_URL`
* `COLANDER_PYTHON_CLIENT_API_KEY`

Having such environment variables set, you can just do:

```python
from colander_client.client import Client

client = Client()
```

### Case management

Before all, you need a case to work with:

```python
# Assuming the given case id :
case_id = 'current-case-id-im-working-on'

case = client.get_case(case_id)
```

Your Case will be asked for each futur creation calls:

```python
artifact = client.upload_artifact(case=case, filepath='/tmp/dump', ...)
experiment = client.create_pirogue_experiment(case=case, pcap=pcap_artifact, ...)
```

Since, the Case is somehow the workspace you are working on during a Colander populating session,
you can use the following handy function:

```python
client.switch_case(case)
```

Then you may avoid mentioning case in futur creation calls:
```python
artifact = client.upload_artifact(filepath='/tmp/dump', ...)
experiment = client.create_pirogue_experiment(pcap=pcap_artifact, ...)
```

To disable case switching:
```python
client.switch_case(None)
```

In any state, Case presence at function call takes precedence.

### Case creation

You may want to create a case on the fly. Since v1.0.4, you can create a case like this:
```python
from colander_client.domain import TlpPap

fresh_case = client.create_case(name='My beaufiful new case',
                                description='Sensitive stuff',
                                tlp=TlpPap.AMBER,
                                pap=TlpPap.RED)
```
> [!IMPORTANT]
> Even if it is optional, we encourage you to specify `tlp` and `pap` levels
> for new cases.

You may want to specify which teams you want to share this case with.
For that, you have to query for teams beforehand:

```python
my_team_list = client.get_teams(name='my team')

shared_fresh_case = client.create_case(name='My beaufiful new case',
                                description='Sensitive stuff',
                                teams=my_team_list,
                                tlp=TlpPap.WHITE,
                                pap=TlpPap.GREEN)
```

Or with a specific team:
```python
my_team = client.get_team('a-team-id-i-know')

shared_fresh_case = client.create_case(name='My beaufiful new case',
                                description='Sensitive stuff',
                                teams=[my_team])
```
> [!NOTE]
> Be careful to provide a list of team

### Artifact uploads

```python
a_type = client.get_artifact_type_by_short_name( 'SAMPLE' )
# Assuming we have switched to a Case
artifact = client.upload_artifact(
    filepath='/tmp/captured.file', artifact_type=a_type)
```

Large file upload progression can be followed with a progress callback:
```python
def progress(what, percent, status):
    print(f"{what} is at {percent}%, currently it is: {status}")
    # in case of artifact upload progress 'what' is the given filepath

a_type = client.get_artifact_type_by_short_name( 'SAMPLE' )
# Assuming we have switched to a Case
artifact = client.upload_artifact(
    filepath='/tmp/captured.file', artifact_type=a_type, progress_callback=progress)
```

When you have many uploads to proceed, you can globally set a callback on the client,
avoiding repetitively passing it at function calls:
```python
client.set_global_progress_callback(progress)
```

In any state, callback presence at function call takes precedence.

### PiRogue Experiment creation

```python
experiment = client.create_pirogue_experiment(
    name='My today investigation',
    pcap=pcap_artifact,
    socket_trace=socket_trace_artifact,
    sslkeylog=sslkeylog_artifact)
```

### Device creation

Device can be specified on Artifact or PiRogue Experiment.
The creation is as follow:
```python
d_type = client.get_device_type_by_short_name('LAPTOP')

pul_device = client.create_device(name='Potential unsecure laptop', device_type=d_type)
```

Then specified at Artifact or PiRogue Experiment creation:
```python
artifact = client.upload_artifact(
    filepath='/tmp/captured.file', artifact_type=a_type,
    extra_params={
        'extracted_from': pul_device
    })

experiment = client.create_pirogue_experiment(
    name='My today investigation',
    pcap=pcap_artifact,
    socket_trace=socket_trace_artifact,
    sslkeylog=sslkeylog_artifact,
    extra_params={
        'target_device': pul_device
    })
```

### Relations

You can create entities relation like this:
```python
artifact_1 = client.upload_artifact( [...] )
artifact_2 = client.upload_artifact( [...] )
device_1 = client.create_device( [...] )

relation_1 = client.creation_relation(name='internally refers',
                                      obj_from=artifact_1,
                                      obj_to=artifact_2)

relation_2 = client.creation_relation(name='mentions victim name',
                                      obj_from=artifact_2,
                                      obj_to=device_1)
```


## Revisions
### 1.0.4 - August 1st 2024
 * Add teams basic support (query)
 * Add case creation support
 * Add entity relations support (query and creation)
 * Client domains refactor
 * Some minor deprecation introduction

### 1.0.3 - January 22th 2024
 * Add observables support (query and creation)

### 1.0.2 - January 16th 2023
 * Add case search by name
 * Add device creation support