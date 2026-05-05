from django.core.management import BaseCommand
from QuickShipApp.domains.user.models import Province, City
from django.db import transaction

"""ESTE SCRIPT CARGA TODAS LAS PROVINCIAS DE ARGENTINA,
 SUS CIUDADES Y SUS CORRESPONDIENTES CODIGOS POSTALES """
class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            ARGENTINA_FULL_DATA = {
        "Buenos Aires": [
            {"nombre": "La Plata", "departamento": "La Plata", "cp": "1900"},
            {"nombre": "Mar del Plata", "departamento": "General Pueyrredón", "cp": "7600"},
            {"nombre": "Bahía Blanca", "departamento": "Bahía Blanca", "cp": "8000"},
            {"nombre": "San Nicolás de los Arroyos", "departamento": "San Nicolás", "cp": "2900"},
            {"nombre": "Tandil", "departamento": "Tandil", "cp": "7000"},
            {"nombre": "Zárate", "departamento": "Zárate", "cp": "2800"},
            {"nombre": "Olavarría", "departamento": "Olavarría", "cp": "7400"},
            {"nombre": "Pergamino", "departamento": "Pergamino", "cp": "2700"},
            {"nombre": "Campana", "departamento": "Campana", "cp": "2804"},
            {"nombre": "Junín", "departamento": "Junín", "cp": "6000"},
            {"nombre": "Necochea", "departamento": "Necochea", "cp": "7630"},
            {"nombre": "Luján", "departamento": "Luján", "cp": "6700"},
            {"nombre": "Chivilcoy", "departamento": "Chivilcoy", "cp": "6600"},
            {"nombre": "Azul", "departamento": "Azul", "cp": "7300"},
            {"nombre": "Mercedes", "departamento": "Mercedes", "cp": "6600"},
            {"nombre": "Pilar", "departamento": "Pilar", "cp": "1629"},
            {"nombre": "Escobar", "departamento": "Escobar", "cp": "1625"},
            {"nombre": "Tigre", "departamento": "Tigre", "cp": "1648"},
            {"nombre": "San Isidro", "departamento": "San Isidro", "cp": "1642"},
            {"nombre": "Vicente López", "departamento": "Vicente López", "cp": "1602"},
            {"nombre": "Lanús", "departamento": "Lanús", "cp": "1824"},
            {"nombre": "Avellaneda", "departamento": "Avellaneda", "cp": "1870"},
            {"nombre": "Quilmes", "departamento": "Quilmes", "cp": "1878"},
            {"nombre": "Lomas de Zamora", "departamento": "Lomas de Zamora", "cp": "1832"},
            {"nombre": "La Matanza (San Justo)", "departamento": "La Matanza", "cp": "1754"},
            {"nombre": "Morón", "departamento": "Morón", "cp": "1708"},
            {"nombre": "Moreno", "departamento": "Moreno", "cp": "1744"},
            {"nombre": "Merlo", "departamento": "Merlo", "cp": "1722"},
            {"nombre": "San Miguel", "departamento": "San Miguel", "cp": "1663"}
        ],
        "CABA": [
            {"nombre": "Comuna 1 (Retiro, San Nicolás, etc)", "departamento": "CABA", "cp": "1001"},
            {"nombre": "Comuna 2 (Recoleta)", "departamento": "CABA", "cp": "1112"},
            {"nombre": "Comuna 3 (Balvanera, San Cristóbal)", "departamento": "CABA", "cp": "1214"},
            {"nombre": "Comuna 4 (La Boca, Barracas, etc)", "departamento": "CABA", "cp": "1152"},
            {"nombre": "Comuna 5 (Almagro, Boedo)", "departamento": "CABA", "cp": "1205"}
        ],
        "Catamarca": [
            {"nombre": "S.F.V. de Catamarca", "departamento": "Capital", "cp": "4700"},
            {"nombre": "Belén", "departamento": "Belén", "cp": "4750"},
            {"nombre": "Tinogasta", "departamento": "Tinogasta", "cp": "5340"},
            {"nombre": "Andalgalá", "departamento": "Andalgalá", "cp": "4740"},
            {"nombre": "Santa María", "departamento": "Santa María", "cp": "4139"},
            {"nombre": "Recreo", "departamento": "La Paz", "cp": "5260"}
        ],
        "Chaco": [
            {"nombre": "Resistencia", "departamento": "San Fernando", "cp": "3500"},
            {"nombre": "P. Roque Sáenz Peña", "departamento": "Comandante Fernández", "cp": "3700"},
            {"nombre": "Villa Ángela", "departamento": "Mayor Luis J. Fontana", "cp": "3540"},
            {"nombre": "Charata", "departamento": "Chacabuco", "cp": "3730"},
            {"nombre": "Juan José Castelli", "departamento": "General Güemes", "cp": "3705"}
        ],
        "Chubut": [
            {"nombre": "Rawson", "departamento": "Rawson", "cp": "9103"},
            {"nombre": "Comodoro Rivadavia", "departamento": "Escalante", "cp": "9000"},
            {"nombre": "Puerto Madryn", "departamento": "Biedma", "cp": "9120"},
            {"nombre": "Trelew", "departamento": "Rawson", "cp": "9100"},
            {"nombre": "Esquel", "departamento": "Futaleufú", "cp": "9200"},
            {"nombre": "Sarmiento", "departamento": "Sarmiento", "cp": "9020"}
        ],
        "Córdoba": [
            {"nombre": "Córdoba Capital", "departamento": "Capital", "cp": "5000"},
            {"nombre": "Río Cuarto", "departamento": "Río Cuarto", "cp": "5800"},
            {"nombre": "Villa María", "departamento": "General San Martín", "cp": "5900"},
            {"nombre": "San Francisco", "departamento": "San Justo", "cp": "2400"},
            {"nombre": "Villa Carlos Paz", "departamento": "Punilla", "cp": "5152"},
            {"nombre": "Alta Gracia", "departamento": "Santa María", "cp": "5186"},
            {"nombre": "Río Tercero", "departamento": "Tercero Arriba", "cp": "5850"},
            {"nombre": "Bell Ville", "departamento": "Unión", "cp": "2550"},
            {"nombre": "Jesús María", "departamento": "Colón", "cp": "5220"},
            {"nombre": "Villa Dolores", "departamento": "San Javier", "cp": "5870"}
        ],
        "Corrientes": [
            {"nombre": "Corrientes Capital", "departamento": "Capital", "cp": "3400"},
            {"nombre": "Goya", "departamento": "Goya", "cp": "3450"},
            {"nombre": "Paso de los Libres", "departamento": "Paso de los Libres", "cp": "3230"},
            {"nombre": "Curuzú Cuatiá", "departamento": "Curuzú Cuatiá", "cp": "3460"},
            {"nombre": "Mercedes", "departamento": "Mercedes", "cp": "3470"},
            {"nombre": "Bella Vista", "departamento": "Bella Vista", "cp": "3432"},
            {"nombre": "Santo Tomé", "departamento": "Santo Tomé", "cp": "3340"}
        ],
        "Entre Ríos": [
            {"nombre": "Paraná", "departamento": "Paraná", "cp": "3100"},
            {"nombre": "Concordia", "departamento": "Concordia", "cp": "3200"},
            {"nombre": "Gualeguaychú", "departamento": "Gualeguaychú", "cp": "2820"},
            {"nombre": "Concepción del Uruguay", "departamento": "Uruguay", "cp": "3260"},
            {"nombre": "Villaguay", "departamento": "Villaguay", "cp": "3240"},
            {"nombre": "Chajarí", "departamento": "Federación", "cp": "3228"},
            {"nombre": "Victoria", "departamento": "Victoria", "cp": "3153"}
        ],
        "Formosa": [
            {"nombre": "Formosa Capital", "departamento": "Formosa", "cp": "3600"},
            {"nombre": "Clorinda", "departamento": "Pilcomayo", "cp": "3610"},
            {"nombre": "Pirané", "departamento": "Pirané", "cp": "3606"},
            {"nombre": "El Colorado", "departamento": "Pirané", "cp": "3603"}
        ],
        "Jujuy": [
            {"nombre": "San Salvador de Jujuy", "departamento": "Dr. Manuel Belgrano", "cp": "4600"},
            {"nombre": "San Pedro de Jujuy", "departamento": "San Pedro", "cp": "4500"},
            {"nombre": "Palpalá", "departamento": "Palpalá", "cp": "4612"},
            {"nombre": "Libertador Gral. San Martín", "departamento": "Ledesma", "cp": "4512"},
            {"nombre": "La Quiaca", "departamento": "Yavi", "cp": "4650"},
            {"nombre": "Humahuaca", "departamento": "Humahuaca", "cp": "4630"}
        ],
        "La Pampa": [
            {"nombre": "Santa Rosa", "departamento": "Capital", "cp": "6300"},
            {"nombre": "General Pico", "departamento": "Maracó", "cp": "6360"},
            {"nombre": "General Acha", "departamento": "Utracán", "cp": "8200"},
            {"nombre": "Eduardo Castex", "departamento": "Conhelo", "cp": "6380"}
        ],
        "La Rioja": [
            {"nombre": "La Rioja Capital", "departamento": "Capital", "cp": "5300"},
            {"nombre": "Chilecito", "departamento": "Chilecito", "cp": "5360"},
            {"nombre": "Aimogasta", "departamento": "Arauco", "cp": "5310"},
            {"nombre": "Chamical", "departamento": "Chamical", "cp": "5380"}
        ],
        "Mendoza": [
            {"nombre": "Mendoza Capital", "departamento": "Capital", "cp": "5500"},
            {"nombre": "San Rafael", "departamento": "San Rafael", "cp": "5600"},
            {"nombre": "Godoy Cruz", "departamento": "Godoy Cruz", "cp": "5501"},
            {"nombre": "Las Heras", "departamento": "Las Heras", "cp": "5539"},
            {"nombre": "Guaymallén", "departamento": "Guaymallén", "cp": "5519"},
            {"nombre": "Luján de Cuyo", "departamento": "Luján de Cuyo", "cp": "5507"},
            {"nombre": "Maipú", "departamento": "Maipú", "cp": "5515"},
            {"nombre": "Malargüe", "departamento": "Malargüe", "cp": "5613"},
            {"nombre": "General Alvear", "departamento": "General Alvear", "cp": "5620"},
            {"nombre": "Tunuyán", "departamento": "Tunuyán", "cp": "5560"}
        ],
        "Misiones": [
            {"nombre": "Posadas", "departamento": "Capital", "cp": "3300"},
            {"nombre": "Oberá", "departamento": "Oberá", "cp": "3360"},
            {"nombre": "Eldorado", "departamento": "Eldorado", "cp": "3380"},
            {"nombre": "Puerto Iguazú", "departamento": "Iguazú", "cp": "3370"},
            {"nombre": "Apóstoles", "departamento": "Apóstoles", "cp": "3350"},
            {"nombre": "San Vicente", "departamento": "Guaraní", "cp": "3364"}
        ],
        "Neuquén": [
            {"nombre": "Neuquén Capital", "departamento": "Confluencia", "cp": "8300"},
            {"nombre": "Cutral Có", "departamento": "Confluencia", "cp": "8322"},
            {"nombre": "Zapala", "departamento": "Zapala", "cp": "8340"},
            {"nombre": "San Martín de los Andes", "departamento": "Lácar", "cp": "8370"},
            {"nombre": "Plottier", "departamento": "Confluencia", "cp": "8316"},
            {"nombre": "Villa La Angostura", "departamento": "Los Lagos", "cp": "8407"},
            {"nombre": "Chos Malal", "departamento": "Chos Malal", "cp": "8353"}
        ],
        "Río Negro": [
            {"nombre": "Viedma", "departamento": "Adolfo Alsina", "cp": "8500"},
            {"nombre": "San Carlos de Bariloche", "departamento": "Bariloche", "cp": "8400"},
            {"nombre": "General Roca", "departamento": "General Roca", "cp": "8332"},
            {"nombre": "Cipolletti", "departamento": "General Roca", "cp": "8324"},
            {"nombre": "Villa Regina", "departamento": "General Roca", "cp": "8336"},
            {"nombre": "Allen", "departamento": "General Roca", "cp": "8322"},
            {"nombre": "San Antonio Oeste", "departamento": "San Antonio", "cp": "8520"}
        ],
        "Salta": [
            {"nombre": "Salta Capital", "departamento": "Capital", "cp": "4400"},
            {"nombre": "San Ramón de la Nueva Orán", "departamento": "Orán", "cp": "4530"},
            {"nombre": "Tartagal", "departamento": "General José de San Martín", "cp": "4560"},
            {"nombre": "General Güemes", "departamento": "General Güemes", "cp": "4430"},
            {"nombre": "Metán", "departamento": "Metán", "cp": "4440"},
            {"nombre": "Rosario de la Frontera", "departamento": "Rosario de la Frontera", "cp": "4190"},
            {"nombre": "Cafayate", "departamento": "Cafayate", "cp": "4427"},
            {"nombre": "Pichanal", "departamento": "Orán", "cp": "4534"}
        ],
        "San Juan": [
            {"nombre": "San Juan Capital", "departamento": "Capital", "cp": "5400"},
            {"nombre": "Rawson", "departamento": "Rawson", "cp": "5425"},
            {"nombre": "Rivadavia", "departamento": "Rivadavia", "cp": "5401"},
            {"nombre": "Chimbas", "departamento": "Chimbas", "cp": "5413"},
            {"nombre": "Santa Lucía", "departamento": "Santa Lucía", "cp": "5411"},
            {"nombre": "Caucete", "departamento": "Caucete", "cp": "5440"},
            {"nombre": "San José de Jáchal", "departamento": "Jáchal", "cp": "5460"}
        ],
        "San Luis": [
            {"nombre": "San Luis Capital", "departamento": "Juan Martín de Pueyrredón", "cp": "5700"},
            {"nombre": "Villa Mercedes", "departamento": "General Pedernera", "cp": "5730"},
            {"nombre": "Merlo", "departamento": "Junín", "cp": "5881"},
            {"nombre": "La Toma", "departamento": "Pringles", "cp": "5750"}
        ],
        "Santa Cruz": [
            {"nombre": "Río Gallegos", "departamento": "Güer Aike", "cp": "9400"},
            {"nombre": "Caleta Olivia", "departamento": "Deseado", "cp": "9011"},
            {"nombre": "El Calafate", "departamento": "Lago Argentino", "cp": "9405"},
            {"nombre": "Pico Truncado", "departamento": "Deseado", "cp": "9015"},
            {"nombre": "Puerto Deseado", "departamento": "Deseado", "cp": "9050"},
            {"nombre": "Las Heras", "departamento": "Deseado", "cp": "9310"}
        ],
        "Santa Fe": [
            {"nombre": "Santa Fe Capital", "departamento": "La Capital", "cp": "3000"},
            {"nombre": "Rosario", "departamento": "Rosario", "cp": "2000"},
            {"nombre": "Rafaela", "departamento": "Castellanos", "cp": "2300"},
            {"nombre": "Venado Tuerto", "departamento": "General López", "cp": "2600"},
            {"nombre": "Reconquista", "departamento": "General Obligado", "cp": "3560"},
            {"nombre": "Santo Tomé", "departamento": "La Capital", "cp": "3016"},
            {"nombre": "Villa Constitución", "departamento": "Constitución", "cp": "2919"},
            {"nombre": "Esperanza", "departamento": "Las Colonias", "cp": "3080"},
            {"nombre": "Casilda", "departamento": "Caseros", "cp": "2170"},
            {"nombre": "Cañada de Gómez", "departamento": "Iriondo", "cp": "2500"}
        ],
        "Santiago del Estero": [
            {"nombre": "Santiago del Estero Capital", "departamento": "Juan Francisco Borges", "cp": "4200"},
            {"nombre": "La Banda", "departamento": "Banda", "cp": "4300"},
            {"nombre": "Termas de Río Hondo", "departamento": "Río Hondo", "cp": "4220"},
            {"nombre": "Frías", "departamento": "Choya", "cp": "4230"},
            {"nombre": "Añatuya", "departamento": "General Taboada", "cp": "3760"}
        ],
        "Tierra del Fuego": [
            {"nombre": "Ushuaia", "departamento": "Ushuaia", "cp": "9410"},
            {"nombre": "Río Grande", "departamento": "Río Grande", "cp": "9420"},
            {"nombre": "Tolhuin", "departamento": "Río Grande", "cp": "9412"}
        ],
        "Tucumán": [
            {"nombre": "San Miguel de Tucumán", "departamento": "Capital", "cp": "4000"},
            {"nombre": "Concepción", "departamento": "Chicligasta", "cp": "4146"},
            {"nombre": "Yerba Buena", "departamento": "Yerba Buena", "cp": "4107"},
            {"nombre": "Tafí Viejo", "departamento": "Tafí Viejo", "cp": "4103"},
            {"nombre": "Aguilares", "departamento": "Río Chico", "cp": "4152"},
            {"nombre": "Monteros", "departamento": "Monteros", "cp": "4142"},
            {"nombre": "Famaillá", "departamento": "Famaillá", "cp": "4132"},
            {"nombre": "Tafí del Valle", "departamento": "Tafí del Valle", "cp": "4137"}
        ]
        }
        self.stdout.write(self.style.WARNING('CARGANDO PROVINCIAS Y CIUDADES'))
        list_province = []
        for province in ARGENTINA_FULL_DATA:
            province_item = Province(name_province = province)
            list_province.append(province_item)
        Province.objects.bulk_create(list_province, ignore_conflicts=True)
        provinces = Province.objects.all()
        map_province = {p.name_province : p for p in provinces}
        list_city = []
        for province_key, citys in ARGENTINA_FULL_DATA.items():
            province_item = map_province[province_key]
            for data in citys:
                city = data['nombre']
                cp = data['cp']
                city_item = City(province_fk =province_item, name_city = city, zipcode = cp)
                list_city.append(city_item)
        City.objects.bulk_create(list_city, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS('LAS PROVINCIAS Y CIUDADES FUERON CARGADAS'))