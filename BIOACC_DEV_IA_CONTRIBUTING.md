How to Contribute as a developer/IA data scientist/bioaccoustician ? 

NBM is an open source project everyone can contribute at. 

If you are a developer/IA data scientist/bioaccoustician, we hope this document makes the contribution process clear and answers questions you may have. Don't hesitate to propose any improvement to it ! 

Requirements : <br>
     • Download Git on your computer : https://git-scm.com/downloads <br>
     • Git clone the repository on your machine : git clone https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration.git <br>
     • Having one code editor (such as VSCode, Atom or whatever) will help you a lot <br>
<br>
Then follow the step : 
1. GitLab : Find/create the issue you want to work on 
2. GitLab : Create a merge request, if not done 
3. Your computer : Pull the branch, develop and push 

## First step : GitLab - Find/create the issue you want to work on ## 

The project is structured in **milestones** : general objective to reach. 
These milestones gather **issues** or functionnalities than can be developed. 

Find the issue or create an issue for a functionnality, a part of code you want to develop. 
When creating an issue, make sure that it can be understood by everyone with an understanble title and a short description.

## Second step : GitLab - Create a merge request to the issue, if not done ## 

<img align="right" width="600" height="250" src="/uploads/59bbe0b5d87f7a7ac10f48552ed83764/MR_example.png">
<br><br>
When you click on an issue, there is the possibility to create a Merge Request (MR), top right.

When creating the MR, there is a possibility to create an associate branch. Create the branch from the **dev** branch if it does not exist.

This created branch is a copy of the last points/improvements/developments reached by the origin branch ("dev" or "AI"). 
<br><br>
## Third step : Go to your development environment

Go to your VSCode or other code editor. 

First : git checkout "the branch that you have created for your merge request" 
Optionnal : if it has been a while that you have created the merge request or someone else work on the same issue you do (not good) : 
Pull the origin branch ("dev" or "AI")

Second : Develop, add, modify, delete, change everything you need to have a working functionnality 

Third : this is git flow (git add then git commit and finally git push (to the good branch))

For those who are not used to git, part of the flow is explained here :
<br>
<br>
<br> 
<img align="right" width="600" height="250" src="/uploads/dc22b4838d6fc0ba7cb5cec4ef6fb9ff/git_operations.png">

<br>
(Source : http://www.silanus.fr/nsi/premiere/git/git.html)

<br>
<br>

## Fourth step : GitLab - Mark your Merge Request as ready and wait for validation 

A MR must be validated at least one time for an AI one and twice for a development one. 
To propose your MR to the community, set your/the MR as ready ("Mark as ready").

Adrien Pajot, for the NBM community 
