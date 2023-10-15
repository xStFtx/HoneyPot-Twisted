
 # Twisted Fake Servers

This repository contains code for fake FTP and SSH servers built using the Twisted framework. These servers are designed to respond with failure messages for authentication attempts, making them useful for certain testing scenarios.

## Features

- **Fake FTP Server**: Responds with a failure message for any login attempt.
- **Fake SSH Server**: Responds with a failure message for any non-root login attempt. Terminates the connection for `root` user attempts.

## Requirements

- Python 3.x
- Twisted
- Twisted[conch]

You can install the required packages using pip:

```bash
pip install twisted twisted[conch]
```

## Usage

1. **Modify the Code (Optional)**:
   - If you want to use your own public and private keys for the SSH server, replace the placeholders "YOUR_PUBLIC_KEY" and "YOUR_PRIVATE_KEY" in the code.

2. **Running the Servers**:

   Execute the script to run both servers:

   ```bash
   python filename.py
   ```

   By default, the FTP server will run on port `2121` and the SSH server on port `2222`.

3. **Customization**:

   You can customize the ports and keys by modifying the arguments passed to the `run_servers` function in the code.

## Logging

The code includes basic logging to the console, which will show server activity and incoming connection attempts.

## Warning

This code is for demonstration and testing purposes only. Do not deploy it in production environments as it lacks security mechanisms.

