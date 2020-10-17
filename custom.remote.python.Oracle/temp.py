# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cx_Oracle
import pandas as pd


def Consulta_Oracle_Bizagi(service, host, port, user, pwd, sql):

    # service = 'BIZAPD.banistmo.corp'
    # host = '10.5.138.30'
    # port = '1526'
    # user = 'DILOAIZA'
    # pwd = 'CDt68(lnB4C#'
    
    
    conn_str = user + "/" + pwd + "@" + host + ":" + port + "/" + service
    
    connection = cx_Oracle.connect(conn_str)
    
    df = pd.read_sql(sql, connection)
    connection.close()
    

    return df

def Condition_validation(self, condition_string, df):
        # MOMARC == 3 & MORESP == 00, CONTEO
        # SUMA == ColumnName
        # df1 = df.loc[(df['MOMARC'] == '3') & (df['MORESP'] == '00'), 'CONTEO']
        # condition_string = condition_string.replace(" ", "")
        indexes = condition_string.split(',')  # check for condition, row and column
        array_cond_row = indexes[0].split('&')
        condition = []
        value = []
        tamano = len(array_cond_row)
        for i in range(0, tamano):
            cond, val = array_cond_row[i].split('==')
            condition.append(cond.strip())
            value.append(val.strip())

        if tamano == 1:
            if condition[0] == 'SUMA':
                df1 = float(df[value[0]].sum())
            elif condition[0] == 'MAX':
                df1 = float(df[value[0]].max())
            else:
                try:
                    df1 = df.loc[(df[condition[0]] == value[0]), indexes[1].strip()]
                    df1 = float(df1.iloc[0])
                except Exception as e:
                    df1 = 0
        if tamano == 2:
            try:
                df1 = df.loc[(df[condition[0]] == value[0]) & (df[condition[1]] == value[1]), indexes[1].strip()]
                df1 = float(df1.iloc[0])
            except Exception as e:
                df1 = 0
        if tamano == 3:
            try:
                df1 = df.loc[(df[condition[0]] == value[0]) & (df[condition[1]] == value[1]) & (df[condition[2]] == value[2]),
                         indexes[1].strip()]
                df1 = float(df1.iloc[0])
            except Exception as e:
                df1 = 0
        return df1

def pointer(condition_string, df):
        # 0,Column_Name
        # condition_string = condition_string.replace(" ", "")
        row, column = condition_string.split(',')  # check for condition, row and column
        try:
            df1 = df.iloc[int(row.strip())][column.strip()]
        except Exception as e:
            df1 = 0
        return df1
    
