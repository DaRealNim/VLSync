import dbus
import threading
import socket
import datetime
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

def seekSignal(*args, **kwargs):
    # print(args, kwargs)
    print("Sending seek to clients ("+str(datetime.timedelta(seconds=int(args[0].real/1e6)))+")")
    for client in clientsocks:
        client.send(b"\x01"+args[0].to_bytes(16, "big"))


def propertyChangedSignal(*args, **kwargs):
    # print(list(args))
    if args[0] == "org.mpris.MediaPlayer2.Player":
        if "PlaybackStatus" in args[1]:
            print(args[1]["PlaybackStatus"])




def handleClients():
    global mainsock, clientsocks
    while True:
        conn, ip = mainsock.accept()
        print("Got connection from "+ip[0]+":"+ip[1])
        clientsocks.append(conn)

def mainThread():
    pass


def main():
    global mainsock, clientsocks, bus, player, interface
    DBusGMainLoop(set_as_default=True)
    print("REDDIT MOMENT")
    # dbus.set_default_main_loop(dbus.mainloop.NativeMainLoop)
    mainsock = socket.socket()
    mainsock.bind(("0.0.0.0", 42069))
    mainsock.listen(0)
    clientsocks = []
    threading.Thread(target=handleClients).start()
    bus = dbus.SessionBus()
    player = bus.get_object('org.mpris.MediaPlayer2.vlc', '/org/mpris/MediaPlayer2')
    interface = dbus.Interface(player, dbus_interface='org.mpris.MediaPlayer2.Player')
    bus.add_signal_receiver(seekSignal, "Seeked", "org.mpris.MediaPlayer2.Player")
    bus.add_signal_receiver(propertyChangedSignal, "PropertiesChanged", "org.freedesktop.DBus.Properties")
    loop = GLib.MainLoop()
    loop.run()


if __name__ == '__main__':
    main()
