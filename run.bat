@echo off

echo .
echo ooo        ooooo oooooooooo.   ooo        ooooo oooooooooooo      ooooooooooooo   .oooooo.   ooooooo  ooooo 
echo `88.       .888' `888'   `Y8b  `88.       .888' `888'     `8      8'   888   `8  d8P'  `Y8b   `8888    d8'  
echo  888b     d'888   888      888  888b     d'888   888                   888      888      888    Y888..8P    
echo  8 Y88. .P  888   888      888  8 Y88. .P  888   888oooo8              888      888      888     `8888'     
echo  8  `888'   888   888      888  8  `888'   888   888    "              888      888      888    .8PY888.    
echo  8    Y     888   888     d88'  8    Y     888   888       o           888      `88b    d88'   d8'  `888b   
echo o8o        o888o o888bood8P'   o8o        o888o o888ooooood8          o888o      `Y8bood8P'  o888o  o88888o 
echo oooooooooo.                 .                  oooooooooo.   o8o                    .o8                     
echo `888'   `Y8b              .o8                  `888'   `Y8b  `"'                   "888                     
echo  888      888  .oooo.   .o888oo  .oooo.         888     888 oooo  ooo. .oo.    .oooo888   .ooooo.  oooo d8b 
echo  888      888 `P  )88b    888   `P  )88b        888oooo888' `888  `888P"Y88b  d88' `888  d88' `88b `888""8P 
echo  888      888  .oP"888    888    .oP"888        888    `88b  888   888   888  888   888  888ooo888  888     
echo  888     d88' d8(  888    888 . d8(  888        888    .88P  888   888   888  888   888  888    .o  888     
echo o888bood8P'   `Y888""8o   "888" `Y888""8o      o888bood8P'  o888o o888o o888o `Y8bod88P" `Y8bod8P' d888b    
echo .

echo Version 1.0 - 12/26/24
echo To rename files only - leave 2nd and 3rd prompts empty


set /p input_dir="Enter the directory of the raw data: "
set /p batch_num="Enter batch number: "
set /p method="Enter method currently supported: SCGEN, SCRNZ: "

echo ##ensure that your raw data folder does not contain sequences or other files##

pause

python "G:\PDF DATA\Python\WPy64-31260\notebooks\MAIN.py" "%input_dir%" "%batch_num%" "%method%"

pause