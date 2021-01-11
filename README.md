# NBM - Nocturnal Bird Migration

## THE PROBLEM ##

Twice a year, millions of birds are migrating on every continents, this phenomenon is called migration and is well documented. However, nocturnal migration has been little studied because of the difficulty to follow birds by night and to identify them uniquely by the sound. Nowadays most of the flight callS for the northern hemisphere species at least, are well documented and many researchers and birders are recording continuously migration activity by night, representing tons of data to treat. 
You understood the problem then : how to analyse hours of night recording automatically ? 

![SpeciesfromSound_birdfalloutRalphEldridgemachiassealisland_20200921160702_20200921141043__1_](/uploads/ec07a2b80dd785cfb1494efa40d25890/SpeciesfromSound_birdfalloutRalphEldridgemachiassealisland_20200921160702_20200921141043__1_.jpg) 
<img src="/uploads/ec07a2b80dd785cfb1494efa40d25890/SpeciesfromSound_birdfalloutRalphEldridgemachiassealisland_20200921160702_20200921141043__1_.jpg"  width="120" height="120">

Millions of bird are migrating by night everywhere on Earth - When conditions are not favorable, some are stopping where they can, as on the Machias Seal Island, this night of May 2011, the 24th (Picture from Ralph Eldridge)

## BEGINNING OF THE PROJECT ##

To answer this question we gathered two companies, Natural Solutions (https://www.natural-solutions.eu/) and BioPhonia (http://www.biophonia.fr/) and propose a challenge in the context of the Hack4Nature (https://www.hackfornature.com/).

Therefore a community of birders, bioaccousticians and developers started the project to discuss about the topic and how it can be treated. 

We opened a Discord chat you can join with this link (in french) : https://discord.gg/95SNguK3tP 

## THE PROJECT ##

With the *bioaccousticians groupe* we identified many issues that have to be explored : <br>
1/ Can we detect a sound recorded from different background, different recorders in different places and at different dates ? 
<br>
2/ Can we separate a bird call from other biophonia or anthropophonia sounds ? 
<br>
3/ Can we identify the species ?
<br>

![SpeciesfromSound_Capture_decran_20200921_a_221022_20200921220823_20200921201138](/uploads/bb19c399eb66f97eab18b6b86ab26234/SpeciesfromSound_Capture_decran_20200921_a_221022_20200921220823_20200921201138.jpg)

AI is able to do so, with good algorithm, lot of training and annotated data. 
As always with AI, the quantity and the quality of data is the main issue. 

It is why we need you birders ! 
Want to participate to this project and don't know how ? Follow the link below ! 
https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/blob/master/BIRDERS_CONTRIBUTING.md

Then, the first step is to construct a database that is under Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) licence (https://creativecommons.org/licenses/by-sa/4.0/) and can be reusable by any people wanted to work with bird sounds. 
The database is for the moment a servor to store the soundfiles you can find at this link : http://91.121.179.208/nextcloud/index.php/s/SW3BG4DJ8Y5MXqp

However, we will create a PostGre database (https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/3) that must be linked with a web platform in order to birders be able to enter data more easily and bioaccousticians to extract them. The features for the plateform are described and discussed here : https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/1 

From these data, bioaccousticians will be able to start training their AI. With many existing projects worlwide, we don't want to create something new but want to adapt and improve existing AI :  
    For the detection, here are the discussions :  https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/7
    <br>
    For the separation between bird sounds, here are the discussions :  https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/5
    <br>
    For the identification, here are the discussions : https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/6
    <br>
All together, here are the explored topics for the AI : 

When the first results of the AI will be on, the next challenge will be to implement this AI in an editor birders can download on their computer to process their night. Here are the discussions for this editor : 

## Technologies ##

Annotations database : 

AI : 

Editor : 

## Licence ## 

• Licence : OpenSource - GPL-3.0
• Copyleft 2020-20XX - NBM Community - BioPhonia - Natural Solutions
 
