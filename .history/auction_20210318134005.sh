curl --request POST \
  --url http://0.0.0.0:8080/new_auction \
  --header 'content-type: application/json' \
  --data '{\n"players": [1 2]\n}' &

sleep 15

curl --request POST \
  --url http://0.0.0.0:8080/end_auction \
  --header 'cache-control: no-cache' \
  --header 'content-type: application/json' \
  --data '{\n	"auction_id": 1\n}'