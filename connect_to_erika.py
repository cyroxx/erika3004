from string import ascii_lowercase

from erika import Erika

with Erika("COM3") as meine_erika:
	meine_erika.print_ascii("Hallo")
	# meine_erika.print_ascii("#")
	# meine_erika.move_up()
	# meine_erika.move_up()
	# meine_erika.print_ascii("^")
	# meine_erika.move_right()
	# meine_erika.move_right()
	# meine_erika.print_ascii("#")
	# meine_erika.move_right()
	# meine_erika.move_right()
	# meine_erika.print_ascii("#")

	# meine_erika.move_down()
	# meine_erika.move_down()
	# meine_erika.print_ascii("#")

	# meine_erika.move_left()
	# meine_erika.move_left()

	# meine_erika.move_left()
	# meine_erika.move_left()
	# meine_erika.print_ascii("#")


	#meine_erika.demo()
#     # meine_erika.alarm(None)
# 	meine_erika.print_ascii("\r")
#     #meine_erika.print_ascii(input("Geben Sie Text ein:"))
# 	while True:
# 	 	print(meine_erika.read())#, end='', flush=True)
#%%
# with open("charTranslation.json", encoding="UTF-8") as f:
#            test = json.load(f)
