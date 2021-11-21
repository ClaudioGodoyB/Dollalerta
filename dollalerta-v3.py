import pandas as pd
import requests
import json
import datetime
import smtplib
import time
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from bs4 import BeautifulSoup


class scraper():

    def __init__(self):
        return

    def kambista(self):
        url = 'https://api.kambista.com/v1/exchange/calculates?originCurrency=USD&destinationCurrency=PEN&amount=1500&active=S'
        response = requests.get(url)
        response = json.loads(response.content)

        compra_kambista = response['tc']['bid']
        venta_kambista = response['tc']['ask']

        return compra_kambista, venta_kambista

    def rextie(self):

        url = 'https://app.rextie.com/api/v1/fxrates/rate/?origin=home'
        response = requests.post(url)
        response = json.loads(response.content)
        compra_rextie = response['fx_rate_buy']
        venta_rextie = response['fx_rate_sell']

        return compra_rextie, venta_rextie

    def tkambio(self):

        url = 'https://tkambio.com/wp-admin/admin-ajax.php'
        payload = {'action': 'get_exchange_rate'}
        response = requests.post(url, data=payload)
        print(response.content)
        try:
            response = json.loads(response.content)
            compra_tkambio = response['buying_rate']
            venta_tkambio = response['selling_rate']
        except ValueError:
            compra_tkambio = 0
            venta_tkambio = 0

        return compra_tkambio, venta_tkambio

    def cocosylucas(self):

        url = "https://www.cocosylucasbcp.com/toc"
        payload = {}
        headers = {
        'authority': 'www.cocosylucasbcp.com',
        'method': 'POST',
        'path': '/toc',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-ES,es;q=0.9',
        'app-code': 'MY',
        'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'cookie': 'HttpOnly; ARRAffinity=bfc34834a03c79d6564594b08177bd00f9106395d1d6d297eab30187120174cb; visid_i$',
        'origin': 'https://www.cocosylucasbcp.com',
        'referer': 'https://www.cocosylucasbcp.com/dolar-hoy',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'}

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.content)
        token = response['access_token']

        url = "https://www.cocosylucasbcp.com/poly/currency-exchanges"
        payload = {}
        headers = {
        'authority': 'www.cocosylucasbcp.com',
        'path': '/poly/currency-exchanges',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-ES,es;q=0.9',
        'app-code': 'MY',
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json; charset=utf-8',
        'cookie': 'HttpOnly; HttpOnly; ARRAffinity=bfc34834a03c79d6564594b08177bd00f9106395d1d6d297eab30187120174cb; visid_incap_2165179=xDRCjtV2Qtemwj6kv1i7HWw4kl4AAAAAQUIPAAAAAACZusCSyTQsTZjYqY$',
        'referer': 'https://www.cocosylucasbcp.com/dolar-hoy',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.content)
        if response['status']['code'] == 'MYV014':
            cyl_compra = 0
            cyl_venta = 0
        else:
            cyl_compra = response['currencyExchangeList'][5]['ratePurchase']
            cyl_venta = response['currencyExchangeList'][5]['rateSale']

        return cyl_compra, cyl_venta

    def tucambista(self):

        url = 'https://app.tucambista.pe/api/transaction/getquote/500/USD/BUY/'
        r = requests.get(url)
        valores = json.loads(r.content)

        tucambista_compra = valores['buyExchangeRate']
        tucambista_venta = valores["sellExchangeRate"]
        return tucambista_compra,tucambista_venta

    def dollarhouse(self):

        url = 'https://app.dollarhouse.pe/calculadora'
        response = requests.get(url)
        data = BeautifulSoup(response.content, 'html.parser')
        dollarhouse_venta = data.find('input', {'name': 'op_saleprice'}).get('value')
        dollarhouse_compra = data.find('input', {'name': 'purchaseprice'}).get('value')
        return dollarhouse_compra, dollarhouse_venta

    def euroXE(self):

        url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=PEN"
        response = requests.get(url)
        soup = BeautifulSoup( response.content, 'html.parser')
        data = soup.findAll("p",{"class":"result__BigRate-sc-1bsijpp-1 iGrAod"})
        euro = data[0].text[0:5]
        return euro


