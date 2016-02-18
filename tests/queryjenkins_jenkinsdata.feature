Feature: Gather build data from Jenkins
	Obtain build data from Jenkins to find out the number of
	successful builds over time for per-day statistics

Scenario: Find all 10 last successful builds
	Given A Jenkins connection is established
	When We can get a list of builds of a specific job
	And Only green jobs are respected
	And We only want to have the last 10 green builds
	Then We get these 10 build ids