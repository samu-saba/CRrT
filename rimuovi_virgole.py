import os

def remove_commas_from_files_and_folders(root_dir):
    print(f"Scansione della cartella: {root_dir}")
    count_files = 0
    count_dirs = 0
    
    # topdown=False è fondamentale: elabora prima i file e le cartelle interne, poi quelle esterne
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        
        # 1. Rinomina i file che contengono virgole
        for filename in filenames:
            if ',' in filename:
                old_path = os.path.join(dirpath, filename)
                new_filename = filename.replace(',', '')
                new_path = os.path.join(dirpath, new_filename)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"[FILE RINOMINATO] '{filename}' -> '{new_filename}'")
                    count_files += 1
                except Exception as e:
                    print(f"[ERRORE FILE] Impossibile rinominare '{filename}': {e}")
                    
        # 2. Rinomina le cartelle che contengono virgole
        for dirname in dirnames:
            if ',' in dirname:
                old_path = os.path.join(dirpath, dirname)
                new_dirname = dirname.replace(',', '')
                new_path = os.path.join(dirpath, new_dirname)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"[CARTELLA RINOMINATA] '{dirname}' -> '{new_dirname}'")
                    count_dirs += 1
                except Exception as e:
                    print(f"[ERRORE CARTELLA] Impossibile rinominare '{dirname}': {e}")
                    
    print(f"\nOperazione completata!")
    print(f"- File rinominati: {count_files}")
    print(f"- Cartelle rinominate: {count_dirs}")

if __name__ == "__main__":
    target_folder = r"F:\Progetti Git\CRrT"
    if os.path.exists(target_folder):
        remove_commas_from_files_and_folders(target_folder)
    else:
        print(f"La cartella {target_folder} non esiste.")