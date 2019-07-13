#!/bin/bash

mysql -u root -p < ../../sql/createTables.sql

echo "Created tables"

python3 createTestData.py 

echo "Created test user"

mysql -u root -p < ../../sql/createTestData.sql

echo "Created test nodes and data points"