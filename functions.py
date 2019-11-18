

def municipality_mapping(val):
    if val in ['Opština Sopot','Opština Mladenovac','Opština Obrenovac','Opština Lazarevac','Opština Barajevo','Opština Grocka']:
        return 1
    elif val in ['Opština Surčin','Opština Rakovica','Opština Čukarica']:
        return 2
    elif val == 'Opština Palilula':
        return 3
    elif val in ['Opština Zemun','Opština Zvezdara','Opština Voždovac']:
        return 4    
    elif val == 'Opština Novi Beograd':
        return 5
    elif val in ['Opština Stari grad', 'Opština Savski venac','Opština Vračar']:
        return 6
    else:
        return -1

def floor_mapping(val):
    if val == 'PR':
        return 0
    elif val == 'VPR':
        return 0.5
    elif val == 'PSUT':
        return -0.5
    elif val == 'SUT':
        return -0.5
    else:
        return -1

def heating_mapping(val):
    if val in ['Gas', 'Mermerni radijatori','Norveški radijatori','TA']:
        return 1
    elif val in ['CG','EG']:
        return 2
    elif val in ['Kraljeva peć','Podno']:
        return 3
    else: 
        return -1


def remap_df(df):    
    # remap character columns to numeric
    
    df['Condition'] = df['Condition'].replace(['Izvorno stanje','Za renoviranje','Renovirano', 'Lux'], [1,2,3,4])
    
    df['Object_Type'] = df['Object_Type'].replace(['Stara gradnja','Novogradnja','U izgradnji'], [1,2,2])
    
    df['No_of_Rooms'] = df['No_of_Rooms'].replace('5+', 6)
    df['No_of_Rooms'] = df['No_of_Rooms'].apply(float)
    
    df['Floor'] = df['Floor'].apply(floor_mapping)
    df['Floor'] = df['Floor'].apply(float)
    
    df['City_Area'] = df['City_Area'].apply(municipality_mapping)
    
    df['Heating'] = df['Heating'].apply(heating_mapping)
    
    df.fillna(-1, inplace=True)
    
    return(df)
    
def find_coordinates(address):
    import geocoder
    try:
        g = geocoder.here(address,app_code='-YNo0dU3B52bdC8AVR_nwA',app_id='TiWIaGqDr3e64oWcYsmg').json
    except:
        g = None
    return g

def get_flag_switch():
    flag_switch1 = {'Odmah Dostupan':'Flag_Available_Immediately',
               'Balkon':'Flag_Balcony',
               'Lođa':'Flag_Covered_Balcony',
               'Kablovska TV': 'Flag_CableTV',
               'Internet': 'Flag_Internet',
               'Duplex':'Flag_Duplex',
               'Lift':'Flag_Elevator',
               'Energetski Pasoš':'Flag_Energy_Saving',
               'Klima':'Flag_AirConditioning'}
               
    flag_switch2 = {'Garaža':'Flag_Garage',
               'Parking':'Flag_Parking',
               'Podrum':'Flag_Has_Basement',
               'Telefon':'Flag_Telephone',
               'Interfon':'Flag_Interphone',
               'Video':'Flag_Surveliance',
               'Legalno':'Flag_Legal',
               'Povraćaj PDV-a':'Flag_VAT_return',
               'Nije u kući':'Flag_Not_Part_of_House'}    

    flag_switch3 = {'Salonac':'Flag_Roomy',
               'Penthaus':'Flag_Penthouse',
               'Zamena':'Flag_Exchange_OK',
               'Pod Hipotekom':'Flag_Under_Mortgage',
               'Potkrovlje':'Flag_Rooftop',
               'Francuski Balkon':'Flag_FrenchBalcony',
               'Topla Voda':'Flag_HotWater',
               'Kamin':'Flag_Fireplace',
               'Nije poslednji sprat':'Flag_Not_Last_Floor'
                }
    
    dct={'City_Area':'','Street':'','Object_Type':'','Condition':'','Heating':'','Property_Size_sqmtr':0,'No_of_Rooms':'','Floor':'','Max_Floors':0,
                                 'Flag_Available_Immediately':-1, 'Flag_Balcony':-1, 'Flag_Covered_Balcony':-1, 'Flag_CableTV':-1, 'Flag_Internet':-1, 'Flag_Duplex':-1,'Flag_Elevator':-1,'Flag_Energy_Saving':-1,'Flag_AirConditioning':-1,
                                 'Flag_Garage':-1,'Flag_Parking':-1,'Flag_Has_Basement':-1, 'Flag_Telephone':-1,'Flag_Interphone':-1,'Flag_Surveliance':-1,'Flag_Legal':-1, 'Flag_VAT_return':-1, 'Flag_Not_Part_of_House':-1,
                                 'Flag_Roomy':-1,'Flag_Penthouse':-1,'Flag_Exchange_OK':-1,'Flag_Under_Mortgage':-1,'Flag_Rooftop':-1,'Flag_FrenchBalcony':-1,'Flag_HotWater':-1,'Flag_Fireplace':-1,'Flag_Not_Last_Floor':-1}

    return flag_switch1, flag_switch2, flag_switch3,dct
    
    
    
    