Feature: Gather build data from Jenkins
	Obtain build data from Jenkins to find out the number of
	successful builds over time for per-day statistics

Scenario: Find all 10 last successful builds
	Given A Jenkins connection is established
	When We can get a list of builds of a specific job	
	Then We get these 10 builds, but only green ones