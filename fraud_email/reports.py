import csv
from pathlib import Path
from .schemas import EmailInput
from .triage import classify

COLUMNS=["message_id","sender","recipient","subject","label","risk_score","priority","relevant","reply_needed","review_required","summary"]

def create_rows(emails: list[EmailInput]):
    for email in emails:
        result=classify(email)
        yield {"message_id":email.message_id,"sender":email.sender,"recipient":email.recipient,
          "subject":email.subject,"label":result.label,"risk_score":result.risk_score,
          "priority":result.priority,"relevant":result.relevant,"reply_needed":result.reply_needed,
          "review_required":result.review_required,"summary":" | ".join(result.summary)}

def export_csv(emails: list[EmailInput], path: str):
    with Path(path).open("w", newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(create_rows(emails))

def export_xlsx(emails: list[EmailInput], path: str):
    from xlsxwriter import Workbook
    wb=Workbook(path)
    ws=wb.add_worksheet("Email Register")
    header=wb.add_format({"bold":True,"bg_color":"#17365D","font_color":"white"})
    danger=wb.add_format({"bg_color":"#FCE4E4"})
    ws.write_row(0,0,COLUMNS,header)
    for row_i, row in enumerate(create_rows(emails),1):
        for col_i, name in enumerate(COLUMNS):
            val=row[name]
            if isinstance(val,str) and val[:1] in "=+-@":val="'"+val
            ws.write(row_i,col_i,val,danger if row["label"] in ("fraud","phishing") else None)
    ws.freeze_panes(1,0)
    ws.autofilter(0,0,row_i if 'row_i' in locals() else 0,len(COLUMNS)-1)
    ws.set_column(0,3,27);ws.set_column(4,9,17);ws.set_column(10,10,65)
    wb.close()
