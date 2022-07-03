#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.message import Message


class Semafor(Agent):	

	class SemaforRadi(FSMBehaviour):
		async def on_start(self):
			print("Semafor je upaljen.")

		async def on_end(self):
			print("Kraj.")

	class ZelenoSvjetlo(State):
		
		msg_received = 0

		async def run(self):
		
			print("Zeleno svjetlo")
			print(f"Brojac: {self.agent.counter}")
			msg = await self.receive(timeout=1)
			
			if (msg):
				self.msg_received = 1
				if self.agent.counter < 6:
					self.agent.counter = 6
				print(f"Pjesak mora cekati {10 - self.agent.counter}")
				
			else:	
				if (self.msg_received):
					print(f"Pjesak mora cekati {10 - self.agent.counter}")
				self.agent.counter += 1
				if self.agent.counter > 10:
					self.agent.counter = 0
					self.msg_received = 0
					self.set_next_state("Zuto")
				else:
					self.set_next_state("Zeleno")

	class ZutoSvjetlo(State):
		async def run(self):
		
			print("Zuto svjetlo")
			time.sleep(1)
			print(f"Brojac: {self.agent.counter}")
			self.agent.counter += 1
			if self.agent.counter > 5:
				self.agent.counter = 0
				self.set_next_state("Crveno")
			else:
				self.set_next_state("Zuto")

	class CrvenoSvjetlo(State):
		async def run(self):
			msg = Message(
				to = "pjesak@localhost",
				body = f"Kreni!"
			)
			await self.send(msg)
			
			print("Crveno svjetlo")
			time.sleep(1)
			print(f"Brojac: {self.agent.counter}")
			self.agent.counter += 1
			if self.agent.counter > 10:
				self.agent.counter = 0
				self.set_next_state("Zeleno")
			else:
				self.set_next_state("Crveno")

	

	async def setup(self):
		print("Pogledaj na semafor!")
		self.counter = 0

		fsm = self.SemaforRadi()

		fsm.add_state(name="Zeleno", state=self.ZelenoSvjetlo(), initial=True)
		fsm.add_state(name="Zuto", state=self.ZutoSvjetlo())
		fsm.add_state(name="Crveno", state=self.CrvenoSvjetlo())


		fsm.add_transition(source="Zeleno", dest="Zuto")
		fsm.add_transition(source="Zuto", dest="Crveno")
		fsm.add_transition(source="Crveno", dest="Zeleno")
		fsm.add_transition(source="Zeleno", dest="Zeleno")
		fsm.add_transition(source="Zuto", dest="Zuto")
		fsm.add_transition(source="Crveno", dest="Crveno")


		self.add_behaviour(fsm)
		#msg_received = 0


if __name__ == '__main__':
	prvi = Semafor("semafor@localhost", "lozinka123")
	raskrizje = prvi.start()
	raskrizje.result()

	while prvi.is_alive():
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			break

	prvi.stop()
	quit_spade()
