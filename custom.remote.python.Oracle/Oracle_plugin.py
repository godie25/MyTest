import logging
from ruxit.api.base_plugin import RemoteBasePlugin
from ruxit.api.exceptions import AuthException, ConfigException

logger = logging.getLogger(__name__)
import pandas as pd
from Oracle import Consulta_Oracle


class Oracle_Connection(RemoteBasePlugin):
    def query(self, **kwargs) -> None:
        config = kwargs.get("config")
        logger.info('Plugin Started')
        QueryName = config["QueryName"]
        server = config["server"]
        User = config["User"]
        Password = config["Password"]
        sql = config["Query"]
        Metric_Names = config["Metric_Names"]
        Condition = config["Condition"]
        Pointer = config["Pointer"]
        Port = config["Port"]
        SID = config["SID"]
########################################################################
        if server == '':
            raise ConfigException('Hostname or IP cannot be empty. You must provide this to connect to an ODBC')

        if User == '' or Password == '':
            raise ConfigException('You must provide a username and password to connect to this iSeries host')

        if sql == '':
            raise ConfigException('You must provide a query')

        if Metric_Names == '':
            raise ConfigException('You must provide a list of metric names')

        if Condition == '' and Pointer == '':
            raise ConfigException('You must provide a condition or a pointer to extract metrics from Dataframe')

        if Condition != '' and Pointer != '':
            raise ConfigException('Please provide just one: Condition or Pointer')


        Metric_Names = Metric_Names.split('|')
        Condition_array = Condition.split('|')
        Pointer_array = Pointer.split('|')
        
        #if len(Metric_Names) != (len(Metric_Names) + len(Condition_array)):
            #raise ConfigException('The number of element in Metric_Names and Condition of Pointer must be equal')

        group = self.topology_builder.create_group('Bizagi', 'Bizagi')
        df = Consulta_Oracle(sql, server, User, Password, Port, SID)
        device = group.create_device(f'Bizagi - {QueryName}', f'Bizagi - {QueryName}')
        for i in range(0, len(Metric_Names)):
            if "(" in Metric_Names[i]:
                Metric_Names[i] = Metric_Names[i].replace('(','')
                Metric_Names[i] = Metric_Names[i].replace(')','')
                Metric_Names[i] = self.pointer(Metric_Names[i], df) 
            if Pointer == '':
                value = self.Condition_validation(Condition_array[i], df)
                device.absolute("Metric.Tx", value, {"Metrics": Metric_Names[i]})
            else:
                value = self.pointer(Pointer_array[i], df)
                device.absolute("Metric.Tx", value, {"Metrics": Metric_Names[i]})

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
                    logger.exception(e)
                    logger.exception(str(df))
                    df1 = 0
        if tamano == 2:
            try:
                df1 = df.loc[(df[condition[0]] == value[0]) & (df[condition[1]] == value[1]), indexes[1].strip()]
                df1 = float(df1.iloc[0])
            except Exception as e:
                logger.exception(e)
                logger.exception(str(df))
                df1 = 0
        if tamano == 3:
            try:
                df1 = df.loc[(df[condition[0]] == value[0]) & (df[condition[1]] == value[1]) & (df[condition[2]] == value[2]),
                         indexes[1].strip()]
                df1 = float(df1.iloc[0])
            except Exception as e:
                logger.exception(e)
                logger.exception(str(df))
                df1 = 0
        return df1

    def pointer(self, condition_string, df):
        # 0,Column_Name
        # condition_string = condition_string.replace(" ", "")
        row, column = condition_string.split(',')  # check for condition, row and column
        try:
            df1 = df.iloc[int(row.strip())][column.strip()]
        except Exception as e:
            logger.exception(e)
            logger.exception(str(df))
            df1 = 0
        return df1