import os
import queue
from plyer import notification
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import mixer

from textual import work
from textual.app import App, ComposeResult
from textual.worker import get_current_worker
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Placeholder, Static, TextArea, Button, Label

import network
from myglobals import messages_q

class ChatUI(App):
	CSS_PATH = "./assets/css/chat_ui.tcss"

	def __init__(self, conn, **kwargs):
		super().__init__(**kwargs)
		self.conn = conn
		self.sound = None

	def compose(self) -> ComposeResult:
		yield Container(
			VerticalScroll(
				id="messages"
			),
			TextArea(id="text"),
			Button("Send", id="send"),
			id="container",
		)
	
	def new_msg(self, content: str, role: str):
					new_msg = Container(
						Label(
							(content),
							classes=f"{role}msg"
						),
						classes=role
					)
					messages = self.query_one("#messages")
					messages.mount(new_msg)
					messages.scroll_end(animate=False)
	
	def on_mount(self) -> None:
		self.get_from_queue()
		mixer.init()
	
	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "send":
			textarea = self.query_one("#text")
			self.new_msg(textarea.text, "me")
			network.send(self.conn, textarea.text, network.PEER_PUBLIC_KEY)
			textarea.clear()
	
	def on_incoming_message(self, message: str) -> None:
		self.new_msg(message, "peer")
		notification.notify(
			title="lanchatty",
			message=message,
			timeout=5
		)
		self.sound = mixer.Sound("./assets/sounds/huh.mp3")
		self.sound.play()
	
	def on_disconnected(self, message, event) -> None:
		self.new_msg(message, event)
		self.notify(message, title=event, severity="error")
		self.sound = mixer.Sound("./assets/sounds/boom.mp3")
		self.sound.play()
	
	@work(thread=True)
	def get_from_queue(self) -> None:
		worker = get_current_worker()
		while not worker.is_cancelled:
			try:
				event, message = messages_q.get(timeout=0.5)
			except queue.Empty:
				continue
			if event == "message":
				self.call_from_thread(self.on_incoming_message, message)
			elif event == "disconnected":
				self.call_from_thread(self.on_disconnected, message, event)
				break
