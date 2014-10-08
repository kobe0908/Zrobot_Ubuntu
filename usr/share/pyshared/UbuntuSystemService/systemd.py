import socket
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)  

from UbuntuSystemService.utils import *
import os
import subprocess

class HostnameSystemdBackend(dbus.service.Object):
    """
    the backend implementing the hostnamed systemd interfaces
    """

    # some class properties
    DBUS_HOSTNAME_NAME = "org.freedesktop.hostname1"

    def __init__(self, bus=None):
        if bus is None:
            bus = dbus.SystemBus()
        bus_name = dbus.service.BusName(self.DBUS_HOSTNAME_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, "/org/freedesktop/hostname1")

        # Initialize properties
        try:
            f = open("/etc/hostname", "r")
            static_hostname = f.readline()
            f.close()
        except Exception:
            # We couldn't read /etc/hostname, so ignore
            static_hostname = socket.gethostname()

        self.properties = {
            "Hostname" : socket.gethostname(),
            "StaticHostname" : static_hostname,
            "PrettyHostname" : "",
            "IconName" : ""
            }

    # hostnamed interface
    @dbus.service.method(DBUS_HOSTNAME_NAME,
                         in_signature='sb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetHostname(self, name, user_interaction, sender=None, conn=None):
        """
        Set the current hostname
        """
        if not authWithPolicyKit(sender, conn,
                                 "org.freedesktop.hostname1.set-hostname",
                                 user_interaction):
            raise PermissionDeniedError("Permission denied by policy")

        if subprocess.call(["hostname", "-b", name]) != 0:
            raise PermissionDeniedError("Could not run hostname command")

        self.properties["Hostname"] = name
        self.PropertiesChanged(self.DBUS_HOSTNAME_NAME,
                               { "Hostname": name },
                               [])

        return

    @dbus.service.method(DBUS_HOSTNAME_NAME,
                         in_signature='sb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetStaticHostname(self, name, user_interaction, sender=None, conn=None):
        """
        Set the static hostname
        """
        if not authWithPolicyKit(sender, conn,
                                 "org.freedesktop.hostname1.set-static-hostname",
                                 user_interaction):
            raise PermissionDeniedError("Permission denied by policy")

        try:
            f = open("/etc/hostname", "w")
            f.write(name)
            f.close()

            self.properties["StaticHostname"] = name
            self.PropertiesChanged(self.DBUS_HOSTNAME_NAME,
                                   { "StaticHostname": name },
                                   [])
        except Exception:
            raise PermissionDeniedError("Can't write to /etc/hostname")

    @dbus.service.method(DBUS_HOSTNAME_NAME,
                         in_signature='sb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetPrettyHostname(self, name, user_interaction, sender=None, conn=None):
        """
        Set the pretty hostname
        """
        # We don't have a standard place to have this information,
        # so ignoring for now
        pass

    @dbus.service.method(DBUS_HOSTNAME_NAME,
                         in_signature='sb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetIconName(self, name, user_interaction, sender=None, conn=None):
        """
        Set icon name for this host
        """
        # We don't have a standard place to have this information,
        # so ignoring for now
        pass

    # Properties
    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='ss',
                         out_signature='v')
    def Get(self, interface_name, property_name):
        return self.properties[property_name]

    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface_name):
        if interface_name == self.DBUS_HOSTNAME_NAME:
            return self.properties
        else:
            raise dbus.exceptions.DBusException(
                'com.example.UnknownInterface',
                'The Foo object does not implement the %s interface'
                % interface_name)

    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='ssv')
    def Set(self, interface_name, property_name, new_value):
        # All our properties are read-only
        pass

    @dbus.service.signal(dbus.PROPERTIES_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        pass


class LocaleSystemdBackend(dbus.service.Object):
    """
    the backend implementing the localed systemd interfaces
    """

    # some class properties
    DBUS_LOCALE_NAME = "org.freedesktop.locale1"

    def __init__(self, bus=None):
        if bus is None:
            bus = dbus.SystemBus()
        bus_name = dbus.service.BusName(self.DBUS_LOCALE_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, "/org/freedesktop/locale1")

        # Initialize properties
        locale = []
        try:
            f = open("/etc/default/locale")
            for line in f:
                if line.startswith("LANG") or line.startswith("LC_"):
                    locale.append(line.strip('\n'))

            f.close()
        except Exception:
            pass

        (model, layout, variant, options) = get_keyboard_from_etc()
        self.properties = {
            "Locale" : locale,
            "VConsoleKeymap" : '',
            "VConsoleKeymapToggle" : '',
            "X11Layout" : layout,
            "X11Model" : model,
            "X11Variant" : variant,
            "X11Options" : options
            }

    # localed interface
    @dbus.service.method(DBUS_LOCALE_NAME,
                         in_signature='asb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetLocale(self, locale, user_interaction, sender=None, conn=None):
        """
        Set the system locale
        """
        if not authWithPolicyKit(sender, conn,
                                 "org.freedesktop.locale1.set-locale",
                                 user_interaction):
            raise PermissionDeniedError("Permission denied by policy")

        try:
            f = open("/etc/default/locale", "w")
            for line in locale:
                f.write(line + "\n")
            f.close();

            self.properties["Locale"] = locale
            self.PropertiesChanged(self.DBUS_LOCALE_NAME,
                                   { "Locale": locale },
                                   [])
        except Exception:
            raise PermissionDeniedError("Could not save to /etc/default/locale")

    @dbus.service.method(DBUS_LOCALE_NAME,
                         in_signature='ssbb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetVConsoleKeyboard(self, keymap, keymap_toggle, convert, user_interaction, sender=None, conn=None):
        """
        Set vconsole keyboard
        """
        if not authWithPolicyKit(sender, conn,
                                 "org.freedesktop.locale1.set-keyboard",
                                 user_interaction):
            raise PermissionDeniedError("Permission denied by policy")

    @dbus.service.method(DBUS_LOCALE_NAME,
                         in_signature='ssssbb',
                         out_signature='',
                         sender_keyword='sender',
                         connection_keyword='conn')
    def SetX11Keyboard(self, layout, model, variant, options, convert, user_interaction, sender=None, conn=None):
        """
        Set the keyboard for X11
        """
        if not authWithPolicyKit(sender, conn,
                                 "org.freedesktop.locale1.set-keyboard",
                                 user_interaction):
            raise PermissionDeniedError("Permission denied by policy")

        if set_keyboard_to_etc(model, layout, variant, options):
            self.properties["X11Layout"] = layout
            self.properties["X11Model"] = model
            self.properties["X11Variant"] = variant
            self.properties["X11Options"] = options

            self.PropertiesChanged(self.DBUS_LOCALE_NAME,
                                   { "X11Layout": layout,
                                     "X11Model": model,
                                     "X11Variant": variant,
                                     "X11Options": options },
                                   [])
        return
    
    # Properties
    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='ss',
                         out_signature='v')
    def Get(self, interface_name, property_name):
        return self.properties[property_name]

    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface_name):
        if interface_name == self.DBUS_LOCALE_NAME:
            return self.properties
        else:
            raise dbus.exceptions.DBusException(
                'com.example.UnknownInterface',
                'The Foo object does not implement the %s interface'
                % interface_name)

    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='ssv')
    def Set(self, interface_name, property_name, new_value):
        # All our properties are read-only
        pass

    @dbus.service.signal(dbus.PROPERTIES_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        pass
