from typing import Dict, List, Any


class BaseProcess():
    def __init__(self, owner: 'Pipe'):
        import pyelt.pipeline
        if isinstance(owner, pyelt.pipeline.Pipe):
            self.pipe = owner
            self.pipeline = self.pipe.pipeline
        elif isinstance(owner, pyelt.pipeline.Pipeline):
            self.pipeline = owner
        self.dwh = self.pipeline.dwh
        self.runid = self.pipeline.runid
        self.logger = self.pipeline.logger
        self.sql_logger = self.pipeline.sql_logger

    def execute(self, sql: str, log_message: str='') -> None:
        self.sql_logger.log_simple(sql + '\r\n')
        try:
            rowcount = self.dwh.execute(sql, log_message)
            self.logger.log(log_message, rowcount=rowcount, indent_level=5)
        except Exception as err:
            if 'on_errors' in self.dwh.config and self.dwh.config['on_errors'] == 'throw':
                raise Exception(err, sql, log_message)
            else:
                self.logger.log_error(log_message, sql, err.args[0])

    def execute_read(self, sql: str, log_message: str='') -> List[List[Any]]:
        self.sql_logger.log_simple(sql + '\r\n')
        result = []
        try:
            result = self.dwh.execute_read(sql, log_message)

            self.logger.log(log_message, indent_level=5)
        except Exception as err:
            self.logger.log_error(log_message, sql, err.args[0])
            raise Exception(err)
            # if 'on_errors' in self.dwh.pyelt_config and self.dwh.pyelt_config['on_errors'] == 'throw':
            #     raise Exception(err)
            # else:
            #     print(err.args)
            #     print(sql)
            #     raise Exception(err)
        finally:
            return result

    def execute_without_commit(self, sql: str, log_message: str=''):
        self.sql_logger.log_simple(sql + '\r\n')

        try:
            self.dwh.execute_without_commit(sql, log_message)

            self.logger.log(log_message, indent_level=5)
        except Exception as err:
            self.logger.log_error(log_message, sql, err.args[0])
            raise Exception(err)

    def _get_fixed_params(self) -> Dict[str, Any]:
        params = {}
        params['runid'] = self.runid
        return params


