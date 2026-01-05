import migrate
import argparse

def main(args):
    # make sure a valid mode (csv or airtable) has been selected
    migrate.user.ensure_valid_mode(args, migrate.config.VALID_MODES)

    # set some configurations interactively if not supplied as comman   d line args
    # also used if no config file was provided
    if(args.interactive or not(args.config)):
        migrate.user.get_configs_interactive(args)
    
    migrate.config.set_configs(args)

    # TODO: implement a reading from cached function if an arg is passed with a file path
    migrate.wrangle.get_data()

    # Migrate all record types, or the one selected
    if(args.record_type == "all"):
        migrate.transform.transform_records("manuscript_objects")
        migrate.transform.transform_records("layers")
        migrate.transform.transform_records("text_units")
    else:
        migrate.transform.transform_records(args.record_type)

    # print(migrate.config.OUTPUT_DIR)

# TODO: add to tables config or main config the path to fields base directory

if __name__ == "__main__":
    # Set up an argparse parser and add CLI args
    parser = argparse.ArgumentParser(prog="Sinai Portal Migration Script",
                                     description="A command line utility for migrating Sinai manuscripts metadata from Airtable or CSVs to Sinai Data Portal-compliant JSON records")

    parser.add_argument('record_type',
                        choices=migrate.config.VALIED_RECORD_TYPES,
                        help=f"The record type, must be one of {migrate.config.VALIED_RECORD_TYPES[:-1]}, or use 'all' to transform all types at once")
    
    # Optional/flag arguments arguments
    parser.add_argument('-m', '--mode',
                        choices=migrate.config.VALID_MODES,
                        help=f"Required. Must be set to one of {migrate.config.VALID_MODES}",
                        required=True)
    parser.add_argument('-c', '--config',
                        help="Path to the configuration file. Required if not using interactive")
    parser.add_argument('--interactive',
                        help="Set most configurations interactively",
                        action='store_true')
    parser.add_argument('-o', '--output',
                        help="Set the directory where output JSON records should be stored; default is the current working directory")

    args = parser.parse_args()

    main(args)
"""

- be able to specify different config files (input or prompt)
- set output directory as the working directory, unless specified in a cli arg
- by default run on one at a time (set in flag or prompt); allow via prompting to do all at once
!! (general user or config refactoring needed) - implement error handling for if unneeded tables are not initialized via csv or airtable path
!! (general refactor needed) - allow paths to work even if multiple table_configs are created


CACHED AIRTABLE!
"""

"""
Set up configurations
- interactively (if -i)
- based on what was passed as CLI flags
2. Log what will be done, and maybe ask user for confirmation?
3. Transform the records, saving as you go
4. save the configuration data (incl. record data) if prompted, or if anny error occurs

"""