class getUsers():

    def __init__(self):
        return

    def getSheets(self):
        SERVICE_ACCOUNT_FILE = #AQUI VAN LAS KEYS DEL SERVICIO DE GOOGLE
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        creds = None
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        SAMPLE_SPREADSHEET_ID = # AQUÍ DEBE IR EL ID DE TU SHEET EN MI CASO ERA DONDE ESTABAN LOS MAILS

        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="respuestas!A2:G180").execute()
        values = result.get('values', [])
        df = pd.DataFrame(values, columns=[
                          'Fecha_inscrito', 'nombre', 'apellido', 'correo', 'frecuencia', 'casas conocidas', 'Enviar'])
        base = df.loc[df['Enviar'] == 'Sí']
        now = datetime.datetime.now()
        
        #AQUÍ SE DEFINE LAS REGLAS DE HORAS PARA HACER LOS ENVÍOS
        if now.hour == 14:
            base = base.loc[(base['frecuencia'] == 'Turno 1: 9:15 a.m') | (
                base['frecuencia'] == 'Turno 2: 9:15 y 13:15') | (base['frecuencia'] == 'Turno 3: 9:15 , 13:15 y 17:45')]
        elif now.hour == 18:
            base = base.loc[(base['frecuencia'] == 'Turno 2: 9:15 y 13:15') | (base['frecuencia'] == 'Turno 3: 9:15 , 13:15 y 17:45')]
        else:
            base = base.loc[base['frecuencia'] ==
                'Turno 3: 9:15 , 13:15 y 17:45']
        self.base = base
        return base

