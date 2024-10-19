import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict
import ast

def parse_bundestag_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    data = []
    key_variability = defaultdict(set)
    
    for mdb in root.findall('.//MDB'):
        member_data = {}
        
        # Extract basic information
        member_data['ID'] = mdb.find('ID').text
        
        # Extract name information
        name = mdb.find('.//NAME')
        member_data['Nachname'] = name.find('NACHNAME').text
        member_data['Vorname'] = name.find('VORNAME').text
        member_data['Adelstitel'] = name.find('ADEL').text
        member_data['Anrede_Titel'] = name.find('ANREDE_TITEL').text
        
        # Extract biographical information
        bio = mdb.find('BIOGRAFISCHE_ANGABEN')
        member_data['Geburtsdatum'] = bio.find('GEBURTSDATUM').text if bio.find('GEBURTSDATUM') is not None else None
        member_data['Geburtsort'] = bio.find('GEBURTSORT').text if bio.find('GEBURTSORT') is not None else None
        member_data['Sterbedatum'] = bio.find('STERBEDATUM').text if bio.find('STERBEDATUM') is not None else None
        member_data['Geschlecht'] = bio.find('GESCHLECHT').text if bio.find('GESCHLECHT') is not None else None
        member_data['Religion'] = bio.find('RELIGION').text if bio.find('RELIGION') is not None else None
        member_data['Beruf'] = bio.find('BERUF').text if bio.find('BERUF') is not None else None
        member_data['Partei'] = bio.find('PARTEI_KURZ').text if bio.find('PARTEI_KURZ') is not None else None
        
        # Extract electoral periods
        wahlperioden = []
        for wp in mdb.findall('.//WAHLPERIODE'):
            wahlperiode = {
                'WP': wp.find('WP').text,
                'Von': wp.find('MDBWP_VON').text,
                'Bis': wp.find('MDBWP_BIS').text,
                'Wahlkreis': wp.find('WKR_NAME').text,
                'Bundesland': wp.find('WKR_LAND').text,
                'Liste': wp.find('LISTE').text,
                'Mandatsart': wp.find('MANDATSART').text
            }
            wahlperioden.append(wahlperiode)
        
        member_data['Wahlperioden'] = wahlperioden
        
        # Update key variability
        for key, value in member_data.items():
            if isinstance(value, str):
                key_variability[key].add(value)
        
        data.append(member_data)
    
    # Create the main DataFrame
    main_df = pd.DataFrame(data)
    
    # Create the key variability DataFrame
    variability_data = [{'Key': key, 'Values': ', '.join(values)} for key, values in key_variability.items()]
    variability_df = pd.DataFrame(variability_data)
    
    return main_df, variability_df

def safe_eval(x):
    if isinstance(x, str):
        return ast.literal_eval(x)
    return x

def main():
    # Parse the XML file
    main_df, variability_df = parse_bundestag_xml('data/MDB_STAMMDATEN.xml')
    
    print("Main DataFrame created.")
    print("Key Variability DataFrame created.")

    # Load the combined professions list
    combined_list = pd.read_csv('data/combined_professions.csv')

    # Prepare the combined list for merging
    combined_list_adj = combined_list[['German Profession', 'English Translation', 'STEM']].drop_duplicates()
    combined_list_adj.columns = ['Beruf', 'Profession', 'is_stem']

    # Merge the main DataFrame with the combined professions list
    main_df_mrg = main_df.merge(combined_list_adj, how='left', on='Beruf')

    print("Merged with profession data.")

    # Apply safe_eval to the 'Wahlperioden' column
    main_df_mrg['Wahlperioden'] = main_df_mrg['Wahlperioden'].apply(safe_eval)

    # Explode the 'Wahlperioden' column
    df_exploded = main_df_mrg.explode('Wahlperioden')

    # Reset the index after exploding
    df_exploded = df_exploded.reset_index(drop=True)

    # Extract the dictionary values into separate columns
    for key in ['WP', 'Von', 'Bis', 'Wahlkreis', 'Bundesland', 'Liste', 'Mandatsart']:
        df_exploded[key] = df_exploded['Wahlperioden'].apply(lambda x: x.get(key) if isinstance(x, dict) else None)

    # Drop the original 'Wahlperioden' column
    df_exploded = df_exploded.drop('Wahlperioden', axis=1)

    print("DataFrame exploded and restructured.")

    # Dictionary to map German column names to English with explanations (using snake case)
    column_name_map = {
        'ID': 'id',  # Unique identifier for each MP
        'Nachname': 'last_name',  # MP's last name
        'Vorname': 'first_name',  # MP's first name
        'Adelstitel': 'noble_title',  # Noble title, if any (e.g., Graf, Freiherr)
        'Anrede_Titel': 'form_of_address',  # Form of address (e.g., Dr., Prof.)
        'Geburtsdatum': 'date_of_birth',  # MP's date of birth
        'Geburtsort': 'place_of_birth',  # MP's place of birth
        'Sterbedatum': 'date_of_death',  # MP's date of death (if applicable)
        'Geschlecht': 'gender',  # MP's gender (männlich/weiblich)
        'Religion': 'religion',  # MP's religious affiliation
        'Beruf': 'occupation',  # MP's occupation (in German)
        'Partei': 'party',  # Political party affiliation
        'Profession': 'profession',  # English translation of the occupation
        'is_stem': 'is_stem',  # Whether the occupation is classified as STEM (Yes/No)
        'WP': 'electoral_term',  # Electoral term number
        'Von': 'term_start',  # Start date of the electoral term for this MP
        'Bis': 'term_end',  # End date of the electoral term for this MP
        'Wahlkreis': 'constituency',  # Name of the constituency (if directly elected)
        'Bundesland': 'state',  # German state represented
        'Liste': 'list',  # State list for party-list MPs
        'Mandatsart': 'mandate_type'  # Type of mandate (e.g., direct election, party list)
    }

    # Rename the columns
    df_exploded = df_exploded.rename(columns=column_name_map)

    # Save the result to a CSV file
    df_exploded.to_csv('output/mp-list-professions.csv', index=False)

    print("Processing complete. Output saved to 'output/mp-list-professions.csv'")

if __name__ == "__main__":
    main()
