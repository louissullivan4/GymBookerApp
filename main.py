# Gymbooker: Console Application that will uses selenium to book my gym session for me for that day.
# Louis Sullivan 13/07/2021

from selenium import webdriver
import time
from datetime import datetime
import tkinter as tk


def getTimes():
	"""
	Getting all available times for that day. Some are missing based on what time of day your booking.

	@return: hourslist: list of hours available
	"""
	# hides chrome browser
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
				 "Chrome/85.0.4183.83 Safari/537.36 "
	options = webdriver.ChromeOptions()
	options.headless = True
	options.add_argument(f'user-agent={user_agent}')
	options.add_argument("--window-size=1920,1080")
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--allow-running-insecure-content')
	options.add_argument("--disable-extensions")
	options.add_argument("--proxy-server='direct://'")
	options.add_argument("--proxy-bypass-list=*")
	options.add_argument("--start-maximized")
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
	today = datetime.today()
	now = today.strftime('%Y-%m-%d')
	# links to website with pre filled form in url
	driver.get(
		"https://splashworld.legendonlineservices.co.uk/enterprise/ticketing/browse?StartDate=" + now + "&ActivityId=2 "
																										"&LocationId=3 "
																										"&ResourceId=8")
	# every sleep is to allow site to load
	time.sleep(7)
	# get the list of times available on site
	calendertable = driver.find_elements_by_class_name("time")
	time.sleep(3)
	hourslist = []
	# add each to list
	for text in calendertable:
		if text.text != '':
			hourslist.append(text.text)
	print(now)
	print(hourslist)
	return hourslist


def gymformfiller(buttontime):
	"""
	Access the website directly and fills everything out

	"""
	today = datetime.today()
	now = today.strftime('%Y-%m-%d')
	try:
		web = webdriver.Chrome()
		web.get(
			"https://splashworld.legendonlineservices.co.uk/enterprise/ticketing/browse?StartDate=" + now + "&ActivityId=2 "
																											"&LocationId=3 "
																											"&ResourceId=8")
		time.sleep(6)
		# clicks the correct time thats is selected by user
		web.find_element_by_xpath("//*[contains(text(),'" + str(buttontime) + "')]").click()
		time.sleep(3)
		# drop down menu fill out
		dropdownmenu = web.find_element_by_xpath(
			'/html/body/div[1]/div[2]/div/booking-tickets-base/div[3]/form/div/div['
			'1]/div/div[1]/ticket-selection/div/div/div[1]')
		dropdownmenu.click()
		time.sleep(5)
		# memeber number left out for Github sorry it wont work from here :(
		membernum = '------'
		# adds member number to form
		membernumadd = web.find_element_by_xpath(
			'/html/body/div[1]/div[2]/div/booking-tickets-base/div[3]/form/div/div['
			'1]/div/div[1]/ticket-selection/div/div/div[2]/div/div/div['
			'1]/div/input-text-button-group/div/div/input')
		membernumadd.send_keys(membernum)
		# clicks submit member button
		addbut = web.find_element_by_xpath('//*[@id="collapsible-ticket-panel-0"]/div/div/div['
										   '1]/div/input-text-button-group/div/div/span/button-primary/button')
		addbut.click()

		time.sleep(3)
		# opens rules and agrees to them
		rulesopen = web.find_element_by_xpath('//*[@id="basket-summary-base"]/div['
											  '1]/booking-summary-base/booking-details/div[1]/div[2]/button[1]')
		rulesopen.click()

		time.sleep(3)
		rulesaccept = web.find_element_by_xpath(
			'//*[@id="basket-summary-base"]/div[1]/booking-summary-base/booking-details/div[2]/div/div/div['
			'3]/button-primary/button')
		rulesaccept.click()

		time.sleep(3)
		# add to basket button clicked
		basketadd = web.find_element_by_xpath('//*[@id="basket-summary-base"]/div[2]/submit-action/button')
		basketadd.click()

		time.sleep(8)
		# another click
		web.find_element_by_xpath(
			'//*[@id="universal-basket-process-request"]/div[2]/div['
			'2]/universal-basket-options/universal-basket-continue-options/button[1]').click()

		# adds email to submission box
		email = "sullivanlouis0@gmail.com"
		time.sleep(6)
		web.find_element_by_xpath('//*[@id="universal-basket-email-address"]').send_keys(email)
		time.sleep(3)
		# adds confirmation email to submission box
		web.find_element_by_xpath('//*[@id="universal-basket-confirm-email-address"]').send_keys(email)
		time.sleep(3)
		# clicks accept
		web.find_element_by_xpath('//*[@id="universal-basket-process-request"]/div[2]/div[1]/div['
								  '4]/universal-basket-payment-details/div/div/div['
								  '5]/universal-basket-terms-conditions/ul/li/div[1]/label/span[2]/i').click()
		time.sleep(4)
		# clicks submit
		web.find_element_by_xpath('//*[@id="universal-basket-process-request"]/div[2]/div['
								  '2]/universal-basket-options/universal-basket-continue-options/button[1]').click()
		print("Done! :)")

	except Exception as e:
		print("Oops! Looks like something went wrong :(")


def main():
	# creating tkinter canvas
	root = tk.Tk()

	canvas1 = tk.Canvas(root, width=300, height=600)
	root.title("GYM TIMES AVAILABLE")
	canvas1.pack()

	# gets current times
	hourslist = getTimes()
	i = 2

	for j in range(len(hourslist)):
		# display the times as button to be selected
		e = tk.Button(canvas1, text=str(hourslist[j]), command=lambda
			buttontime = str(hourslist[j]): gymformfiller(buttontime))
		e.grid(row=i, column=j, padx=10, pady=10)

	root.mainloop()


if __name__ == '__main__':
	main()
