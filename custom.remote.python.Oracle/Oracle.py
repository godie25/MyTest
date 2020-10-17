
import pandas as pd
import cx_Oracle
import time
import datetime as dt


def _calcularHoraInicioYFin(current, windowTime, format_date):
    delta = dt.timedelta(days=0, hours=0, minutes=0, seconds=windowTime)
    if (current.second % windowTime) == 0: #  Estoy en un intervalo exacto
        endHour = current.strftime(format_date)
        iniHour = (current - delta).strftime(format_date)
    else:
        delta_exacto = dt.timedelta(days=0, hours=0, minutes=0, seconds=(current.second % windowTime))
        endHour = (current - delta_exacto).strftime(format_date)
        iniHour = ((current - delta_exacto)-delta).strftime(format_date)

    return iniHour, endHour

def Consulta_Oracle(sql, host, user, passw, port, SID):

    current = dt.datetime.now()
    startTime = current.replace(day=1, hour=0, minute=0, second=0)
    date = startTime.strftime('%d-%b-%y')
    conn_str = user + "/" + passw + "@" + host + ":" + port + "/" + SID
    connection = cx_Oracle.connect(conn_str)
    sql = sql.format(date)
    df = pd.read_sql(sql, connection)
    connection.close()
    return df
