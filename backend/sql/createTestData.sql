use clairvoyant;

SELECT @testUser := user_id FROM User 
WHERE email = 'mnassar@uwaterloo.ca';

-- create nodes
INSERT INTO Node(node_id,last_heartbeat, user_id, battery_level)
VALUES ('1','2019-01-01 11:38:01.00', @testUser, 92.3),
	   ('2','2019-01-01 12:45:01.00', @testUser, 10.2),
	   ('3','2019-01-01 10:13:01.00', @testUser, 100);

SELECT @node := node_id FROM Node
WHERE user_id = @testUser
LIMIT 1;

-- create datapoints
INSERT INTO DataPoint (data_point_id, node_id, created_at, classification, confidence)
VALUES ('c56be2cd0f0244d7aa3a9117ca29579a', @node, '2019-01-01 10:28:01.00', 'EXPLOSION', 0.92),
	   ('7304b98072304a91afdb7da63cda9ec3', @node, '2019-01-01 9:38:01.00', 'GUNSHOT', 0.45),
	   ('fc704b40f0904bb7ab7fddacc0a2f860', @node, '2019-01-01 7:38:01.00', 'VEHICLE', 0.72);
