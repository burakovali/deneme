import fetcher, generate, query, analytics

def main():
    # Define a device identification database name.
    # This didb name will also be used for naming populated didbs.
    didbName = 'didb'


    # Fetch logs for parsing. Use a dateInfo for defining the necessary information for the fetcher. An example dateInfo is as follows:
    # dateInfo = {'use_timeRange': True, 'startDate': '2023-03-01 00:00:00', 'endDate': '2023-03-10 00:00:00', 'interval': '24'}
    # if "use_timeRange" is True, then the fetcher gets and stores the logs that only fall within the indicated start and end dates. If it is False, fetcher gets and stores all data from the server in a single log file.
    # Start date indicates the earliest timestamp in the fetched log file
    # Start date indicates the last timestamp in the fetched log file
    # interval indicates the timespan (in hours) for each log file to be downloaded and stored. For example, if the interval is set as 24, the logs will be downloaded and stored in files each spanning 24 hours of data. As such, if the time difference between start date and end date is 4 days, than there will be a seprate log file for each of the four days. 
    # Call get_data_intervals_recursive to fetch the data for the given dateInfo. Note that "type" is always set to 'ALL"
    if False:
        dateInfo = {'use_timeRange': True, 'startDate': '2023-03-01 00:00:00', 'endDate': '2023-03-10 00:00:00', 'interval': '24'}
        fetcher.get_data_intervals_recursive(dateInfo, type='ALL')


    # Once you have fetched the logs, you can run create_and_populate_didb to create and populate the didb (in both pickle and csv formats)
    # Note that create_and_populate_didb works on logs that span a single time duration. For example, below a didb file is generated using user_agent, dhcp and assoc_req logs that are collected between 2023-03-01 00:00:00 and 2023-03-02 00:00:00
    # To create and populate a didb using multiple logs from different time frames, you should use combine_didb.
    if False:
        # files_to_use = {'user_agent': 'user_agent_2023-03-01-00-00-00_2023-03-02-00-00-00.json', 'dhcp_proc': 'dhcp_proc_2023-03-01-00-00-00_2023-03-02-00-00-00.json', 'assoc_req': 'assoc_req_2023-03-01-00-00-00_2023-03-02-00-00-00.json', 'raw_user_agent': 'raw_user_agent_2023-03-01-00-00-00_2023-03-02-00-00-00.json'}
        # files_to_use = {'user_agent': 'user_agent_2023-03-02-00-00-00_2023-03-03-00-00-00.json', 'dhcp_proc': 'dhcp_proc_2023-03-02-00-00-00_2023-03-03-00-00-00.json', 'assoc_req': 'assoc_req_2023-03-02-00-00-00_2023-03-03-00-00-00.json', 'raw_user_agent': 'raw_user_agent_2023-03-02-00-00-00_2023-03-03-00-00-00.json'}
        files_to_use = {'user_agent': 'user_agent_2023-03-03-00-00-00_2023-03-04-00-00-00.json', 'dhcp_proc': 'dhcp_proc_2023-03-03-00-00-00_2023-03-04-00-00-00.json', 'assoc_req': 'assoc_req_2023-03-03-00-00-00_2023-03-04-00-00-00.json', 'raw_user_agent': 'raw_user_agent_2023-03-03-00-00-00_2023-03-04-00-00-00.json'}
        generate.create_and_populate_didb(didbName, files_to_use, True)


    # Combine separately created didbs into a single combined_didb. This function takes the list of didbs in a list format (didbList)
    # An example didbList is given below.
    # combined_didb is the final didb that will be used for querying device identification. 
    if False:
        didbList = ['didb_2023-03-01-00-00-00_2023-03-02-00-00-00', 'didb_2023-03-02-00-00-00_2023-03-03-00-00-00', 'didb_2023-03-03-00-00-00_2023-03-04-00-00-00' ]
        generate.combine_didb(didbList, True)    


    # Combined didb can be queried as given in following examples. For full list of available queries refer to query.py
    if False:
        analytics.analyze_didb()
        query.query_by_mac('78:4f:43:a0:98:72')
        query.query_by_brand('apple')
        query.query_by_model('iphone')
        query.query_by_params('1-121-3-6-15-108-114-119-252')
        query.query_by_timestamp('2023-03-10T10:41:04', '2023-03-11T10:41:04')
        query.query_by_gwmac('00:1c:7f:81:58:27')


if __name__ == "__main__":
    main()