def generator(result,type,name):
    prediction = result[0]
    probability = result[1]
    name = name.split(' ')
    fname = name[0]
    html = """\
    <html>
    <body style="background-color:white;">
        <p>Hi %s,<br>
        Your result = %s<br>
        Probability = %s%%<br>
        Thank you for using our %s<br>
        Be sure to provide feedback at our contact page.<br>
        Thanks,<br>
        Our team
        </p>
    </body>
    </html>
    """%(fname.capitalize(),prediction,probability,type)
    return html


if __name__ == "__main__":
    generator(('tumordetected','93%'),'brain')