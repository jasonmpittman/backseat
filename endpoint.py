from shared import tcp_socket_handler

socket_handler = tcp_socket_handler.TcpSocketHandler()

client_socket = socket_handler.create_client_socket_connect("localhost", 9999)

message = "Test to see if the tcp_socket_handler is working"

message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis in arcu at nisi finibus posuere id a est. Duis eget pretium libero. Maecenas vestibulum, lectus nec gravida laoreet, nisl dolor viverra felis, vel vulputate est nisl at sapien. Suspendisse sodales enim at ligula sodales varius. Integer imperdiet volutpat nibh a scelerisque. Etiam luctus commodo accumsan. Ut a massa orci. Mauris viverra, justo non accumsan suscipit, tellus arcu ultricies ex, id pharetra odio ante ut odio. Fusce interdum neque eget augue venenatis, at commodo orci elementum. Nulla facilisi. Donec in eleifend nisl. Nulla non faucibus nunc. Nam posuere, velit eu mollis efficitur, mi nunc sollicitudin neque, varius placerat lorem nunc a mauris. I can add event more characters without any issues whatsoever. Do you think that what-so-ever should have - in it? I do not know. Creative writting is always a key feature of my bad programming style."

socket_handler.send(client_socket, message, "public.pem", "private.pem")

# E = endpoint.Endpoint()
# E.run_local_command()
