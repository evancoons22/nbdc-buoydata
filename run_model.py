import model_functions as mf
import torch
import sqlite3
import datetime


def predictWaves(indays = 1): 

    num_features = 225
    input_size = num_features
    hidden_size = 64
    num_layers = 1 
    output_size = 3

    model = mf.WaveForecastingRNN(input_size, hidden_size, num_layers, output_size)
    model.load_state_dict(torch.load(f'model_weights_{indays}.pth'))
    model.eval()


    data, target = mf.querySqliteData()

    # data_use = mf.intoTensor(data)
    input_seq = mf.intoTensor(data)[-240:]
    input_seq = torch.reshape(input_seq, (1, 240, 225))


    # insert result into a sqlite table called predictions, with the date of predictions

    result = model(input_seq)

    # insert result into predictions table in sqlite3
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    print(result[0][0].item())
    try:
        c.execute("INSERT INTO predictions (datetime, WVHT, MWD, APD, inDays) VALUES (?, ?, ?, ?, ?);", (datetime.datetime.now(), result[0][2].item(), result[0][1].item(), result[0][0].item(), indays))
        conn.commit()
        print("inserted into predictions table")
        conn.close()
    except:
        print("error inserting into predictions table")

    print(model(input_seq))

predictWaves(1)
predictWaves(2)
predictWaves(3)
