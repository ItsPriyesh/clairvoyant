SELECT @testUser := LAST_INSERT_ID();

-- create nodes
INSERT INTO Node(last_heartbeat, user_id)
VALUES ('2019-01-01 11:38:01.00', @testUser),
	   ('2019-01-01 12:45:01.00', @testUser),
	   ('2019-01-01 10:13:01.00', @testUser);

SELECT @node := LAST_INSERT_ID();

-- create datapoints
INSERT INTO DataPoint (node_id, received_at, event_type, confidence) 
VALUES (@node, '2019-01-01 10:28:01.00', 'EXPLOSION', 0.92),
	   (@node, '2019-01-01 9:38:01.00', 'GUNSHOT', 0.45),
	   (@node, '2019-01-01 7:38:01.00', 'VEHICLE', 0.72);