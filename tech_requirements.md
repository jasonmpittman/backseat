# Technical Requirements

### Agent:
- Producing a differential of missing patches compared to official distribution repository.
    - Get list most up to date software versions
    - Get list of current software versions
    - Return a list of only the updates that are needed
- Installing missing patches based on Backseat server selections.
    - Server will provide a list of patches that need to be updated
    - Agent will install those patches and return [somehow] proof of success to server
- Execute commands issued from Backseat server.
    - Execute an arbitrary commands issued by the server —> this is the key to all the other parts
    - Return the resulting output to the server
