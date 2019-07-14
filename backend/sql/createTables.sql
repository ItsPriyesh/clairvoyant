use clairvoyant;

DROP TABLE IF EXISTS `UserDataPoint`;
DROP TABLE IF EXISTS `DataPoint`;
DROP TABLE IF EXISTS `Node`;
DROP TABLE IF EXISTS `User`;

CREATE TABLE User(
   user_id       int not null auto_increment,
   first_name    varchar(255) not null,
   last_name     varchar(255) not null,
   email        varchar(255) not null,
   created_at    datetime,
   password_hash	varchar(255) not null,
   session_token	varchar(255),
   PRIMARY KEY(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Node(
   node_id        int 		 not null auto_increment,
   last_heartbeat datetime 	 not null,
   user_id		 int not null,
   CONSTRAINT Node_user_id FOREIGN KEY (user_id) REFERENCES User(user_id),
   PRIMARY KEY(node_id, last_heartbeat, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE DataPoint(
   data_point_id  int 		 not null auto_increment,
   node_id 		int 		 not null,
   received_at   datetime 	 not null,
   event_type	varchar(255) not null,
   confidence	float		 not null 
   CHECK(confidence >= 0 AND confidence <= 1),
   CONSTRAINT DataPoint_node_id FOREIGN KEY (node_id) REFERENCES Node(node_id),
   PRIMARY KEY(data_point_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
