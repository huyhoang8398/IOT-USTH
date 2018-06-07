import gammu
sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()
data = ''
with open('/home/pi/scann/test.txt', 'r') as myfile:
    data = myfile.read()
message = {
        'Text': data,
        'SMSC': {'Location': 1},
        'Number': '+84984420826',
}

sm.SendSMS(message)