class mail():

    def __init__(self, tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9, tc10, tc11, tc12, tc13):
        self.tc1 = tc1
        self.tc2 = tc2
        self.tc3 = tc3
        self.tc4 = tc4
        self.tc5 = tc5
        self.tc6 = tc6
        self.tc7 = tc7
        self.tc8 = tc8
        self.tc9 = tc9
        self.tc10 = tc10
        self.tc11 = tc11
        self.tc12 = tc12
        self.tc13 = tc13
        return

    def sendMail(self, correo, name):
        now = datetime.datetime.now()
        hora = str(int(now.hour) - int(5))
        if int(hora) > 24:
            hora = int(hora)-24
        me = #AQUÍ VA TU CORREO DESDE DONDE SALE EL MAIL
        msg = MIMEMultipart('alternative')
        msg['Subject'] = #AQUÍ VA EL ASUNTO DEL MAIL
        msg['From'] = me
        msg['To'] = correo
        html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div style="height: 100%;">
        <a href="">
            <img src="cid:image1"  style="width: 100%;" >
        </a>
    </div>
    <div style="text-align: center; border-bottom: 10px; background-color: #DDF1FF;border-radius: 25px;">
        <h1 style="font: bold;">Dollalerta</h1>
        <h4> Flash de las {hora} horas </h4>
    </div>
    <br>
    <div style="background-color:#EBF8FF;border-radius: 25px;">
        <br>
        <p style=" margin-left: 3px;">Hola {name},</p>
        <table style="border-collapse: collapse; margin: 25px 0; font-size: 0.9em; border: 1px solid black; width: 100%;">
            <thead>
                <tr style= "background-color: #EDFFEF; text-align: center; border: 1px solid black;">
                    <tr style= "background-color: #EDFFEF; text-align: center; border: 1px solid black;">
                    <th style= "border: 1px solid black;">Casa</th>
                    <th style= "border: 1px solid black;">Compra</th>
                    <th style= "border: 1px solid black;">Venta</th>
                    <th style= "border: 1px solid black;">Web</th>
                </tr>
            </thead>
            <tbody>
                <tr style= "text-align: center; border: 1px solid black">
                    <td style= "border: 1px solid black;">Kambista</td>
                    <td style= "border: 1px solid black;">S/{self.tc1}</td>
                    <td style= "border: 1px solid black;">S/{self.tc2}</td>
                    <td style= "border: 1px solid black;"><a href="https://bit.ly/3AfSBTB"><button>IR</button></a></td>
                </tr>
                <tr style= "text-align: center; border: 1px solid black">
                    <td style= "border: 1px solid black;">Rextie</td>
                    <td style= "border: 1px solid black;">S/{self.tc3}</td>
                    <td style= "border: 1px solid black;">S/{self.tc4}</td>
                    <td style= "border: 1px solid black;"><a href="https://bit.ly/364t7L4"><button>IR</button></a></td>
                </tr>
                <tr style= "text-align: center; border: 1px solid black">
                    <td style= "border: 1px solid black;">Tkambio</td>
                    <td style= "border: 1px solid black;">S/{self.tc5}</td>
                    <td style= "border: 1px solid black;">S/{self.tc6}</td>
                    <td style= "border: 1px solid black;"><a href="https://bit.ly/3x52Zvo"><button>IR</button></a></td>
                </tr>
                <tr style= "text-align: center; border: 1px solid black">
                    <td style= "border: 1px solid black;">Cocos y Lucas</td>
                    <td style= "border: 1px solid black;">S/{self.tc7}</td>
                    <td style= "border: 1px solid black;">S/{self.tc8}</td>
                    <td style= "border: 1px solid black;"><a href="https://bit.ly/3w8ySC2"><button>IR</button></a></td>
                </tr>
                    <tr style= "text-align: center; border: 1px solid black">
                    <td style= "border: 1px solid black;">Tu Cambista</td>
                    <td style= "border: 1px solid black;">S/{self.tc9}</td>
                    <td style= "border: 1px solid black;">S/{self.tc10}</td>
                    <td style= "border: 1px solid black;"><a href="https://bit.ly/3dW5oBb"><button>IR</button></a></td>
                </tr>
                </tr>
                    <tr style= "text-align: center; border: 1px solid black">
                    <td style= "border: 1px solid black;">Dollarhouse</td>
                    <td style= "border: 1px solid black;">S/{self.tc11}</td>
                    <td style= "border: 1px solid black;">S/{self.tc12}</td>
                    <td style= "border: 1px solid black;"><a href="https://bit.ly/3zjq0vp"><button>IR</button></a></td>
                </tr>
            </tbody>
        </table>
       <br>
       <h6> Euros </h6>
        <table style="border-collapse: collapse; margin: 25px 0; font-size: 0.9em; border: 1px solid black; width: 100%;">
         <thead>
          <tr style= "background-color: #EDFFEF; text-align: center; border: 1px solid black;">
            <th style= "border: 1px solid black;">Fuente</th>
            <th style= "border: 1px solid black;">Tasa Promedio</th>
            <th style= "border: 1px solid black;">Web</th>
          </tr>
        </thead>
        <tbody>
          <tr style= "text-align: center; border: 1px solid black">
            <td style= "border: 1px solid black;">XE</td>
            <td style= "border: 1px solid black;">S/ {self.tc13} </td>
            <td style= "border: 1px solid black;"><a href="https://bit.ly/3q91lbp"><button>IR</button></a></td>
          </tr>
         </tbody>
        </table>
        <div>
            <p style=" margin-left: 3px;">¿Te gustaría dejar de recibir esta información, o cambiar tu frecuencia? o ¿Conoces a alguien que le gustaría recibir esta alerta? Puedes reenviar el siguiente <a href="https://forms.gle/TK6rHDBHHYstWZG6$
        </div>
    </div>

