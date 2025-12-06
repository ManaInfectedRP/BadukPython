"""
Network multiplayer functionality for Baduk (Go) game
"""

import socket
import json
import threading


class GameServer:
    """Server for hosting a network multiplayer game."""
    
    def __init__(self, port=5555):
        """Initialize the game server."""
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.connected = False
        self.received_move = None
        self.lock = threading.Lock()
        
    def start(self):
        """Start the server and listen for connections."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind to all interfaces (0.0.0.0) to allow connections from other machines
            # This is necessary for network multiplayer functionality
            # Users should configure their firewall to control access
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(1)
            self.running = True
            
            # Start accept thread
            accept_thread = threading.Thread(target=self._accept_connection, daemon=True)
            accept_thread.start()
            
            return True
        except Exception as e:
            print(f"Error starting server: {e}")
            return False
    
    def _accept_connection(self):
        """Accept incoming connection."""
        try:
            self.server_socket.settimeout(1.0)
            while self.running and not self.connected:
                try:
                    client_socket, address = self.server_socket.accept()
                    self.client_socket = client_socket
                    self.connected = True
                    print(f"Client connected from {address}")
                    
                    # Start receive thread
                    receive_thread = threading.Thread(target=self._receive_data, daemon=True)
                    receive_thread.start()
                    break
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"Error accepting connection: {e}")
    
    def _receive_data(self):
        """Receive data from client."""
        while self.running and self.connected:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    self.connected = False
                    break
                    
                message = json.loads(data.decode('utf-8'))
                
                with self.lock:
                    if message['type'] == 'move':
                        self.received_move = message['data']
                    elif message['type'] == 'pass':
                        self.received_move = 'pass'
                        
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.connected = False
                break
    
    def send_move(self, row, col):
        """Send a move to the client."""
        if not self.connected or not self.client_socket:
            return False
            
        try:
            message = {
                'type': 'move',
                'data': {'row': row, 'col': col}
            }
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error sending move: {e}")
            self.connected = False
            return False
    
    def send_pass(self):
        """Send a pass to the client."""
        if not self.connected or not self.client_socket:
            return False
            
        try:
            message = {'type': 'pass'}
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error sending pass: {e}")
            self.connected = False
            return False
    
    def get_received_move(self):
        """Get the move received from the client."""
        with self.lock:
            move = self.received_move
            self.received_move = None
            return move
    
    def is_connected(self):
        """Check if a client is connected."""
        return self.connected
    
    def stop(self):
        """Stop the server."""
        self.running = False
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception:
                pass
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
    
    def get_local_ip(self):
        """Get the local IP address."""
        try:
            # Create a socket to find the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"


class GameClient:
    """Client for joining a network multiplayer game."""
    
    def __init__(self):
        """Initialize the game client."""
        self.socket = None
        self.connected = False
        self.received_move = None
        self.lock = threading.Lock()
    
    def connect(self, host, port):
        """Connect to a game server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((host, port))
            self.connected = True
            
            # Start receive thread
            receive_thread = threading.Thread(target=self._receive_data, daemon=True)
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False
    
    def _receive_data(self):
        """Receive data from server."""
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    self.connected = False
                    break
                    
                message = json.loads(data.decode('utf-8'))
                
                with self.lock:
                    if message['type'] == 'move':
                        self.received_move = message['data']
                    elif message['type'] == 'pass':
                        self.received_move = 'pass'
                        
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.connected = False
                break
    
    def send_move(self, row, col):
        """Send a move to the server."""
        if not self.connected or not self.socket:
            return False
            
        try:
            message = {
                'type': 'move',
                'data': {'row': row, 'col': col}
            }
            self.socket.send(json.dumps(message).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error sending move: {e}")
            self.connected = False
            return False
    
    def send_pass(self):
        """Send a pass to the server."""
        if not self.connected or not self.socket:
            return False
            
        try:
            message = {'type': 'pass'}
            self.socket.send(json.dumps(message).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error sending pass: {e}")
            self.connected = False
            return False
    
    def get_received_move(self):
        """Get the move received from the server."""
        with self.lock:
            move = self.received_move
            self.received_move = None
            return move
    
    def is_connected(self):
        """Check if connected to server."""
        return self.connected
    
    def disconnect(self):
        """Disconnect from the server."""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
