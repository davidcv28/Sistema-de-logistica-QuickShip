#######################PRIVATE FUNCTIONS PROFILE USER###########################
################################################################################

"""
Aqui crearemos funciones publicas para todos los mixins
"""


#######<--TYPE DOCUMENT FUNCTION-->#######
"""
Creamos una función publica que se encargara de validar si el documento ingresado
 corresponde con las condiciones del tipo de documento seleccionado
"""
def validate_document_format(type_doc, doc):
    dict_errors ={}
    if type_doc == 'DNI':
        if len(doc) < 7 or len(doc)>8:
            dict_errors['document'] = 'El documento ingresado no es valido'
    if type_doc =='CUIT':
        prefix_list = ("20", "23", "24", "27", "30", "33", "34")
        if not doc.startswith(prefix_list):
            dict_errors['document'] = 'El prefijo del CUIL/CUIT no es valido'
        if len(doc) != 11:
            dict_errors['document'] = 'El CUIT/CUIL ingresado no es valido'
    if type_doc == 'LIB':
        if len(doc) < 6 or len(doc)>8:
            dict_errors['document'] = 'Número de LIB ingresado no es valido'
    if dict_errors:
        return dict_errors
    return False


######<--TAX CONDITION-->#######
"""
Creamos una función para verificar si esta correcta la selección de condición fiscal y razon social

"""
def validate_tax_conditions(type_doc, type_tax,business):
    dict_errors = {}
    if type_tax != 'CF':
        if type_doc != 'CUIT':
            dict_errors['type_document'] = 'Es necesario ingresar CUIT/CUIL para esta condición fiscal'
        if not business:
            dict_errors['business_name'] = 'Se requiere razón social para esta condición fiscal'
    if dict_errors:
        return dict_errors
    return False