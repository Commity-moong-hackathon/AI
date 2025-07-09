from app.parser import parse_calcelation_invoice, parse_calcelation_officail

def parse_by_type(form_type: str, text: str):
    if form_type == "official":
        return parse_calcelation_officail.parse(text)
    elif form_type == "invoice":
        return parse_calcelation_invoice.parse(text)
    else:
        raise ValueError("Unknown form type")