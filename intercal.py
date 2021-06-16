from datetime import datetime
import calendar
from fpdf import FPDF

# --- Variables
debugBorder = 0
pageSize = (297, 420) # Size of A3 in mm
border = 25 # Border in mm
cellWidth = (pageSize[0] - 2*border) / 7
dayCellHeight = 40
language = "en"


# --- Translations
monthNames = {
    "de": ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}

dayNames = {
    "de": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
    "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
}


# --- Initial page setup
pdf = FPDF(
    orientation="P",
    unit="mm",
    format="A3"
)

pdf.set_margins(0, 0, 0)

# --- Register fonts
pdf.add_font("Inter", "", "fonts/Inter-Regular.ttf", uni=True)
pdf.add_font("Inter", "B", "fonts/Inter-Bold.ttf", uni=True)


now = datetime.now()

lastMonthDays = 31

for month in range(1, 13):

    # --- Calculate days
    dayRange = calendar.monthrange(now.year, month)

    daysPreviousMonth = [i+1 for i in range(lastMonthDays)]
    if dayRange[0] > 0:
        daysPre = [d for d in daysPreviousMonth[-dayRange[0]:]]
    else:
        daysPre = []

    daysNow = [d+1 for d in range(dayRange[1])]

    daysAfter = 7 - ((len(daysPre) + dayRange[1]) % 7)
    if daysAfter < 7:
        daysPost = [i+1 for i in range(daysAfter)]
    else:
        daysPost = []

    lastMonthDays = dayRange[1]

    pdf.add_page()

    # --- Write Month
    pdf.set_xy(border, 2*border)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Inter", "B", 120)
    pdf.cell(pageSize[0] - 2*border, 50, monthNames[language][month-1], border=debugBorder)

    # --- Write Header
    y = pdf.get_y()
    pdf.set_y(y+3*border)
    pdf.set_x(border)
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Inter", "", 16)
    for i in range(7):
        pdf.cell(cellWidth, dayCellHeight/2, dayNames[language][i], align="L", border=debugBorder)

    # --- Write Days
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Inter", "B", 32)

    y = pdf.get_y()
    pdf.set_y(y+dayCellHeight/2)
    pdf.set_x(border)

    dayCounter = 0

    pdf.set_text_color(200, 200, 200)
    for day in daysPre:
        pdf.cell(cellWidth, dayCellHeight, str(day), align="L", border=debugBorder)
        dayCounter += 1
        if dayCounter % 7 == 0:
            y = pdf.get_y()
            pdf.set_y(y+dayCellHeight)
            pdf.set_x(border)

    pdf.set_text_color(0, 0, 0)
    for day in daysNow:
        pdf.cell(cellWidth, dayCellHeight, str(day), align="L", border=debugBorder)
        dayCounter += 1
        if dayCounter % 7 == 0:
            y = pdf.get_y()
            pdf.set_y(y+dayCellHeight)
            pdf.set_x(border)

    pdf.set_text_color(200, 200, 200)
    for day in daysPost:
        pdf.cell(cellWidth, dayCellHeight, str(day), align="L", border=debugBorder)
        dayCounter += 1
        if dayCounter % 7 == 0:
            y = pdf.get_y()
            pdf.set_y(y+dayCellHeight)
            pdf.set_x(border)


# --- Output
pdf.output("calendar.pdf", "F")
