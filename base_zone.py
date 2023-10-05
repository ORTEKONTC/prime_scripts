from script_base import Script
import API
import json
from event import *
import logging

logging.basicConfig(level=logging.INFO, format="%(name)s %(message)s")
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('/tmp/prime_script', 'a', encoding="UTF-8"))
logger.disabled = False


class BaseZone(Script):
    def __init__(self, uid, script_parameters):
        super().__init__(uid, script_parameters)
        self.send_event = None
        '''
        Функция инициализации скрипта.
        '''

        if "zoneId" in self.scriptParameters:
            self.zoneId = self.scriptParameters["zoneId"]

        if "partition" in self.scriptParameters:
            self.partitionId = self.scriptParameters["partition"]
        else:
            self.partitionId = 0

        if "Power_supply_12_24_V_resource" in self.scriptParameters:
            self.powerResourceId = self.scriptParameters["Power_supply_12_24_V_resource"]
            self.resource_to_zone(self.powerResourceId)

        if "AC_power_supply_resource" in self.scriptParameters:
            self.ac_powerResourceId = self.scriptParameters["AC_power_supply_resource"]
            self.resource_to_zone(self.ac_powerResourceId)

        if "Battery_resource" in self.scriptParameters:
            self.batteryResourceId = self.scriptParameters["Battery_resource_resource"]
            self.resource_to_zone(self.batteryResourceId)

        if "General_malfunction_resource" in self.scriptParameters:
            self.general_malfunctionResourceId = self.scriptParameters["General_malfunction_resource"]
            self.resource_to_zone(self.general_malfunctionResourceId)

        # TODO Добавить эти ресурсу по необходимости
        # if "Device_opening_resource" in self.scriptParameters:
        #     self.device_openingResourceId = self.scriptParameters["Device_opening_resource"]
        #     self.resource_to_zone(self.device_openingResourceId)
        #
        # if "Wall_detachment_resource" in self.scriptParameters:
        #     self.wall_detachmentResourceId = self.scriptParameters["Wall_detachment_resource"]
        #     self.resource_to_zone(self.wall_detachmentResourceId)

        if "Wired_interface_resource" in self.scriptParameters:
            self.wired_interfaceResourceId = self.scriptParameters["Wired_interface_resource"]
            self.resource_to_zone(self.wired_interfaceResourceId)

        if "Radio_channel_interface_resource" in self.scriptParameters:
            self.radio_channel_interfaceResourceId = self.scriptParameters["Radio_channel_interface_resource"]
            self.resource_to_zone(self.radio_channel_interfaceResourceId)

        if "Communication_control_resource" in self.scriptParameters:
            self.communication_controlResourceId = self.scriptParameters["Communication_control_resource"]
            self.resource_to_zone(self.communication_controlResourceId)

        if "WI_FI_interface_resource" in self.scriptParameters:
            self.wi_fi_interfaceResourceId = self.scriptParameters["WI_FI_interface_resource"]
            self.resource_to_zone(self.wi_fi_interfaceResourceId)

        if "Ethernet_interface_resource" in self.scriptParameters:
            self.ethernet_interfaceResourceId = self.scriptParameters["Ethernet_interface_resource"]
            self.resource_to_zone(self.ethernet_interfaceResourceId)

        if "USB_interface_resource" in self.scriptParameters:
            self.usb_interfaceResourceId = self.scriptParameters["USB_interface_resource"]
            self.resource_to_zone(self.usb_interfaceResourceId)

        if "Device_resource" in self.scriptParameters:
            self.deviceResourceId = self.scriptParameters["Device_resource"]
            self.resource_to_zone(self.deviceResourceId)

        self.set_initialized()

    def on_event(self, mess):
        """
        Основная функция для скрипта.
        """

        event = Event.to_event(mess)
        if event.get_class() in [Class.Sabotage, Class.Power, Class.Malfunction, Class.Connectivity]:
            event._source = ZoneSource(event.get_source().type, self.zoneId, self.partitionId)

        if event.get_class() == Class.Internal:
            if event.get_value()['command'] == 'reboot':
                self.send_event = Control(EVENTREASON_CONTROL_COMMAND,
                                          ZoneSource(event.get_source().type, self.zoneId, self.partitionId),
                                          event.get_activity())

                return json.dumps(self.send_event.to_message())

        return json.dumps(event.to_message())

    def resource_to_zone(self, resource_id):
        resource_events = API.get_resource_state(resource_id)
        if not resource_events:
            return 1

        else:
            for i in resource_events:
                event = Event.to_event(i)
                event._source = ZoneSource(event.get_source().type, self.zoneId, self.partitionId)
                API.post_message(json.dumps(event.to_message()))
                return True

            return False
