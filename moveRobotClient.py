import socket
import create

# robot = create.Create(3)
# forward = 0
# rotate = 0


while True:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('10.159.220.225', 8082))
	data = client.recv(1024)
	data = str(data)

	list_of_data = data.split(":")
	forward = ''.join(x for x in list_of_data[0] if x.isdigit())
	rotate = ''.join(x for x in list_of_data[1] if x.isdigit())

	forward = int(forward)
	rotate = int(rotate)


	
	forward *= 5
	rotate *= 10


	if forward == 0:
		rotate = 0
	if forward == 5:
		forward = -50
	if forward == 30:
		forward = -25
	if forward == 55:
		forward = 25
	if forward == 80:
		forward = 50

	if rotate == 10:
		roate = 360
	if rotate == 20:
		rotate = 270
	if rotate  == 30:
		rotate = 180
	if rotate == 40:
		rotate = 90


	print("forward: " + str(forward))
	print("rotate: " + str(rotate))


	# robot.go(forward,rotate)