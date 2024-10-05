CREATE CONSTRAINT FOR (t:Title) REQUIRE t.title_number IS UNIQUE;
CREATE CONSTRAINT FOR (s:Section) REQUIRE s.id IS UNIQUE;

// Example node creation
CREATE (t1:Title {title_number: 1, name: "GENERAL PROVISIONS"});