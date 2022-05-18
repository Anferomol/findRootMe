# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_findRootMe
# Purpose:      Find accounts in the website: "Root-me.org".
#
# Author:      Andrés Felipe Rodriguez <anferomol@protonmail.com>
#
# Created:     14/05/2022
# Copyright:   (c) Andrés Felipe Rodríguez 2022
# Licence:     GPL
# -------------------------------------------------------------------------------


from spiderfoot import SpiderFootEvent, SpiderFootPlugin
import requests


class sfp_findRootMe(SpiderFootPlugin):

    meta = {
        'name': "findRootMe",
        'summary': "Find if the target has an account in: Rootme.org",
        'flags': [],
        'useCases': ["Footprint", "Passive"],
        'categories': ["Social Media", "Custom"],
        'dataSource': {
        	'website': "hhttps://www.github.com/anferomol/findRootMe",
        	'model': "FREE_NOAUTH_UNLIMITED",
        	'references': [
             			"https://www.github.com/anferomol/findRootMe"
		]
        }
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["USERNAME"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["USERNAME"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")
        
        if eventName != "USERNAME" and srcModuleName == "sfp_findRootMe":
        	self.debug(f"ignoring {eventName} :(")
        	return 

        try:
            data = None

            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            def getUsername(username):
            	url = f'https://www.root-me.org/{username}'
            	r = requests.get(url)
            	if r.status_code == 200:
            		return True
            	else:
            		return False

            if getUsername(eventData):
                evt = SpiderFootEvent("USERNAME", "Account Found", self.__name__, event)
                self.notifyListeners(evt)
            else:
                return 

            if not data:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return  
        
# End of sfp_findRootMe class
