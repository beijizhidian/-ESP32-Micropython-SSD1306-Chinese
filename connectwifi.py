def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Tp-158327', 'gp2018.11.14.')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
