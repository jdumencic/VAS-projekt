#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.message import Message


class Pjesak(Agent):

	class PjesakSemafor(FSMBehaviour):
		async def on_start(self):
			print("Semafor je upaljen.")

		async def on_end(self):
			print("Kraj.")

	class Prijelaz(State):
		async def run(self):
		
			print("Nalazis se na pjesackom prijelazu.")
			tipka = input("Pritisni tipku: ")
			
			if (tipka):
				print("Cekaj da se zeleno svjetlo upali.")
				msg = Message(
					to = "semafor@localhost",
					body = "green"

				)
				await self.send(msg)
				self.set_next_state("Cekaj")
			else:
				self.set_next_state("Prijelaz")

	class Cekaj(State):
		async def run(self):
			
			print("Cekaj!")
			msg = await self.receive(timeout=1)
			if (msg):
				print(msg.body)
				self.set_next_state("Kreni")
			else:
				self.set_next_state("Cekaj")

	class Kreni(State):
		async def run(self):
		
			if (self.agent.counter < 5):
				print("Zeleno svjetlo")
			time.sleep(1)
			
			if (self.agent.counter < 5):
				print(f"Brojac: {self.agent.counter}")
			self.agent.counter += 1

			if self.agent.counter > 5:
				self.agent.counter = 0
				self.set_next_state("Prijelaz")
			else:
				self.set_next_state("Kreni")

	

	async def setup(self):
		print("Pogledaj na semafor!")
		self.counter = 0

		fsm = self.PjesakSemafor()

		fsm.add_state(name="Prijelaz", state=self.Prijelaz(), initial=True)
		fsm.add_state(name="Cekaj", state=self.Cekaj())
		fsm.add_state(name="Kreni", state=self.Kreni())


		fsm.add_transition(source="Prijelaz", dest="Cekaj")
		fsm.add_transition(source="Cekaj", dest="Kreni")
		fsm.add_transition(source="Kreni", dest="Prijelaz")
		fsm.add_transition(source="Prijelaz", dest="Prijelaz")
		fsm.add_transition(source="Cekaj", dest="Cekaj")
		fsm.add_transition(source="Kreni", dest="Kreni")


		self.add_behaviour(fsm)


if __name__ == '__main__':
	drugi = Pjesak("pjesak@localhost", "lozinka123")
	pPrijelaz = drugi.start()
	pPrijelaz.result()

	while drugi.is_alive():
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			break

	drugi.stop()
	quit_spade()