sql = """select

COUNT(m.idp_tipodemantenimiento) CANTIDAD_CASOS,
m.idp_tipodemantenimiento,
ex.sdescripcion  "TIPO_MANTENIMIENTO"
from 
(select * from BIZAGIGOPBI.WFCASE union ALL select * from BIZAGIGOPBI.WFCASECL) w
join (select * from BIZAGIGOPBI.PVbpm union ALL select * from BIZAGIGOPBI.PVCLbpm) p on w.idCase = p.idcase
join BIZAGIGOPBI.m_cat_beg cat on p.m_cat_beg = cat.idm_cat_beg 
inner join BIZAGIGOPBI.m_beg_infmantenimientos m on cat.idm_beg_infomantenimientos = m.idm_beg_infmantenimientos
inner join BIZAGIGOPBI.p_beg_tipoexcepcion ex on m.idp_tipodemantenimiento = ex.idp_beg_tipoexcepcion
inner join BIZAGIGOPBI.wfuser crea on crea.iduser = m.usuariocreador
inner join BIZAGIGOPBI.m_beg_informacionproceso infp on infp.idm_beg_informacionproceso = m.idm_beg_informacionproceso
left join BIZAGIGOPBI.p_beg_resultadomantenimi res1 on  res1.idp_beg_resultadomantenimi = m.idp_resultadoaprobdirecto
left join BIZAGIGOPBI.p_beg_resultadomantenimi res2 on  res2.idp_beg_resultadomantenimi = m.idp_resultadorecomriesgo
left join BIZAGIGOPBI.p_beg_resultadomantenimi res3 on  res3.idp_beg_resultadomantenimi = m.idp_resultadoaprobacionvp
left join BIZAGIGOPBI.m_beg_solicitante sol on sol.idm_beg_solicitante = cat.idm_beg_solicitante
left join BIZAGIGOPBI.m_beg_clientebeg c on c.idm_beg_clientebeg = sol.idm_beg_clientebeg
LEFT JOIN BIZAGIGOPBI.m_beg_datosempresa de ON de.idm_beg_datosempresa = c.iddatosempresa
LEFT JOIN BIZAGIGOPBI.p_e2e_actividadgener_ek AGEK ON agek.idp_e2e_actividadgener = de.idp_e2e_actividadgener
LEFT JOIN BIZAGIGOPBI.p_e2e_actividadgener AG ON ag.scodigo = agek.scodigo
LEFT JOIN BIZAGIGOPBI.p_e2e_actividadespec_ek AEEK ON aeek.idp_e2e_actividadespec = de.idp_e2e_actividadespec
LEFT JOIN BIZAGIGOPBI.p_e2e_actividadespec AE ON ae.scodigo = aeek.scodigo
LEFT JOIN BIZAGIGOPBI.m_beg_datosgrupo DG ON dg.idm_beg_datosgrupo = c.idm_beg_datosgrupo
LEFT join BIZAGIGOPBI.m_beg_informacioncomerci IC on ic.idm_beg_informacioncomerci = c.idinformacioncomercial
LEFT join BIZAGIGOPBI.p_beg_segmento_ek SEK on sek.idp_beg_segmento = ic.idp_segmento
LEFT join BIZAGIGOPBI.p_beg_segmento S on s.scodigo = sek.scodigo
LEFT join BIZAGIGOPBI.p_beg_banca B on b.idp_beg_banca = ic.idp_banca
LEFT join BIZAGIGOPBI.wfuser UG on ug.iduser = ic.idgerentederelacion
LEFT join BIZAGIGOPBI.wfuser UE on ue.iduser = ic.idejecutivocomercial
LEFT JOIN BIZAGIGOPBI.p_beg_region R ON r.idp_beg_region = ic.idregion
WHERE
ic.idp_banca=2
AND
infp.dfechadecreacion > '01-OCT-20'
GROUP BY m.idp_tipodemantenimiento,ex.sdescripcion
"""

SID = 'BIZAPD.banistmo.corp'
server = '10.5.138.30'
Port = '1526'
User = 'DILOAIZA'
Password = 'CDt68(lnB4C#'

df = Consulta_Oracle_Bizagi(SID, server, Port, User, Password, sql)
 
Metric_Names = '(0,TIPO_MANTENIMIENTO)|(1,TIPO_MANTENIMIENTO)|(2,TIPO_MANTENIMIENTO)|(3,TIPO_MANTENIMIENTO)|(4,TIPO_MANTENIMIENTO)|(5,TIPO_MANTENIMIENTO)|(6,TIPO_MANTENIMIENTO)|(7,TIPO_MANTENIMIENTO)|(8,TIPO_MANTENIMIENTO)|(9,TIPO_MANTENIMIENTO)|(10,TIPO_MANTENIMIENTO)'
Pointer =       '0,CANTIDAD_CASOS|1,CANTIDAD_CASOS|2,CANTIDAD_CASOS|3,CANTIDAD_CASOS|4,CANTIDAD_CASOS|5,CANTIDAD_CASOS|6,CANTIDAD_CASOS|7,CANTIDAD_CASOS|8,CANTIDAD_CASOS|9,CANTIDAD_CASOS|11,CANTIDAD_CASOS'
Condition = ''


Metric_Names = Metric_Names.split('|')
Condition_array = Condition.split('|')
Pointer_array = Pointer.split('|')
print(len(Metric_Names))
print(len(Pointer_array))
for i in range(0, len(Metric_Names)):
    if "(" in Metric_Names[i]:
        Metric_Names[i] = Metric_Names[i].replace('(','')
        Metric_Names[i] = Metric_Names[i].replace(')','')
        Metric_Names[i] = pointer(Metric_Names[i], df) 
    if Pointer == '':
        value = Condition_validation(Condition_array[i], df)
        print("Value: " + value)
        print("Metrics: " + Metric_Names[i])
       #device.absolute("Metric.Tx", value, {"Metrics": Metric_Names[i]})
    else:
        value = pointer(Pointer_array[i], df)
        print(value)
        print("Metrics: " + Metric_Names[i])
        #device.absolute("Metric.Tx", value, {"Metrics": Metric_Names[i]})
    



