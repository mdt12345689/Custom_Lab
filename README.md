Labtainers: A Docker-based cyber lab framework
==============================================

Labtainers include more than 50 cyber lab exercises and tools to build your own. Import a single [VM appliance][vm-appliance] or install on a Linux system and your students are done with provisioning and administrative setup, for these and future lab exercises.  

* Consistent lab execution environments and automated provisioning via Docker containers
* Multi-component network topologies on a modestly performing laptop computer 
* Automated assessment of student lab activity and progress
* Individualized lab exercises to discourage sharing solutions

## Content
[Distribution and Use](#distribution-and-use)

[Guide to directories](#guide-to-directories)

[Support](#support)

[Release notes](#release-notes)

## Distribution and Use
Please see the licensing and distribution information
in the [docs/license.md file](docs/license.md).

## Guide to directories

* scripts/labtainers-student -- the work directory for running and 
   testing student labs.  You must be in that directory to run 
   student labs.
   
* scripts/labtainers-instructor -- the work directory for 
   running and testing automated assessment and viewing student
   results.
  
* labs -- Files specific to each of the labs
   
* setup\_scripts -- scripts for installing Labtainers and Docker and updating Labtainers
   
* docs -- latex source for the labdesigner.pdf, and other documentation.

* UI -- Labtainers lab editor source code (Java).


January 24, 2018

-  Use of tabbed windows caused instructor side to fail, use of double quotes.
-  Ignore files in \_tar directories (other than .tar) when determining build
   dependencies.

