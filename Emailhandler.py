import gmail
def send_credentials(email,name,acn,pwd):
    con=gmail.GMail("tamannasharma1029384756@gmail.com","afzs xpsq utkt cplu")
    body=f'''Hello {name},
    Welcome to ABC Bank, here is your credentials 
    Account No={acn}
    Password={pwd}

    Kindly change your password when you login first time

    ABC Bank
    Sector-16, Noida
'''
    msg=gmail.Message(
        to=email,
        subject="Your Credentials for Operating Acount",
        text=body)
    con.send(msg)

def send_otp(email,name,otp):
    con=gmail.GMail("tamannasharma1029384756@gmail.com","afzs xpsq utkt cplu")
    body=f'''Hello {name},
    Welcome to ABC Bank, here is your otp to recover password 
    otp={otp}

    
    ABC Bank
    Sector-16, Noida
'''
    msg=gmail.Message(
        to=email,
        subject="OTP for Password Recovery ",
        text=body)
    con.send(msg)


def send_otp_withdraw(email,name,otp,amt):
    con=gmail.GMail("tamannasharma1029384756@gmail.com","afzs xpsq utkt cplu")
    body=f'''Hello {name},
    Welcome to ABC Bank, here is your otp to withdraw {amt} 
    otp={otp}

    
    ABC Bank
    Sector-16, Noida
'''
    msg=gmail.Message(
        to=email,
        subject="OTP for Withdrawal",
        text=body)
    con.send(msg)


def send_otp_transfer(email,name,otp,amt,to_acn):
    con=gmail.GMail("tamannasharma1029384756@gmail.com","afzs xpsq utkt cplu")
    body=f'''Hello {name},
    Welcome to ABC Bank, here is your otp to Transfer Amount {amt} to ACN: {to_acn}
    otp={otp}

    
    ABC Bank
    Sector-16, Noida
'''
    msg=gmail.Message(
        to=email,
        subject="OTP for Transfer",
        text=body)
    con.send(msg)