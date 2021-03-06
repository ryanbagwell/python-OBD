
from obd.commands import OBDCommand
from obd.decoders import noop
from obd.protocols import *
from obd.protocols.protocol import Message


def test_constructor():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "01", "23", 2, noop)
	assert cmd.name      == "Test"
	assert cmd.desc      == "example OBD command"
	assert cmd.mode      == "01"
	assert cmd.pid       == "23"
	assert cmd.bytes     == 2
	assert cmd.decode    == noop
	assert cmd.supported == False

	assert cmd.get_command()  == "0123"
	assert cmd.get_mode_int() == 1
	assert cmd.get_pid_int()  == 35

	cmd = OBDCommand("Test", "example OBD command", "01", "23", 2, noop, True)
	assert cmd.supported == True


def test_clone():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("", "", "01", "23", 2, noop)
	other = cmd.clone()

	assert cmd.name      == other.name
	assert cmd.desc      == other.desc
	assert cmd.mode      == other.mode
	assert cmd.pid       == other.pid
	assert cmd.bytes     == other.bytes
	assert cmd.decode    == other.decode
	assert cmd.supported == cmd.supported


def test_call():
	p = SAE_J1850_PWM()
	m = p("48 6B 10 41 00 BE 1F B8 11 AA\r\r") # parse valid data into response object 

	# valid response size
	cmd = OBDCommand("", "", "01", "23", 4, noop)
	r = cmd(m[0])
	assert r.value == "BE1FB811"

	# response too short (pad)
	cmd = OBDCommand("", "", "01", "23", 5, noop)
	r = cmd(m[0])
	assert r.value == "BE1FB81100"

	# response too long (clip)
	cmd = OBDCommand("", "", "01", "23", 3, noop)
	r = cmd(m[0])
	assert r.value == "BE1FB8"


def test_get_command():
	cmd = OBDCommand("", "", "01", "23", 4, noop)
	assert cmd.get_command() == "0123" # simple concat of mode and PID


def test_get_mode_int():
	cmd = OBDCommand("", "", "01", "23", 4, noop)
	assert cmd.get_mode_int() == 0x01

	cmd = OBDCommand("", "", "", "23", 4, noop)
	assert cmd.get_mode_int() == 0


def test_get_pid_int():
	cmd = OBDCommand("", "", "01", "23", 4, noop)
	assert cmd.get_pid_int() == 0x23

	cmd = OBDCommand("", "", "01", "", 4, noop)
	assert cmd.get_pid_int() == 0

