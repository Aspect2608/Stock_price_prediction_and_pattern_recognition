from flask import Flask, render_template, request
from main import search, stockpredict
import yfinance as yf
import datetime

app = Flask(__name__)
app.debug = False

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/download")
def download():

    stonks = "MMM ABT ABBV ABMD ACN ATVI ADBE AMD AAP AES AFL A APD AKAM ALK ALB ARE ALXN ALGN ALLE AGN ADS LNT ALL GOOGL GOOG MO AMZN AMCR AEE AAL AEP AXP AIG AMT AWK AMP ABC AME AMGN APH ADI ANSS ANTM AON AOS APA AIV AAPL AMAT APTV ADM ARNC ANET AJG AIZ ATO T ADSK ADP AZO AVB AVY BKR BLL BAC BK BAX BDX BRK.BBY BIIB BLK BA BKNG BWA BXP BSX BMY AVGO BR BF.CHRW COG CDNS CPB COF CPRI CAH KMX CCL CAT CBOE CBRE CDW CE CNC CNP CTL CERN CF SCHW CHTR CVX CMG CB CHD CI XEC CINF CTAS CSCO C CFG CTXS CLX CME CMS KO CTSH CL CMCSA CMA CAG CXO COP ED STZ COO CPRT GLW CTVA COST COTY CCI CSX CMI CVS DHI DHR DRI DVA DE DAL XRAY DVN FANG DLR DFS DISCA DISCK DISH DG DLTR D DOV DOW DTE DUK DRE DD DXC ETFC EMN ETN EBAY ECL EIX EW EA EMR ETR EOG EFX EQIX EQR ESS EL EVRG ES RE EXC EXPE EXPD EXR XOM FFIV FB FAST FRT FDX FIS FITB FE FRC FISV FLT FLIR FLS FMC F FTNT FTV FBHS FOXA FOX BEN FCX GPS GRMN IT GD GE GIS GM GPC GILD GL GPN GS GWW HRB HAL HBI HOG HIG HAS HCA PEAK HP HSIC HSY HES HPE HLT HFC HOLX HD HON HRL HST HPQ HUM HBAN HII IEX IDXX INFO ITW ILMN IR INTC ICE IBM INCY IP IPG IFF INTU ISRG IVZ IPGP IQV IRM JKHY J JBHT SJM JNJ JCI JPM JNPR KSU K KEY KEYS KMB KIM KMI KLAC KSS KHC KR LB LHX LH LRCX LW LVS LEG LDOS LEN LLY LNC LIN LYV LKQ LMT L LOW LYB MTB M MRO MPC MKTX MAR MMC MLM MAS MA MKC MXIM MCD MCK MDT MRK MET MTD MGM MCHP MU MSFT MAA MHK TAP MDLZ MNST MCO MS MOS MSI MSCI MYL NDAQ NOV NTAP NFLX NWL NEM NWSA NWS NEE NLSN NKE NI NBL JWN NSC NTRS NOC NLOK NCLH NRG NUE NVDA NVR ORLY OXY ODFL OMC OKE ORCL PCAR PKG PH PAYX PYPL PNR PBCT PEP PKI PRGO PFE PM PSX PNW PXD PNC PPG PPL PFG PG PGR PLD PRU PEG PSA PHM PVH QRVO PWR QCOM DGX RL RJF RTN O REG REGN RF RSG RMD RHI ROK ROL ROP ROST RCL SPGI CRM SBAC SLB STX SEE SRE NOW SHW SPG SWKS SLG SNA SO LUV SWK SBUX STT STE SYK SIVB SYF SNPS SYY TMUS TROW TTWO TPR TGT TEL FTI TFX TXN TXT TMO TIF TJX TSCO TDG TRV TFC TWTR TSN UDR ULTA USB UAA UA UNP UAL UNH UPS URI UTX UHS UNM VFC VLO VAR VTR VRSN VRSK VZ VRTX VIAC V VNO VMC WRB WAB WMT WBA DIS WM WAT WEC WCG WFC WELL WDC WU WRK WY WHR WMB WLTW WYNN XEL XRX XLNX XYL YUM ZBRA ZBH ZION ZTS"
    companies = stonks.split(" ")
    data = yf.download(stonks, start="2018-01-01", end=datetime.date.today())
    ohlc_dict = {}
    for company in companies:
        ohlc_data = data.xs(company, level=1, axis=1)
        ohlc_data['Name'] = company
        ohlc_dict[company] = ohlc_data

    for company, ohlc_data in ohlc_dict.items():
        file_name = f"{company}_data.csv"
        ohlc_data.to_csv("dataset/individual_stocks_5yr/{}".format(file_name))

@app.route('/', methods=['POST'])
def requestStock():
    text = request.form['sname']
    stockName = text.upper()
    print(stockName)
    if(search(stockName)):
        return displayStock(stockName)
    else:
        return predictStock(stockName)

def displayStock(stockName):
    stockData = []
    with open('static/stocks/'+stockName+'/'+stockName+'.txt', 'r') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            stockData.append(currentPlace)
    return render_template("stockdetail.html", stockName = stockName, stockData=stockData)

def predictStock(stockName):
    stockData=stockpredict(stockName)
    return render_template("stockdetail.html", stockName = stockName, stockData=stockData)



if __name__ == "__main__":



    app.run()