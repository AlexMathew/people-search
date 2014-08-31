import time
from itertools import izip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display


def check_spelling(browser):
	try:
		spell_fix = browser.find_element_by_xpath('//a[@class="spell"]').text
	except NoSuchElementException:
		spell_fix = None
	return spell_fix


def get_box_text_info(browser):
	try:
		box_text_info = browser.find_element_by_xpath('//div[@class="_Tgc"]').text
	except NoSuchElementException:
		box_text_info = None
	return box_text_info


def get_details(browser):
	try:
		name = browser.find_element_by_xpath('//div[@class="_eF"]').text
		title = browser.find_element_by_xpath('//div[@class="_Tfc"]').text
		more_info = browser.find_element_by_xpath('//div[@class="vk_arc"]')
		more_info.click()
	except NoSuchElementException:
		try:
			name = browser.find_element_by_xpath('//div[@class="kno-ecr-pt"]').text
			title = browser.find_element_by_xpath('//div[@class="_CLb"]').text
		except NoSuchElementException:
			name, title = None, None
	return {'name': name, 'title': title}


def get_description(browser):
	try:
		descr = browser.find_element_by_xpath('//div[@class="kno-rdesc"]/span').text
	except NoSuchElementException:
		descr = None
	return descr


def get_points(browser):
	try:
		points = {}
		headers = browser.find_elements_by_xpath('//span[@class="_xdb"]')
		values = browser.find_elements_by_xpath('//span[@class="kno-fv _lgc"]')
		for h, v in izip(headers, values):
			points[h.text] = v.text
	except NoSuchElementException:
		pass
	return points


def get_other_searches(browser):
	try:
		browser.find_elements_by_xpath('//a[@class="_Yqb"]')[-1].click()
		other_searches = [x.text for x in browser.find_elements_by_xpath('//div[@class="kltat"]')]
	except (NoSuchElementException, IndexError):
		other_searches = None
	return other_searches


def scrape_page(query):
	display = Display(visible=0, size=(800, 600))
	display.start()
	browser = webdriver.Firefox()
	browser.get('http://google.com')
	inp = browser.find_element_by_xpath('//input[@id="gbqfq"]')
	inp.send_keys(query)
	inp.send_keys(Keys.ENTER)
	time.sleep(5)
	spell_fix = check_spelling(browser)
	box_text_info = get_box_text_info(browser)
	details = get_details(browser)
	description = get_description(browser)
	points = get_points(browser)
	other_searches = get_other_searches(browser)
	browser.quit()
	display.stop()
	data = {
		'spell': spell_fix,
		'box_text': box_text_info,
		'details': details,
		'description': description,
		'points': points,
		'other_searches': other_searches
	}
	return data	