</body>
</html>
"""
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        #AQUI VA LA IMAGEN QUE ADJUNTÉ EN EL HEADER
        fp = open('/home/claudiogodoyb/logo.jpeg', 'rb') 
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

        username = #AQUÍ VA TU CORREO DESDE DONDE SALE EL MAIL
        password = #AQUÍ VA LA CLAVE GENERADA PARA PODER USAR DESDE APPS EXTERNAS A GMAIL EN MI CASO
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(me, str(correo), msg.as_string())
        server.quit()

#ESTA CLASS ACTUALIZA DATOS EN UN JSON Y GENERA UNA GRÁICA DE TENDENCIA PROMEDIO DEL TC
class graficaDatos():

    def __init__(self, lista):
        self.lista = lista
        return

    #UPDATE DE DATOS
    def actualizaDatos(self):
        now = datetime.datetime.now()
        if now.hour == 14:
            f = open('/home/claudiogodoyb/programas/tc_historico.json', 'r')
            data = json.load(f)
            print(data)
            data['dias']['hace_5']['avg'] = data['dias']['hace_4']['avg']
            data['dias']['hace_4']['avg'] = data['dias']['hace_3']['avg']
            data['dias']['hace_3']['avg'] = data['dias']['hace_2']['avg']
            data['dias']['hace_2']['avg'] = data['dias']['ayer']['avg']
            data['dias']['ayer']['avg'] = data['dias']['hoy']['avg']
            print(data)
            f = open('/home/claudiogodoyb/programas/tc_historico.json', 'w')
            json.dump(data, f)
            print(data)
            f.close()

            f = open('/home/claudiogodoyb/programas/tc_historico.json', 'r')
            data = json.load(f)
            lista_avg = self.lista
            avg_day = round(sum(lista_avg)/len(lista_avg), 2)
            data['dias']['hoy']['avg'] = avg_day
            print(data)
            f = open("/home/claudiogodoyb/programas/tc_historico.json", "w")
            json.dump(data, f)
            f.close()

        else:

            f = open('/home/claudiogodoyb/programas/tc_historico.json', 'r')
            data = json.load(f)
            print(data)
            lista_avg = self.lista
            avg_day = round(sum(lista_avg)/len(lista_avg), 2)
            data['dias']['hoy']['avg'] = avg_day
            print(data)
            f = open("/home/claudiogodoyb/programas/tc_historico.json", "w")
            json.dump(data, f)
            f.close()

        return

    #GENERA LA GRÁFICA
    def grafica(self):
        y = []
        f = open('/home/claudiogodoyb/programas/tc_historico.json', 'r')
        data = json.load(f)
        for i in data['dias']:
            y.append(data['dias'][i]['avg'])
        x = ['-5 días', '-4 días', '-3 días', '-2 días', 'ayer', 'hoy']
        plt.figure()
        plt.plot(x, y,color='yellowgreen')
        plt.grid(axis='y', linestyle='dashed')
        for a, b in zip(x, y):
            plt.text(a, b, str(b))
        plt.xlabel("Fecha")
        plt.ylabel("Tipo de Cambio Venta")
        plt.title("Evolución TC Casas de Cambio Digitales")
        plt.savefig('gráfica_hoy.jpg')
        return

#ejecución del código
s = scraper()
compra_kambista, venta_kambista = s.kambista()
compra_rextie, venta_rextie = s.rextie()
compra_tkambio, venta_tkambio = s.tkambio()
compra_cyl , venta_cyl = s.cocosylucas()
compra_tucambista, venta_tucambista = s.tucambista()
compra_dollarhouse, venta_dollarhouse = s.dollarhouse()
euro = s.euroXE()
c = getUsers()
base_datos = c.getSheets()
lista_correos = base_datos['correo'].tolist()
lista_nombres = base_datos['nombre'].tolist()
print(lista_nombres)
print(len(lista_nombres))

#ejecucion de grafica y actualización de tc promedio dias anteriores 
lista_tc_venta = [float(venta_kambista) , float(venta_rextie) , float(venta_tkambio) , float(venta_cyl) , float(venta_tucambista) , float(venta_dollarhouse) ]
lista_tc_venta = [i for i in lista_tc_venta if i>0]
gd = graficaDatos(lista_tc_venta)
gd.actualizaDatos()
gd.grafica()
time.sleep(5)
m = mail(compra_kambista, venta_kambista, compra_rextie, venta_rextie, compra_tkambio, venta_tkambio, compra_cyl , venta_cyl, compra_tucambista, venta_tucambista, compra_dollarhouse, venta_dollarhouse, euro)

for (email,nombre) in zip(lista_correos,lista_nombres):
    correo = email
    name = nombre
    print(correo, name)
    m.sendMail(correo, name)
    time.sleep(1)

