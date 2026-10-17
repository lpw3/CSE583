mkdir pronto
cd pronto
touch README.txt
echo "Downloads Pronto data from AWS into folder" > README.txt
mkdir data
cd data
curl -LO https://s3.amazonaws.com/pronto-data/open_data_year_one.zip 
unzip open_data_year_one.zip
head 2015_trip_data.csv
