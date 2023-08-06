# Open LISA SDK

This SDK provides an interface to interact with the [Open LISA Server](https://github.com/aalvarezwindey/Open-LISA-Server). The server must be integrated with the instruments of interest and running in a known IP and port (TCP connections) or you must known the serial port (SERIAL connections) for the client side in order to be able to connect via this SDK.

## Installation

```
pip install open-lisa-sdk
```

## Examples

You can check online [examples](https://github.com/aalvarezwindey/Open-LISA-SDK/tree/main/examples). You can go to examples folder and run

```bash
python <example_script_name>.py
```

## API Doc

`SDK(log_level='WARNING', default_response_format='PYTHON')`: Initializes the SDK with the specified log level and default response format of the methods

    Args:
        log_level (str, optional): specifies the SDK log level. Defaults to "WARNING".
        default_response_format (str, optional): specifies the response format of the SDK methods supported
        types are "PYTHON" for Python native types or "JSON" for JSON strings. Defaults to "PYTHON".

### Methods

`connect_through_RS232(self, baudrate=921600, port=None) ‑> None`: Tries to connect with Open LISA Server through RS232 protocol

    Args:
        baudrate (int, optional): Specifies the baudrate, must be the same as in Open LISA Server. Defaults to 921600.
        port (str, optional): Serial port of the client side. Defaults to None and will try with all the ports listed by serial.tools.list_ports.comports(),
        this is not recommended since handshake information could be sent to unexpected serial ports.

    Raises:
        CouldNotConnectToServerException: raised when connection could not be stablished

`connect_through_TCP(self, host: str, port: int) ‑> None`
: Tries to connect with Open LISA Server through TCP protocol

    Args:
        host (string): Open LISA Server IP address
        port (int): Open LISA Server port number

    Raises:
        CouldNotConnectToServerException: raised when connection could not be stablished

`create_directory(self, remote_path, new_directory)`
: Creates a folder with the name specified by new_directory in remote_path folder

    Args:
        remote_path (str): folder in server side
        new_directory (str): new folder name

    Raises:
        OpenLISAException: raised when there was an error in the Server

`create_instrument(self, new_instrument, response_format=None)`
: Tries to create the new instrument with the fields specified

    Args:
        new_instrument (dict): new instrument payload
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        dict|string: server creation response

    Raises:
        OpenLISAException: raised when there was an error in the Server

`create_instrument_command(self, new_command, response_format=None)`
: Creates the command specified by new_command payload

    Args:
        new_command (dict): new command payload
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Raises:
        OpenLISAException: raised when there was an error in the Server

`delete_directory(self, remote_path)`
: Deletes the folder specified by remote_path and all its content

    Args:
        remote_path (str): path in server side

    Raises:
        OpenLISAException: raised when there was an error in the Server

`delete_file(self, file_path)`
: Deletes the remote file specified by file_path

    Args:
        file_path (str): file path in server

    Raises:
        OpenLISAException: raised when there was an error in the Server

`delete_instrument(self, instrument_id, response_format=None)`
: Tries to delete the instrument specified

    Args:
        instrument_id (int): instrument ID
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        dict|string: server delete response

    Raises:
        OpenLISAException: raised when there was an error in the Server

`delete_instrument_command(self, command_id)`
: Deletes the command specified by command_id

    Args:
        command_id (int): command ID

    Raises:
        OpenLISAException: raised when there was an error in the Server

`disconnect(self)`
: Gracefully disconnect with Open LISA Server

`execute_bash_command(self, command, capture_stdout=False, capture_stderr=False)`
: Executes the bash command specified by command in the server

    Args:
        command (str): bash command to be executed in server side, the command is executed at sandbox folder
        capture_stdout (bool, optional): if true the stdout of the command is retrieved. Defaults to False.
        capture_stderr (bool, optional): if true the stderr of the command is retrieved. Defaults to False.

    Returns:
        any: command execution result

`get_detected_physical_addresses(self, response_format=None)`
: Get a list of the detected physical addresses in the Open LISA Server

    Args:
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        list|string: the physical addresses detected

    Raises:
        OpenLISAException: raised when there was an error in the Server

`get_directory_structure(self, remote_path, response_format=None)`
: Retrieves the directory structure in server specified in remote_path

    Args:
        remote_path (str): directory path in server side
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        dict|str: directory structure

    Raises:
        OpenLISAException: raised when there was an error in the Server

`get_file(self, remote_file_name, file_target_name)`
: Tries to retrieve the file in server specified by remote_file_name and tries to save in file_target_name in client side

    Args:
        remote_file_name (str): file path in server
        file_target_name (str): file path in client

    Raises:
        OpenLISAException: raised when there was an error in the Server

`get_instrument(self, instrument_id, response_format=None)`
: Get the instrument registered in Open LISA Server that matches with the ID

    Args:
        instrument_id (int): instrument ID
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        dict|string: the instrument match
    Raises:
        OpenLISAException: raised when there was an error in the Server

`get_instrument_commands(self, instrument_id, response_format=None)`
: Get a list of the specified instrument commands

    Args:
        instrument_id (int): instrument ID
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        list|stirng: The list of the registered commands for that instrument

    Raises:
        OpenLISAException: raised when there was an error in the Server

`get_instruments(self, response_format=None)`
: Get all the instruments registered in Open LISA Server

    Args:
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        dict|string: list of registered instruments

    Raises:
        OpenLISAException: raised when there was an error in the Server

`is_valid_command_invocation(self, instrument_id, command_invocation)`
: Determines if the command invocation syntax is valid but it is not sent to the instrument

    Args:
        instrument_id (int): instrument ID
        command_invocation (str): command invocation syntax

    Returns:
        bool: True or False depending the validity of the command invocation syntax

`send_command(self, instrument_id, command_invocation, command_result_output_file=None, response_format=None, convert_result_to=None)`
: Sends the command_invocation to the specified instrument by instrument_id

    Args:
        instrument_id (int): instrument ID
        command_invocation (str): command invocation syntax with parameters
        command_result_output_file (str, optional): if provided the output of the command will be saved in server at the specified path and
        not returned to the client (convinient for low throughputs between client and server). Defaults to None.
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case
        convert_result_to (str, optional): converts the result to the specified type, supported types are "str", "double", "bytearray", "bytes" and "int". Defaults to None.

    Raises:
        InvalidCommandException: when the command could not be executed

    Returns:
        str|int|float|bytearray|bytes: the result of the command execution

`send_file(self, file_path, file_target_name)`
: Sends the file specified by client file_path and saves it in the server at file_target_name

    Args:
        file_path (str): client side file path
        file_target_name (_type_): server remote file path

    Raises:
        OpenLISAException: raised when there was an error in the Server

`update_instrument(self, instrument_id, updated_instrument, response_format=None)`
: Tries to update the instrument with the fields specified

    Args:
        instrument_id (int): instrument ID
        updated_instrument (dict): new instrument fields
        response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

    Returns:
        dict|string: server update response

    Raises:
        OpenLISAException: raised when there was an error in the Server
