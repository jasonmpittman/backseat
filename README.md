# Backseat
Backseat is a cross-platform and cross-ditribution GNU/Linux patch management tool. 

## Table of Contents
- [Features](#features)
- [Implementation](#implementation)
- [Acknowledgments](#acknowledgments)

## Features

The Backseat agent is capable of:
1. Producing a differential of missing patches compared to official distribution repository.
2. Installing missing patches based on Backseat server selections.  
3. Execute commands issued from Backseat server.  
  
On each heartbeat:  
4. Sending a list of open and listening TCP and UDP ports.  
5. Sending a list of local users and groups.  
6. Sending an array of system parameters (uptime, ).  

The Backseat server is capable of:  
1.  Managing endpoints across major GNU/Linux distributions. No count limit!  
2.  Sending commands to individual or groups of endpoints.  
3.  Orchestrating patch installation.  
  
All network communication between agent and server occurs within an encrypted tunnel.

## Implementation

## Agent

## Server

## Acknowledgements
