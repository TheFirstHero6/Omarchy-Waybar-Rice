#!/bin/bash

count=$(makoctl list 2>/dev/null | jq -r 'length' 2>/dev/null || echo "0")
if [ "$count" = "0" ]; then
  echo '{"text": "", "tooltip": "No notifications"}'
else
  echo "{\"text\": \"🔔 $count\", \"tooltip\": \"$count notifications\"}"
fi


