use clairvoyant;

SELECT @testUser := user_id FROM User 
WHERE email = 'test@test.com';

-- create nodes
INSERT INTO Node(last_heartbeat, user_id)
VALUES ('2019-01-01 11:38:01.00', @testUser),
	   ('2019-01-01 12:45:01.00', @testUser),
	   ('2019-01-01 10:13:01.00', @testUser);

SELECT @node := node_id FROM Node
WHERE user_id = @testUser
LIMIT 1;

-- create datapoints
INSERT INTO DataPoint (node_id, received_at, event_type, confidence) 
VALUES (@node, '2019-01-01 10:28:01.00', 'EXPLOSION', 0.92),
	   (@node, '2019-01-01 9:38:01.00', 'GUNSHOT', 0.45),
	   (@node, '2019-01-01 7:38:01.00', 'VEHICLE', 0.72);