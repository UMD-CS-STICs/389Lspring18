ERR_MSG='Provide a URL as a parameter: ./lat_test.sh https://example.com/an/image.jpeg'
URL=${1:?$ERR_MSG}

echo "Testing: $URL"

curl -s -o /dev/null -w \
'
time_namelookup: %{time_namelookup} 
time_connect:  %{time_connect}
time_appconnect:  %{time_appconnect}
time_pretransfer:  %{time_pretransfer}
time_redirect:  %{time_redirect}
time_starttransfer:  %{time_starttransfer}
-
time_total: %{time_total}\n' \
$URL
