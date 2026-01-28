import csv



"""
מודול קבועים עבור משחק פקמן.

מכיל:
- הגדרות חלון (רוחב, גובה, כותרת)
- גודל אריח בודד במפה
- מפה לוגית (LEVEL_MAP) שמגדירה קירות, מטבעות, פקמן ורוחות.
"""
LEVEL_MAP=[]
# הגדרות חלון
with open("text.txt","r") as file:
    for row in file:
        LEVEL_MAP.append(row.strip())


with open ("data.csv","r")as file:
    num_of_constants=0
    reader=csv.reader(file)
    constants_items=[]
    for row in reader:
        for i in range(len(row)):
            num_of_constants+=1
            constants_items.append(row[i])
    for j in range(num_of_constants//2):
        if constants_items[j]== "WINDOW_WIDTH":
            WINDOW_WIDTH=int(constants_items[j + num_of_constants //2])
        if constants_items[j]== "WINDOW_HEIGHT":
            WINDOW_HEIGHT=int(constants_items[j + num_of_constants //2])
        if constants_items[j]== "WINDOW_TITLE":
            WINDOW_TITLE=str(constants_items[j + num_of_constants //2])
        if constants_items[j]== "TILE_SIZE":
            TILE_SIZE=int(constants_items[j + num_of_constants // 2])

#WINDOW_WIDTH = 800
#WINDOW_HEIGHT = 600
#WINDOW_TITLE = "Pacman Arcade Example"

# גודל אריח במפה (בפיקסלים)
#TILE_SIZE = 32

# מפה:
# # - קיר
# . - מטבע
# P - פקמן (נקודת התחלה לשחקן)
# G - רוח
#LEVEL_MAP = [
 #   "########################",
  #  "#..........##..........#",
   # "#.####.###.##.###.####.#",
    #"#P....................G#",
    #"########################",
#]
