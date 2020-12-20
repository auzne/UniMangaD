import os

from utils.conn import Database

class Application:
    def __init__(self, printErrors: bool = False):
        self.db = Database()
        self.printErrors = printErrors

    def start(self):
        functions_list = [self.list_f, self.add_f, self.remv_f, self.edit_f, self.open_f]
        commands_list  = ['list', 'add', 'remove', 'edit', 'open']
        self.printHeader()
        while 1:
            command = str(input("-> ")).strip().lower().split(' ')
            if command[0] in commands_list:
                functions_list[commands_list.index(command[0])](' '.join(command[1:]) if command[0] not in ["list", "add"] else bool)

    def printHeader(self):
        if os.name == "nt":
            os.system("cls")
        else: 
            os.system("clear")
        print("Universal manga downloader")
        print("README.md for more info\n")
    
    def list_f(self, _):
        all_sources = self.db.read("SELECT id, name FROM sources;")
        if len(all_sources) == 0:
            print("No sources found!")
        if type(all_sources) == str and self.printErrors:
            print(all_sources)
        elif type(all_sources) == list and len(all_sources) > 0:
            for source in all_sources:
                print(f" [{source[0]}] {source[1]}")

    def add_f(self, warn_user: bool = True):
        self.printHeader()
        if warn_user:
            print("Make sure to read README.md to do this right")
        print("Adding a source")
        source_info = ["", "", "", "", "", ""]
        while source_info[0] == "":
            source_info[0] = str(input("Source name: ")).strip()
        while source_info[1] == "":
            source_info[1] = str(input("Homepage link: ")).strip()
        while source_info[2] == "":
            source_info[2] = str(input("Eddited search link: ")).strip()
            try:
                i = source_info[2].index("[query]")
            except ValueError:
                print("[query] marcation missing")
                source_info[2] = ""
        while source_info[3] == "":
            source_info[3] = str(input("Eddited manga link: ")).strip()
            try:
                i = source_info[3].index("[mangaName]")
            except ValueError:
                print("[mangaName] marcation missing")
                source_info[3] = ""
        while source_info[4] == "":
            source_info[4] = str(input("Eddited chapter link: ")).strip()
            try:
                i = source_info[4].index("[mangaName]")
                j = source_info[4].index("[chapterNum]")
            except ValueError:
                print("[mangaName] or [chapterNum] marcation missing")
                source_info[4] = ""
        while source_info[5] == "":
            source_info[5] = str(input("Eddited image in chapter link: ")).strip()
            try:
                i = source_info[5].index("[image]")
            except ValueError:
                print("[image] marcation missing")
                source_info[5] = ""
        
        result = self.db.execute("INSERT INTO sources (name, home_link, search_link, manga_link, cap_link, img_link)"
            + f"VALUES ('{source_info[0]}', '{source_info[1]}', '{source_info[2]}', '{source_info[3]}', '{source_info[4]}', '{source_info[5]}');")
        if type(result) == bool and result:
            print("Source added!")
        elif type(result) == str:
            print(result)
        elif not result:
            print("Source not added, something went wrong!")
    
    def remv_f(self, source_name: str):
        result = self.db.read(f"SELECT id, name FROM sources WHERE name LIKE '%{source_name}%';")
        if len(result) == 0:
            print("No sources found!")
        elif type(result) == str and self.printErrors:
            print(result)
        elif type(result) == list and len(result) > 0:
            if len(result) == 1:
                print(f"Removed source [{result[0][0]}] {result[0][1]}")
                self.db.execute(f"DELETE FROM sources WHERE id = {result[0][0]};")
            else:
                sources_ids = list()
                for source in result:
                    print(f"[{source[0]}] {source[1]}")
                    sources_ids.append(source[0])
                to_be_deleted = -1
                while to_be_deleted not in sources_ids:
                    num = str(input("Enter source id to delete: ")).strip()
                    try:
                        num = int(num)
                    except:
                        print("Only numbers")
                    else:
                        to_be_deleted = num
                print(f"Removed source [{to_be_deleted}] {result[sources_ids.index(to_be_deleted)][1]}")
                self.db.execute(f"DELETE FROM sources WHERE id = {result[0][0]};")
    
    def edit_f(self, source_name: str):
        result = self.db.read(f"SELECT id, name FROM sources WHERE name LIKE '%{source_name}%';")
        if len(result) == 0:
            print("No sources found!")
        elif type(result) == str and self.printErrors:
            print(result)
        elif type(result) == list and len(result) > 0:
            to_be_edited = -1
            if len(result) == 1:
                print(f"Editing [{result[0][0]}] {result[0][1]}")
                to_be_edited = result[0][0]
            else:
                sources_ids = list()
                for source in result:
                    print(f"[{source[0]}] {source[1]}")
                    sources_ids.append(source[0])
                while to_be_edited not in sources_ids:
                    num = str(input("Enter source id to edit: ")).strip()
                    try:
                        num = int(num)
                    except:
                        print("Only numbers")
                    else:
                        to_be_edited = num
            self.editor(to_be_edited)
    
    def open_f(self, source_name: str):
        # to do
        print("open_f " + source_name)
    
    def editor(self, source_id: int):
        # to finish
        self.printHeader()
        edit_sql = self.db.readOne(f"SELECT name, home_link, search_link, manga_link, cap_link, img_link FROM sources WHERE id = {source_id};")
        new_infos = ["", "", "", "", "", ""]
        # editing name
        print("Editing NAME")
        print(f"Original: {edit_sql[0]}")
        