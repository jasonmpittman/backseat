# Backseat
Backseat is a cross-platform and cross-ditribution GNU/Linux patch management tool.

## Table of Contents
- [Features](#features)
- [Implementation](#implementation)
- [Configuration](#configuration)
- [Acknowledgments](#acknowledgments)

## Dependencies
- PyCryptodome

## Features

The Backseat agent is capable of:
- Producing a differential of missing patches compared to official distribution repository.
- Installing missing patches based on Backseat server selections.  
- Execute commands issued from Backseat server.  

On each heartbeat:  
- Sending a list of open and listening TCP and UDP ports.  
- Sending a list of local users and groups.  
- Sending an array of system parameters (uptime, ).  

The Backseat server is capable of:  
-  Managing endpoints across major GNU/Linux distributions. No count limit!  
-  Sending commands to individual or groups of endpoints.  
-  Orchestrating patch installation.  

All network communication between agent and server occurs within an encrypted tunnel.

## Implementation

### Server


### Endpoint



## Configuration
### host.config
The format for a line in the host.config file is:

|Endpoint Name| |Endpoint OS| |Endpoint's public key|

#### Explaination:
|Endpoint Name|:
This is a name that you come up with in order to keep track of this
host. This is for your use and does not have any bearing on how the
code acts.

|Endpoint OS|:	 
This the the operating system that the endpoint is running.

|Endpoint's public key|:
This is the Endpoint't public key. This is needed so that signed
messages can be verified

Each line in the file is 1 endpoint.

### server_info.config
The configuration of this file needs to be done for both the server and the
endpoint. The endpoint uses this information in order to connect with the
server.

Format:
|Server IP| |Server Port| |Server Public Key|

#### Explaination:
|Server IP|: The server's IP.

|Server Port|: The server's Port.

|Server Public Key|: The Server's Public Key.

### accounts.config
The accounts.config file is used to register users with the server. Basically,
it determines who has access to the server.

Format:
|username (in plain text)|,|Hashed password|

#### Explaination:
|username|:
The username used for server access in plain text.

|Hashed password|:
The hash of the password using SHA512. There is a function in account_handler.py
(called add_account) that will be useful to use in order to add an account.

Each line is 1 username and password pair.


## Acknowledgements
