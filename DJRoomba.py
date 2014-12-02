import create
import time
import music
import random
import socket

# windows version
# robot = create.Create(3)

# OSX version
robot = create.Create("/dev/tty.KeySerial1")

robot.toFullMode()

# Initial musical information
duration = 5
pitch_shift = 0
pentatonic = [60, 63, 65, 67, 70]
pentatonic_with_rest = [0, 1, 2, 60, 63, 65, 67, 70]

# Booleans for deciding whether to add rests
unbumped = True
add_rests = False

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = socket.gethostname()
server.bind((name, 443))
server.listen(5)

while True:
	sensors = robot.sensors([create.CLIFF_LEFT_SIGNAL, 
							 create.CLIFF_RIGHT_SIGNAL, 
							 create.CENTER_WHEEL_DROP,
							 create.RIGHT_BUMP,
							 create.LEFT_BUMP])

# Finish when pressing down center wheel
	if sensors[create.CENTER_WHEEL_DROP] == 0:
		break

	bumped = sensors[create.RIGHT_BUMP] or sensors[create.LEFT_BUMP]
	left_sensor_data = sensors[create.CLIFF_LEFT_SIGNAL]
	right_sensor_data = sensors[create.CLIFF_RIGHT_SIGNAL]

	if left_sensor_data < 50:
		pitch_shift = 1
	elif left_sensor_data < 250:
		pitch_shift = 6
	elif left_sensor_data < 700:
		pitch_shift = 11
	else:
		pitch_shift = 16

	if right_sensor_data < 50:
		tempo_shift = 4
	elif right_sensor_data < 250:
		tempo_shift = 3
	elif right_sensor_data < 700:
		tempo_shift = 2
	else:
		tempo_shift = 1

	shifted_duration = duration * tempo_shift

	print(right_sensor_data)


# If the bump sensor has been pressed and then released, flip value of add_rests
	if bumped and unbumped:	
		add_rests = not add_rests
		unbumped = False
	if (not bumped) and (not unbumped):
		unbumped = True 


	tuple_to_send = (pitch_shift, shifted_duration / 5)
	data_to_send = str(pitch_shift) + ":" + str(int(shifted_duration / 5))
	(client,address) = server.accept()

	
# If add_rests is true, play notes with randomly added rests, as well as elongate all note values
	if add_rests:
		pitch = random.choice(pentatonic_with_rest) + pitch_shift
		shifted_duration *= 3
	else:	
		pitch = random.choice(pentatonic) + pitch_shift


	if pitch < 50:
		data_to_send = "0:" + str(int(shifted_duration / 5))

	client.send(bytes(data_to_send, "utf-8"))
	client.close()

	robot.playNote(pitch, shifted_duration)

	print("pitch: " + str(pitch))
	print("duration: " + str(shifted_duration))

	time.sleep(shifted_duration/float(64))


		
