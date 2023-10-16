import libsql_client
import os

api_key = os.environ.get("API_KEY")

client = libsql_client.create_client_sync(
    url="https://database-evancoons22.turso.io",
    auth_token=api_key
)

# with client: 
    # r = client.execute("drop table conditions").rows
    # r = client.execute("drop table main").rows
    # print(r) 
commands = [
        "CREATE TABLE predictions (datetime TIMESTAMP, WVHT numeric(19,6), MWD numeric(19,6), APD numeric(19, 6), inDays INTEGER)",
        "INSERT INTO predictions VALUES('2023-09-30 18:11:48.923569',6.6157617568969726562,50.981006622314453125,0.94983005523681640625,1)",
        "INSERT INTO predictions VALUES('2023-09-30 21:21:13.212224',0.94983005523681640625,50.981006622314453125,6.6157617568969726562,1)",
        "INSERT INTO predictions VALUES('2023-09-30 21:32:25.213655',0.88881915807723999023,105.96920776367187499,6.4635500907897949218,1)",
        "INSERT INTO predictions VALUES('2023-09-30 21:32:26.525056',0.89522850513458251953,91.364105224609375001,6.5201220512390136718,2)",
        "INSERT INTO predictions VALUES('2023-09-30 21:32:27.870051',0.93061673641204833984,31.310121536254882812,6.6877446174621582031,3)",
        "INSERT INTO predictions VALUES('2023-10-01 19:49:19.680473',0.88881927728652954101,105.9692230224609375,6.4635500907897949218,1)",
        "INSERT INTO predictions VALUES('2023-10-01 19:49:21.062719',0.89522850513458251953,91.364105224609375001,6.5201220512390136718,2)",
        "INSERT INTO predictions VALUES('2023-10-01 19:49:22.392343',0.93061673641204833984,31.310121536254882812,6.6877446174621582031,3)",
        "INSERT INTO predictions VALUES('2023-10-02 21:55:52.024101',0.71381598711013793945,39.9747314453125,2.0311863422393798828,1)",
        "INSERT INTO predictions VALUES('2023-10-02 21:55:53.437424',0.51256871223449707031,46.005611419677734375,3.3768939971923828125,2)",
        "INSERT INTO predictions VALUES('2023-10-02 21:55:54.807247',0.32645991444587707519,13.167966842651367187,3.0589358806610107421,3)",
        "INSERT INTO predictions VALUES('2023-10-03 10:53:11.267240',1.003381967544555664,99.798263549804687496,5.9193739891052246093,1)",
        "INSERT INTO predictions VALUES('2023-10-03 10:53:12.649553',0.6227098703384399414,84.401824951171875001,5.940044403076171875,2)",
        "INSERT INTO predictions VALUES('2023-10-03 10:53:14.001845',0.90340697765350341796,31.071825027465820312,6.6159892082214355468,3)",
        "INSERT INTO predictions VALUES('2023-10-04 08:54:31.163884',0.51269984245300292968,37.892955780029296875,2.3098726272583007812,1)",
        "INSERT INTO predictions VALUES('2023-10-04 08:54:32.658528',0.50294017791748046875,22.72086334228515625,1.6515365839004516601,2)",
        "INSERT INTO predictions VALUES('2023-10-04 08:54:34.149240',0.26653534173965454101,10.346769332885742187,1.6082988977432250976,3)",
        "INSERT INTO predictions VALUES('2023-10-04 11:48:11.309712',0.51269984245300292968,37.892955780029296875,2.3098726272583007812,1)",
        "INSERT INTO predictions VALUES('2023-10-04 11:48:12.670467',0.50294017791748046875,22.72086334228515625,1.6515365839004516601,2)",
        "INSERT INTO predictions VALUES('2023-10-04 11:48:14.045073',0.26653534173965454101,10.346769332885742187,1.6082988977432250976,3)",
        "INSERT INTO predictions VALUES('2023-10-05 09:13:39.522278',0.51269984245300292968,37.892955780029296875,2.3098726272583007812,1)",
        "INSERT INTO predictions VALUES('2023-10-05 09:13:40.986022',0.50294017791748046875,22.72086334228515625,1.6515365839004516601,2)",
        "INSERT INTO predictions VALUES('2023-10-05 09:13:42.401187',0.26653534173965454101,10.346769332885742187,1.6082988977432250976,3)"
        ]

commands = map(lambda x: libsql_client.Statement(x), commands)

def executeScriptsFromFile(filename, client):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    # sqlCommands = sqlFile.split(';')
    # remove \n from statements
    # sqlCommands = [x.replace('\n', '') for x in sqlCommands]
    # print(sqlCommands[0:10])
    # with client: 
        # r = client.batch(commands)
        # print(r)

    for command in commands: 
        r = client.execute(command)
        print(r)

    # Execute every command from the input file
    # with client:
        # for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            # try:
                # r = client.execute(command)
                # c.execute(command)
            # except r:
                # print("Command skipped: ", r)


executeScriptsFromFile("test.sql", client)
