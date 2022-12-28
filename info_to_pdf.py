'''
Data and Graphs generated from other files are taken and stored into the pdf form and a report is being generated. 
'''

from fpdf import FPDF
import os
import yfinance as yf
import datetime as dt
from IPO_stock_performance import adj_price_analysis,list_top,grouping


# Margin
m = 20 
# Page width: Width of A4 is 210mm
pw = 210 - 2*m 
# Cell height
ch = 8

class PDF(FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        self.set_font('Arial', '', 12)
        self.cell(0, 8, "Header", 0, 1, 'C')
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 12)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

def info_to_pdf():
    '''
    All the information is being converted to PDF and stored locally.
    '''
    pdf = FPDF()
    pdf.set_margins(left=20,right=20,top=20)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(w=0, h=20, txt=f"Performance of the IPOs listed in {dt.date.today().year}", ln=1)
    pdf.set_font('Arial', '', 16)
    pdf.cell(w=15, h=ch, txt="Analysis done on: ", ln=1)
    pdf.cell(w=15, h=ch, txt=f'{dt.date.today()}', ln=1)

    def page_add(df):
        # Adding a new Page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(w=0, h=20, txt=f"{df['Name of the issue']}", ln=1)
        pdf.ln(ch)
        # Table Header
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(w=60, h=ch, txt='Index', border=1, ln=0, align='C')
        pdf.cell(w=100, h=ch, txt='Values', border=1, ln=1, align='C')
        # Table contents
        pdf.set_font('Arial', '', 12)
        for i in range(2,len(df)):
            pdf.cell(w=60, h=ch, 
                    txt=df.index[i], 
                    border=1, ln=0, align='L')
            pdf.cell(w=100, h=ch, 
                    txt=str(df[i]), 
                    border=1, ln=1, align='R')
        # Setting the pages for price action chart information
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(w=0, h=20, txt="Price Action Graph", ln=1,align='C')
        try:
            img = adj_price_analysis(f"{df['symbol']}.NS")
            pdf.image(img, 
                x = None, y = None, w = 190, h = 0, type = 'PNG')
            pdf.ln(ch*2)     

            # pdf.set_font('Arial', '', 12)

            # stock_analysis=f"{df['Name of the issue']} listed at"
            # pdf.multi_cell(w=0, h=5, txt=stock_analysis)

        except:
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(w=0, h=5, txt="No iformation Available")

    # gathering the info of loosing and winning IPOs
    loosers,winners=list_top()

    def performing_stocks(df,performance=None):
        '''
        How a particular stock has performed is being written to a page.
        '''
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(w=0, h=20, txt=f"Five {performance} IPOs", ln=1,align='C')
        for ele in range(len(df)):
            text1 = f"{df.loc[ele,'Name of the issue']}"
            text2 = f"listed on {df.loc[ele,'Date ofListing']} at {df.loc[ele,'listing price']} currently trading at {df.loc[ele,'LTP']} with the gain of {df.loc[ele,'current_gain_percentage']}% from the date of listing."
            pdf.set_font('Arial', 'B', 7)
            pdf.cell(w=5, h=4, txt=text1,ln=1)
            pdf.cell(w=5, h=4, txt=text2,ln=2)
            pdf.ln(ch)
        for win in range(df.shape[0]):
            temp_df = df.iloc[win,:]
            page_add(temp_df)

    def groupwise_analysis(group=None,output_col=None):
        '''
        This function returns the groupwise data for the pdf page
        '''
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(w=0, h=20, txt=f"{group.upper()} WISE Listed IPOs Names", ln=1,align='C')
        dc = grouping(group,output_col)
        for key,val in dc.items():
            text = f"{key} : {len(val)}"
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(w=5, h=4, txt=text,ln=1)
            pdf.ln(ch-5)
            for ele in val:
                pdf.set_font('Arial', 'B', 6)
                pdf.cell(w=10, h=4, txt=ele,ln=1)
            pdf.ln(ch)

    groupwise_analysis('sector','Name of the issue')
    groupwise_analysis('industry','Name of the issue')
    performing_stocks(winners,performance='Best Performing')
    performing_stocks(loosers,'Worst Performing')

    directory='PDFs'
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"{directory} created to save the PDFs")
    pdf.output(f'{directory}/IPOs_analysis.pdf')
    print(f"\nData saved as : {directory}/IPOs_analysis.pdf\n")


if __name__=="__main__":
    info_to_pdf()


