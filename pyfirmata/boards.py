BOARDS = {
    'arduino' : {
        'digital' : tuple(x for x in range(24)),
        'analog' : tuple(x for x in range(14, 20)),
        'pwm' : (3, 5, 6, 9, 10, 11),
        'use_ports' : True,
        'disabled' : (0, 1, 20, 21, 22, 23) # Rx, Tx, Crystal
    },
    'arduino_mega' : {
        'digital' : tuple(x for x in range(54)),
        'analog' : tuple(x for x in range(16)),
        'pwm' : tuple(x for x in range(2,14)),
        'use_ports' : True,
        'disabled' : (0, 1, 14, 15) # Rx, Tx, Crystal
    }
}
