DROP TABLE IF EXISTS `User`;
CREATE TABLE User(
   userID       varchar(255) not null,
   firstName    varchar(255) not null,
   lastName     varchar(255) not null,
   createdDate  date,
   passwordHash	varchar(255) not null,
   PRIMARY KEY(userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Node`;
CREATE TABLE Node(
   nodeID       int 		 not null auto_increment,
   receivedTime datetime 	 not null,
   userID		varchar(255) not null,
   CONSTRAINT Node_userID FOREIGN KEY (userID) REFERENCES User(userID),
   PRIMARY KEY(nodeID, receivedTime, userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `DataPoint`;
CREATE TABLE DataPoint(
   dataPointID  int 		 not null auto_increment,
   nodeID 		int 		 not null,
   receivedTime datetime 	 not null,
   eventType	varchar(255) not null,
   confidence	float		 not null 
   CHECK(confidence >= 0 AND confidence <= 1),
   CONSTRAINT DataPoint_nodeID FOREIGN KEY (nodeID) REFERENCES Node(nodeID),
   PRIMARY KEY(dataPointID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `UserDataPoint`;
CREATE TABLE UserDataPoint(
   userID		varchar(255) not null,
   dataPointID 	int 		 not null,
   CONSTRAINT UserDataPoint_userID FOREIGN KEY (userID) REFERENCES User(userID),
   CONSTRAINT UserDataPoint_dataPointID FOREIGN KEY (dataPointID) REFERENCES DataPoint(dataPointID),
   PRIMARY KEY(dataPointID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;