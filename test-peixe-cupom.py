#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2015 Daniel Cunha <danielsoro@gmail.com>
# Copyright (C) 2015 Ricardo Dantas <licensed@gmail.com>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import click

def do_login(driver, username, password):
    emailInput = driver.find_element_by_name(u'email')
    emailInput.send_keys(username)

    password_input = driver.find_element_by_name(u'password')
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

def do_valid_code(driver, url, type, number):
    try:
        driver.execute_script(u"jQuery('.promocode-field').show()")
        ticket_number = "%s%04i" % (type, number)
        candidate_promocode_input = driver.find_element_by_id(u'candidatePromocode')
        candidate_promocode_input.clear()
        candidate_promocode_input.send_keys(ticket_number)
        candidate_promocode_input.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)

        if driver.find_element_by_class_name(u'error-box') == None:
            print u"It's a valid ticket %s" % ticket_number

    except StaleElementReferenceException:
        driver.get(url)
        do_valid_code(driver, url, type, number)

@click.command()
@click.option('--username', required='True', help=u'Username para login no peixeurbano')
@click.option('--password', required='True', help=u'Passsword para login no peixeurbano')
@click.option('--types', default='E', type=(str), help=u'Define o tipo do parâmetro: E - Email | F - Facebook')
@click.option('--url', required='True', help=u'URL da promoção para ser feito o teste do cupom')
def valid_promocupom(username, password, types, url):
    print u'Username: %s\nPassword: %s\nType: %s\nURL: %s' % (username, password, types, url)
    driver = webdriver.Firefox()
    driver.get(url)
    do_login(driver, username, password)
    for type in types:
        print u'Testing tickets for %s type' % type
        for number in range(0000, 9999):
            do_valid_code(driver, url, type, number)

if __name__ == u'__main__':
    valid_promocupom()
