# Backseat
Backseat is a cross-platform and cross-ditribution GNU/Linux patch management tool.

## Table of Contents
- [Features](#features)
- [Implementation](#implementation)
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

## Agent

## Server

## Configuration
### host.config

### server.config

### accounts.config

## Acknowledgements
