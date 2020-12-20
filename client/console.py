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
            source_info[2] = str(input("edited search link: ")).strip()
            try:
                i = source_info[2].index("[query]")
            except ValueError:
                print("[query] marcation missing")
                source_info[2] = ""
        while source_info[3] == "":
            source_info[3] = str(input("edited manga link: ")).strip()
            try:
                i = source_info[3].index("[mangaName]")
            except ValueError:
                print("[mangaName] marcation missing")
                source_info[3] = ""
        while source_info[4] == "":
            source_info[4] = str(input("edited chapter link: ")).strip()
            try:
                i = source_info[4].index("[mangaName]")
                j = source_info[4].index("[chapterNum]")
            except ValueError:
                print("[mangaName] or [chapterNum] marcation missing")
                source_info[4] = ""
        while source_info[5] == "":
            source_info[5] = str(input("edited image in chapter link: ")).strip()
            try:
                i = source_info[5].index("[image]")
            except ValueError:
                print("[image] marcation missing")
                source_info[5] = ""
        
        result = self.db.execute("INSERT INTO sources (name, home_link, search_link, manga_link, chap_link, img_link)"
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
                to_be_deleted = result[0][0]
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
            delete_exec = self.db.execute(f"DELETE FROM sources WHERE id = {to_be_deleted};")
            if type(delete_exec) == bool and delete_exec:
                print(f"Removed source [{to_be_deleted}] {result[sources_ids.index(to_be_deleted)][1]}")
            elif type(delete_exec) == str:
                print(delete_exec)
            elif not delete_exec:
                print("Source not removed, something went wrong!")
    
    def edit_f(self, source_name: str):
        result = self.db.read(f"SELECT id, name FROM sources WHERE name LIKE '%{source_name}%';")
        if len(result) == 0:
            print("No sources found!")
        elif type(result) == str and self.printErrors:
            print(result)
        elif type(result) == list and len(result) > 0:
            to_be_edited = -1
            if len(result) == 1:
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
        edit_sql = self.db.readOne(f"SELECT name, home_link, search_link, manga_link, chap_link, img_link FROM sources WHERE id = {source_id};")
        if type(edit_sql) == tuple:
            print(f"Editing [{source_id}] {edit_sql[0]}")
            columns   = ["name", "home_link", "search_link", "manga_link", "chap_link", "img_link"]
            new_infos = ["", "", "", "", "", ""]
            temp = str()
            
            # editing name
            print("\nEditing NAME")
            print("Actual NAME: " + edit_sql[0])
            temp = str(input("New source name: ")).strip()
            if temp == "":
                print("NAME was not updated")
            else:
                new_infos[0] = temp
                print("Updated NAME")
            
            # editing home_link
            print("\nEditing HOMEPAGE LINK")
            print("Actual HOMEPAGE LINK: " + edit_sql[1])
            temp = str(input("New homepage link: ")).strip()
            if temp == "":
                print("HOMEPAGE LINK was not updated")
            else:
                new_infos[1] = temp
                print("Updated HOMEPAGE LINK")

            # editing search_link
            print("\nEditing SEARCH LINK")
            print("Actual SEARCH LINK: " + edit_sql[2])
            while 1:
                temp = str(input("New edited search link: ")).strip()
                if temp == "":
                    print("SEARCH LINK was not updated")
                    break
                try:
                    _ = temp.index("[query]")
                except ValueError:
                    print("[query] marcation missing")
                else:
                    new_infos[2] = temp
                    print("Updated SEARCH LINK")
                    break

            # editing manga_link
            print("\nEditing MANGA LINK")
            print("Actual MANGA LINK: " + edit_sql[3])
            while 1:
                temp = str(input("New edited manga link: ")).strip()
                if temp == "":
                    print("MANGA LINK was not updated")
                    break
                try:
                    _ = temp.index("[mangaName]")
                except ValueError:
                    print("[mangaName] marcation missing")
                else:
                    new_infos[3] = temp
                    print("Updated MANGA LINK")
                    break
            
            # editing chap_link
            print("\nEditing CHAPTER LINK")
            print("Actual CHAPTER LINK: " + edit_sql[4])
            while 1:
                temp = str(input("New edited chapter link: ")).strip()
                if temp == "":
                    print("CHAPTER LINK was not updated")
                    break
                try:
                    _ = temp.index("[mangaName]")
                    _ = temp.index("[chapterNum]")
                except ValueError:
                    print("[mangaName] or [chapterNum] marcation missing")
                else:
                    new_infos[4] = temp
                    print("Updated CHAPTER LINK")
                    break
            
            # editing img_link
            print("\nEditing IMAGE LINK")
            print("Actual IMAGE LINK: " + edit_sql[4])
            while 1:
                temp = str(input("New edited image link: ")).strip()
                if temp == "":
                    print("IMAGE LINK was not updated")
                    break
                try:
                    _ = temp.index("[image]")
                except ValueError:
                    print("[image] marcation missing")
                else:
                    new_infos[5] = temp
                    print("Updated IMAGE LINK")
                    break

            # updating the sql
            updating = list()
            for index, new_info in enumerate(new_infos):
                if new_info != "":
                    updating.append([index, new_info])
            if len(updating) > 0:
                update_sql = "UPDATE sources SET "
                temp = str()
                for upd in updating:
                    temp += f"{columns[upd[0]]} = '{upd[1]}'"
                    if updating.index(upd) != len(updating) - 1:
                        temp += ", "
                update_sql += f"{temp} WHERE id = {source_id};"
                
                final_exec = self.db.execute(update_sql)
                if type(final_exec) == bool and final_exec:
                    print(f"Updated source [{source_id}]", end=" ")
                    print(edit_sql[0] if new_infos[0] == "" else new_infos[0])
                elif type(final_exec) == str:
                    print(final_exec)
                elif not final_exec:
                    print("Source not edited, something went wrong!")
            else:
                print("Nothing updated")
        else:
            print("Something went wrong!")
        