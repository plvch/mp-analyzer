# German MP Data Transformation exercise (check for professions)

Dataset of translated and profession-tagged German MPs from an Open Data XML (https://www.bundestag.de/services/opendata)
Data Source: Deutscher Bundestag/Bundesrat - DIP 

Further Translation / Tagging / Data extraction is Claude-assisted. 

This repository contains scripts to process and analyze data about Members of the German Bundestag (MPs). The main script performs the following tasks:

1. Parses XML data containing information about German MPs
2. Enriches the data with profession classifications and English translations
3. Restructures the data to create a row for each MP's term in the Bundestag
4. Outputs the processed data as a CSV file with English column names in snake case

Caveat - public versions of the script may contain differences with output in repo

## Output Schema

The final CSV file contains the following columns:

| Column Name    | Description                                           |
|----------------|-------------------------------------------------------|
| id             | Unique identifier for each MP                         |
| last_name      | MP's last name                                        |
| first_name     | MP's first name                                       |
| noble_title    | Noble title, if any                                   |
| form_of_address| Form of address (e.g., Dr.)                           |
| date_of_birth  | MP's date of birth                                    |
| place_of_birth | MP's place of birth                                   |
| date_of_death  | MP's date of death (if applicable)                    |
| gender         | MP's gender                                           |
| religion       | MP's religious affiliation                            |
| occupation     | MP's occupation (in German)                           |
| party          | Political party affiliation                           |
| profession     | English translation of the occupation                 |
| is_stem        | Whether the occupation is classified as STEM (Yes/No) |
| electoral_term | Electoral term number                                 |
| term_start     | Start date of the electoral term for this MP          |
| term_end       | End date of the electoral term for this MP            |
| constituency   | Name of the constituency (if applicable)              |
| state          | German state represented                              |
| list           | State list for party-list MPs                         |
| mandate_type   | Type of mandate (e.g., direct election, party list)   |

## Data Sources

- The main MP data is sourced from the German Bundestag's official records.
- Claude-assistance supported the compilation of the profession classifications and translations, is subject to interpretation and may contain inaccuracies.

## Note

This data processing script is for educational and research purposes. Always refer to official sources for the most up-to-date and accurate information about German MPs.
