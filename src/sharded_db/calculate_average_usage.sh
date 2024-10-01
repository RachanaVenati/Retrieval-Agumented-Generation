#!/bin/bash

total_usage=0
total_available=0

for i in {0..9}
do
  # Get the disk usage and available percentages
  usage=$(kubectl exec -it weaviate-$i -n webisstud -- /bin/sh -c "df -h /var/lib/weaviate" | awk 'NR==2 {print $5}' | sed 's/%//')
  available=$(kubectl exec -it weaviate-$i -n webisstud -- /bin/sh -c "df -h /var/lib/weaviate" | awk 'NR==2 {print $4}' | sed 's/%//')

  # Add to the total
  total_usage=$((total_usage + usage))
  total_available=$((total_available + (100 - usage)))
done

# Calculate the total percentage usage
if [ $total_available -gt 0 ]; then
  total_percentage=$((100 * total_usage / (total_usage + total_available)))
  echo "Total Disk Usage: $total_percentage%"
else
  echo "No data to calculate usage."
fi
