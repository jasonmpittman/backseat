from backseat_endpoint import endpoint_message

import unittest

import json

unittest.TestLoader.sortTestMethodsUsing = None
class TestCreateMsg(unittest.TestCase):

    def test_types(self):
        ping = True
        ready = True
        completed = True
        stdout = "-"
        stderr = "-"
        successful = True
        exit_code = 0
        command_id = 11
        
        EM = endpoint_message.EndpointMessage()
        message = EM.create_msg(ping, ready, completed, stdout, stderr, successful, exit_code, command_id)
        MD = json.loads(message)

        self.assertEqual(type(MD["ping"]), type(ping))
        self.assertEqual(type(MD["ready"]), type(ready))
        self.assertEqual(type(MD["completed"]), type(completed))
        self.assertEqual(type(MD["stdout"]), type(stdout))
        self.assertEqual(type(MD["stderr"]), type(stderr))
        self.assertEqual(type(MD["successful"]), type(successful))
        self.assertEqual(type(MD["exit_code"]), type(exit_code))
        self.assertEqual(type(MD["command_id"]), type(command_id))
    
    def test_content(self):
        ping = True
        ready = True
        completed = True
        stdout = "-"
        stderr = "-"
        successful = True
        exit_code = 0
        command_id = 11

        EM = endpoint_message.EndpointMessage()
        message = EM.create_msg(ping, ready, completed, stdout, stderr, successful, exit_code, command_id)
        MD = json.loads(message)

        self.assertEqual(MD["ping"], ping)
        self.assertEqual(MD["ready"], ready)
        self.assertEqual(MD["completed"], completed)
        self.assertEqual(MD["stdout"], stdout)
        self.assertEqual(MD["stderr"], stderr)
        self.assertEqual(MD["successful"], successful)
        self.assertEqual(MD["exit_code"], exit_code)
        self.assertEqual(MD["command_id"], command_id)

class TestGetPingMsg(unittest.TestCase):
    def test_correct(self):
        EM = endpoint_message.EndpointMessage()
        ping_msg = EM.get_ping_msg()
        MD = json.loads(ping_msg)
        
        self.assertEqual(MD["ping"], True)
        self.assertEqual(MD["ready"], True)
        self.assertEqual(MD["completed"], True)
        self.assertEqual(MD["stdout"], "")
        self.assertEqual(MD["stderr"], "")
        self.assertEqual(MD["successful"], False)
        self.assertEqual(MD["exit_code"], -1)
        self.assertEqual(MD["command_id"], 0)
    
    def test_wrong(self):
        EM = endpoint_message.EndpointMessage()
        ping_msg = EM.get_ping_msg()
        MD = json.loads(ping_msg)
        self.assertNotEqual(MD["ping"], False)
        self.assertNotEqual(MD["ready"], False)
        self.assertNotEqual(MD["completed"], False)
        self.assertNotEqual(MD["stdout"], "-")
        self.assertNotEqual(MD["stderr"], "-")
        self.assertNotEqual(MD["successful"], True)
        self.assertNotEqual(MD["exit_code"], 0)
        self.assertNotEqual(MD["command_id"], 1)









        