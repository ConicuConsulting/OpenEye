CREATE CONSTRAINT ON (t:Title) ASSERT t.title_number IS UNIQUE;
CREATE CONSTRAINT ON (s:Section) ASSERT s.id IS UNIQUE;

// Example node creation
CREATE (t1:Title {title_number: 1, name: "GENERAL PROVISIONS"});
