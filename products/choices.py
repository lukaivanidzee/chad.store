from django.db.models import TextField

class Currency(TextField):
    GEL = 'gel', '₾'
    USD = 'usd', '$'
    EURO = 'euro', '€'