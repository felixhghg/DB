#Таблица данных созданная felix-ом предупреждаю то что этот файл, а точнее база данных не будет коммов максимум тут будет комментарии к функциям
__version__ = 0.1
__name__ = "'Astro_db'"
__dev__ = "@lastfelminfonne"
__gitrepo__ = "https://github.com/felixhghg/DB/"

example = f"""__name__ = {__name__}
__version__ = {__version__}
# В случаии не исправностей напишите {__dev__} или откройте Issue на {__gitrepo__+"issues"}
"""

import codecs

class Db:

    def __init__(self,file_name: str = "DB.py",file_format: str = "py"):
        """инициализация"""
        # self.create_db()
        # filenm = file_name.split(".",maxsplit=1)[0]+"."+file_format
        self.format = file_format
        # self.db_name: str = filenm
        self.db_name: str = file_name
        # self.file = open(file=self.db_name,mode="w+",encoding="utf-8")
        self.text = example
        self.tables = []
        self.as_lib = None


    # def init(self):
    #     if not self.check_db():
    #         self.create_db()
    #         file = codecs.open(self.db_name, mode="w+", encoding="utf-8")
    #         file.write(example)
    #     else:
    #         file = codecs.open(self.db_name,mode="w+",encoding="utf-8")
    #
    #     self.file = file
    #     return self


    def create_db(self) -> bool:
        """если нету дб то нету вам дб"""
        try:
            # self.file.close()
            with codecs.open(self.db_name,mode="w+",encoding="utf-8") as f:
                f.write(self.text)
                return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False


    def check_db(self) -> bool:
        """А есть ли ваще?"""
        try:
            with codecs.open(self.db_name,mode="r",encoding="utf-8"):
                return True
        except:
            return False


    def create_table_db(self,**kwargs) -> None:
        """создать таблицу использование:(название таблицы)=(либо тут уже как хотите)"""
        for i,n in kwargs.items():
            self.tables.append(i)

            exec(f"self.{i} = {n}")


    def check_table_db(self,table: str) -> bool:
        """Проверяет существовать ли данная таблица в датабазе"""
        if table in self.tables:
            return True
        else:
            return False

    def write_db(self,**kwargs) -> None:
        """
        добавляет данные
        использование:(название таблицы)=(данные)
        ! Если вы используйте список[] словарь{}, то надо как бы занести в тип ["example"] а не "example"
        """
        self.text = example
        for i,n in kwargs.items():
            table = i
            if n is bool:
                exec(f"self.raw_write_db({i}={n})")
                return
            if self.check_table_db(table=table):
                if isinstance(getattr(self,i),dict):
                    n = {n}
                if isinstance(getattr(self,i),list):
                    n = [n]
                exec(f"self.{i} += {n}")
                return

    def raw_write_db(self,**kwargs) -> None:
        """в аргументы передаете table(любое название)=(любой тип переменной) но прикол в том что он ЗАМЕНЯЕТ данные"""
        for table,data in iter(kwargs):
            exec(f"self.{table} = {data}")


    def portable(self) -> None:
        """Портирует Датабазу и выставляет настройки """
        db = self.raw_read_db()
        self.read_db_file()
        text1 = db.split("\n")[4:]
        for text2 in text1:
            try:
                var: str = text2.split(" = ")[0]
                if "'" not in var and '"' not in var and var != "":
                    self.tables.append(var)
            except:
                print("Non for tables")
        self.load_tables()

    def load_tables(self) -> None:
        """Загрузить таблички(а точнее данные из них)"""
        self.read_db_file()
        as_lib=self.as_lib
        # print(self.tables)
        for i in self.tables:
            setattr(self, i, getattr(as_lib, i))
            # t = eval(f"as_lib.{i}")
            # exec(f"self.{i} = {t}")
            # eval(f"print(self.{i})")


    def save_db(self) -> None:
        """Сохраняет Датабазу"""
        text = self.text

        for table in self.tables:
            text += f"\n\n{table} = {getattr(self, table)}"
        self.text = text
        self.as_lib = None
        self.create_db()


    def raw_read_db(self) -> str:
        """Нужно для табличек"""
        with codecs.open(self.db_name,"r","utf-8") as f:
            text = f.read()
            return text


    def read_db_file(self) -> None:
        """типо просто надо, но оно и само может(portable, read table) к слову из self.as_lib можно вытянуть всю ДБ"""
        try:
            as_lib = __import__(self.db_name.split("."+self.format,maxsplit=1)[0])
            # print(as_lib)
            self.as_lib = as_lib
        except ImportError as e:
            print(f"Ошибка: {e}")


    def __str__(self) -> str:
        """не знаю для чего она вам, но выдает СЫРУЮ дб в виде текста"""
        st = self.raw_read_db()
        return st
    