import os, django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChartAnalyze.settings")
django.setup()

from charts.models import PanelCompose

from utils.db_commands import ExecuteSQL
from utils import db_config


class FieldControl:
    def __init__(self, panel_id):
        self.panel_id = panel_id

    def fetch_panel(self):
        """
        获取仪表盘数据对象
        :return:
        """
        p_obj = PanelCompose.objects.get(id=self.panel_id)
        return p_obj

    def fetch_feild(self):
        pass

    def build_dis_and_mst(self, field_set):
        """
        根据数据集字段，生成维度、度量sql查询表达式
        :param field_set:
        :return:
        """
        f_list = []
        for field_obj in field_set:
            # 判断字段聚合类型，如果有聚合类型，代表该字段为度量字段，并通过聚合表达式进行渲染
            if field_obj.mst_type:
                mst_up_type = field_obj.mst_type.value
                f_expression = mst_up_type.format(m_field=field_obj.field)
            else:
                f_expression = field_obj.field

            # 判断字段是否包含别名转换，生成 sql case 表达式
            if field_obj.alias:
                case_condition = ''  # case 条件
                alias_list = eval(field_obj.alias)
                for alias_obj in alias_list:
                    (k, v), = alias_obj.items()
                    if k == 'else':
                        case_condition += 'ELSE "%s" ' % v
                    else:
                        case_condition += 'WHEN "%s" THEN "%s" ' % (k, v)
                f_expression = 'CASE %s %s END' % (field_obj.field, case_condition)

            # 为表达式添加 AS 别名
            f_expression = "({f_expression}) AS FEILD_{f_name}".format(f_expression=f_expression,
                                                                       f_name=field_obj.field)
            f_list.append(f_expression)

            return f_list

    def sql_controller(self, p_dis_format_list, p_mst_format_list, dis_list):
        """
        根据维度、度量等参数拼接sql执行语句；
        :param p_dis_format_list:
        :param p_mst_format_list:
        :param dis_list:
        :return:
        """
        _sql = 'select {mst_expression}, {dis_expression} from test.member_base group by {dis_fields} ;'.format(
            mst_expression=''.join(p_mst_format_list), dis_expression=''.join(p_dis_format_list),
            dis_fields=''.join(dis_list))

        return _sql

    def db_controller(self, sql):
        mysql_conn = db_config.Master_MySQL_DB['test']
        result = ExecuteSQL(mysql_conn, sql, _type='select')
        return result

    def fetch_panel_json(self, sql_exec_result):
        data_list = []
        for f_obj in sql_exec_result:
            data_list.append({'name': f_obj[1], 'value': f_obj[0]})

        return json.dumps(data_list)

    def compose_handler(self):
        """
        数据集控制器
        :return:
        """
        # 获取仪表盘数据
        panel_obj = self.fetch_panel()

        # 获取查询字段数据，生成维度、度量列表
        dis_field_list = list(obj.field for obj in panel_obj.dis.all())  # 维度字段，用于生成sql语句中group by表达式
        p_dis_format_list = self.build_dis_and_mst(panel_obj.dis.all())
        p_mst_format_list = self.build_dis_and_mst(panel_obj.mst.all())

        # 渲染sql查询语句
        sql_statement = self.sql_controller(p_dis_format_list, p_mst_format_list, dis_field_list)

        # 执行sql查询
        sql_exec_result = self.db_controller(sql_statement)
        print(self.fetch_panel_json(sql_exec_result))


if __name__ == '__main__':
    sql_handler = FieldControl(1)
    sql_handler.compose_handler()
