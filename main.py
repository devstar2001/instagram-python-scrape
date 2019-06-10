# pip install python-dotenv
import os
import dotenv
from pathlib import Path  # python3 only
from insta_bot import create_logger, create_driver, login_user, highlight_print


if __name__ == '__main__':
	env_path = Path('.') / '.env'
	dotenv.load_dotenv(dotenv_path=env_path)
	# --- input parameters ---
	insta_username = os.getenv("insta_username") or None
	insta_password = os.getenv("insta_password") or None
	headless = False
	proxy = os.getenv("proxy_address") or None
	# -----------------------------------

	# ------ proxy format ------
	# if user info(name and password) exists
	# proxy = 'login:password@ip:port'
	# if user info(name and password) does not exists
	# proxy = 'ip:port'
	# proxy = '77.232.163.176:8080'
	# ------------------------------------

	log_location = './logs'
	show_logs = False
	driver_location = "./chromedriver.exe"

	logger = create_logger(log_location, insta_username)
	driver, err_msg = create_driver(driver_location=driver_location,logger=logger, proxy=proxy, headless=headless)

	if driver:
		logged_in, message = login_user(driver,
										insta_username,
										insta_password,
										logger,
										log_location)
		if not logged_in:
			highlight_print(insta_username,
							message,
							"login",
							"critical",
							logger)
		else:
			message = "Logged in successfully!"
			highlight_print(insta_username,
							message,
							"login",
							"info",
							logger)
		# -------- login result messages(log_status) --------
		# 0	Logged in successfully!
		# 1	Suspicious Login Attempt
		# 2	Sorry, your password was incorrect. Please double-check your password.
		# 3	The username you entered doesn't belong to an account. Please check your username and try again.
		# 4	unknown login error

		if 'Logged' in message:
			log_status = 0
		elif 'Attempt' in message:
			log_status = 1
		elif 'your password' in message:
			log_status = 2
		elif 'your username' in message:
			log_status = 3
		else:
			log_status = 4

		driver.close()