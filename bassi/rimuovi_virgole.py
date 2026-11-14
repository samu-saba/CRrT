import os

def remove_commas_from_filenames(root_dir):
    print(f"Scansione della cartella: {root_dir}")
    count = 0
    
    # os.walk con topdown=False permette di rinominare prima i file e poi le cartelle (se necessario)
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            if ',' in filename:
                old_path = os.path.join(dirpath, filename)
                new_filename = filename.replace(',', '')
                new_path = os.path.join(dirpath, new_filename)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"[RINOMINATO] '{filename}' -> '{new_filename}'")
                    count += 1
                except Exception as e:
                    print(f"[ERRORE] Impossibile rinominare '{filename}': {e}")
                    
    print(f"Operazione completata. Totale file rinominati: {count}")

if __name__ == "__main__":
    target_folder = r"F:\Progetti Git\CRrT"
    if os.path.exists(target_folder):
        remove_commas_from_filenames(target_folder)
    else:
        print(f"La cartella {target_folder} non esiste.")
