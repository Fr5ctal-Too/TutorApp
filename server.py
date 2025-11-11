from config import SERVER_HOST, SERVER_PORT

import json
import socket
import threading
from enum import Enum


class MessageType(Enum):
    CHAT = 'chat'
    STATUS = 'status'
    SYSTEM = 'system'
    REGISTER = 'register'
    QUESTION = 'question'
    DUEL_REQUEST = 'duel_request'
    DUEL_SCORE = 'duel_score'


class ChatServer:

    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.lock = threading.Lock()

        self.waiting_clients = {}
        self.client_info = {}
        self.active_pairs = []


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f'Server started on {self.host}:{self.port}')
        print('Waiting for clients to connect...')

        while True:
            client_socket, address = self.server_socket.accept()

            print(f'New connection from {address}')

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.daemon = True

            client_thread.start()


    def handle_client(self, client_socket, address):
        try:
            registered = False

            while True:
                data = client_socket.recv(4096)

                if not data:
                    break

                try:
                    message_dict = json.loads(data.decode('utf-8'))

                    if 'type' not in message_dict:
                        print(f'Invalid message format from {address}: missing type field')
                        continue

                    msg_type = message_dict.get('type')

                    if msg_type == MessageType.REGISTER.value and not registered:
                        subject = message_dict.get('subject')
                        role = message_dict.get('role')

                        if not subject or not role:
                            print(f'Invalid registration from {address}')
                            continue

                        print(f'Client {address} registered: subject={subject}, role={role}')

                        with self.lock:
                            self.client_info[client_socket] = {'subject': subject, 'role': role}

                            partner_role = 'tutor' if role == 'learn' else 'learn'
                            match_key = (subject, partner_role)

                            if match_key in self.waiting_clients and len(self.waiting_clients[match_key]) > 0:
                                partner_socket = self.waiting_clients[match_key].pop(0)

                                if len(self.waiting_clients[match_key]) == 0:
                                    del self.waiting_clients[match_key]

                                pair = (client_socket, partner_socket)
                                self.active_pairs.append(pair)

                                print(f'Matched two clients for {subject}: {role} <-> {partner_role}')

                                self.send_status(client_socket, 'connected', 'Connected! You can now chat.')
                                self.send_status(partner_socket, 'connected', 'Connected! You can now chat.')
                            else:
                                wait_key = (subject, role)
                                if wait_key not in self.waiting_clients:
                                    self.waiting_clients[wait_key] = []
                                self.waiting_clients[wait_key].append(client_socket)

                                print(f'Client {address} waiting for: subject={subject}, looking for={partner_role}')
                                self.send_status(client_socket, 'waiting', f'Waiting for a {partner_role} in {subject}...')

                        registered = True

                    elif msg_type == MessageType.CHAT.value:
                        if not registered:
                            print(f'Client {address} tried to chat without registering')
                            continue

                        partner = self.find_partner(client_socket)
                        if partner:
                            try:
                                partner.send(data)
                            except:
                                print('Failed to send message to partner')
                                break

                    elif msg_type == MessageType.QUESTION.value:
                        if not registered:
                            print(f'Client {address} tried to send question without registering')
                            continue

                        partner = self.find_partner(client_socket)
                        if partner:
                            try:
                                partner.send(data)
                                print(f'Question forwarded to partner')
                            except:
                                print('Failed to send question to partner')
                                break

                    elif msg_type == MessageType.DUEL_REQUEST.value:
                        if not registered:
                            print(f'Client {address} tried to send duel request without registering')
                            continue

                        partner = self.find_partner(client_socket)
                        if partner:
                            try:
                                partner.send(data)
                                print(f'Duel request forwarded to partner')
                            except:
                                print('Failed to send duel request to partner')
                                break

                    elif msg_type == MessageType.DUEL_SCORE.value:
                        if not registered:
                            print(f'Client {address} tried to send duel score without registering')
                            continue

                        partner = self.find_partner(client_socket)
                        if partner:
                            try:
                                partner.send(data)
                                print(f'Duel score forwarded to partner')
                            except:
                                print('Failed to send duel score to partner')
                                break
                    else:
                        print(f'Ignoring message type: {msg_type}')

                except json.JSONDecodeError:
                    print(f'Invalid JSON from {address}')
                    continue
                except Exception as e:
                    print(f'Error processing message from {address}: {e}')
                    continue

        except Exception as e:
            print(f'Error handling client {address}: {e}')

        finally:
            self.disconnect_client(client_socket)
            client_socket.close()

            print(f'Client {address} disconnected')


    def find_partner(self, client_socket):
        for pair in self.active_pairs:
            if pair[0] == client_socket:
                return pair[1]
            elif pair[1] == client_socket:
                return pair[0]
        return None


    def disconnect_client(self, client_socket):
        with self.lock:
            if client_socket in self.client_info:
                info = self.client_info[client_socket]
                wait_key = (info['subject'], info['role'])

                if wait_key in self.waiting_clients and client_socket in self.waiting_clients[wait_key]:
                    self.waiting_clients[wait_key].remove(client_socket)
                    if len(self.waiting_clients[wait_key]) == 0:
                        del self.waiting_clients[wait_key]

                del self.client_info[client_socket]

            partner = self.find_partner(client_socket)

            if partner:
                try:
                    self.send_status(partner, 'disconnected', 'Partner disconnected')
                except:
                    pass

                self.active_pairs = [pair for pair in self.active_pairs if client_socket not in pair]


    def send_message(self, client_socket, message_dict):
        try:
            message = json.dumps(message_dict)
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f'Error sending message: {e}')


    def send_status(self, client_socket, status_code, message):
        status_message = {
            'type': MessageType.STATUS.value,
            'status': status_code,
            'message': message
        }
        self.send_message(client_socket, status_message)


    def send_chat(self, client_socket, content, sender=None):
        chat_message = {
            'type': MessageType.CHAT.value,
            'content': content
        }
        if sender:
            chat_message['sender'] = sender
        self.send_message(client_socket, chat_message)


server = ChatServer()
server.start()
