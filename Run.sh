 #!/bin/bash

mkdir Logs/
echo "Apakah bahasa yang ingin kamu gunakan ?"
echo "What language would you like to use ?"
echo -n "[Eng/Ind]>>> "
read bahasa

if [[ "$bahasa" == "Eng" ]]; then
python Eng.py
fi

if [[ "$bahasa" == "Ind" ]]; then 
python Ind.py
fi

if [[ "$bahasa" != "Eng" && "$bahasa" != "Ind" ]]; then echo "Pilihan tidak valid. Harap masukkan 'Eng' atau 'Ind'." fi

