# NBM - Nocturnal Bird Migration

![Front_image_NBM](/uploads/b7354c7e72f564900939999b817b2cd8/Front_image_NBM.png)

## THE PROBLEM ##
<img align="right" width="600" height="270" src="/uploads/ec07a2b80dd785cfb1494efa40d25890/SpeciesfromSound_birdfalloutRalphEldridgemachiassealisland_20200921160702_20200921141043__1_.jpg">

Twice a year, millions of birds are migrating on every continents, this phenomenon is called migration and is well documented. However, nocturnal migration has been little studied because of the difficulty to follow birds by night and to identify them uniquely by the sound. Nowadays most of the flight calls for the northern hemisphere species at least, are well documented and many researchers and birders are recording continuously migration activity by night, representing tons of data to treat. 
You understood the problem then : how to analyse hours of night recording automatically ? 

Millions of bird are migrating by night everywhere on Earth - When conditions are not favorable, some are stopping where they can, as on the Machias Seal Island, this night of May 2011, the 24th (Picture from Ralph Eldridge)
<br>
## BEGINNING OF THE PROJECT ##

To answer this question we gathered two companies, Natural Solutions (https://www.natural-solutions.eu/) and BioPhonia (http://www.biophonia.fr/) and propose a challenge in the context of the Hack4Nature (https://www.hackfornature.com/).

<img width="450" height="180" src="/uploads/7ad014a872620614846256079ef1fe9c/logo_BioPhonia.jpg">
<img width="450" height="180" src="/uploads/e974f8f4715b4bbb5d766e5f97d4e821/logo_NS_fond-blanc.webp">

<br>

Therefore a **community of birders, bioaccousticians and developers** started the project to discuss about the topic and how it can be treated. 

At its scale, everyone, can participate ! You can see how with the contributing.md files displayed for each groupe. <br>
Birders : https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/blob/master/BIRDERS_CONTRIBUTING.md <br>
AI data scientist/developer/bioaccousticians : https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/blob/master/BIOACC_DEV_IA_CONTRIBUTING.md

We opened a Discord chat you can join with this link (in french) : https://discord.gg/95SNguK3tP 

## THE PROJECT ##

### For bioaccousticians ###

Normally, after having put the recording ont its computer, a birder open it with a software that transform the sound file into a spectrogramm. 
Then, the birder browses the audio sequence until he/she detects a sound, plays it and identify what bird it is (when it is a bird) ! 

Therefore, with the **bioaccousticians groupe** we identified many issues that have to be explored : <br>
1/ Can we detect a sound recorded from different background, different recorders in different places and at different dates ? 
<br>
2/ Can we separate a bird call from other biophonia or anthropophonia sounds ? 
<br>
3/ Can we identify the species ?
<br>

With many existing projects worlwide, we don't want to create something new but want to use, adapt and improve existing AI :  
    For the detection, here are the discussions :  https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/7
    <br>
    For the separation between bird sounds, here are the discussions :  https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/5
    <br>
    For the identification, here are the discussions : https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/6
    <br>
All together, here are the explored topics for the AI : https://app.wisemapping.com/c/maps/1073690/public 

Here is a scheme : 
![SpeciesfromSound_Capture_decran_20200921_a_221022_20200921220823_20200921201138](/uploads/bb19c399eb66f97eab18b6b86ab26234/SpeciesfromSound_Capture_decran_20200921_a_221022_20200921220823_20200921201138.jpg)

### For birders ###

AI is able to do so with good algorithm, lot of training and annotated data. 
As always with AI, **the quantity and the quality of data is the main issue**. 

It is why we need you **birders** ! <br>
Want to participate to this project and don't know how ? Follow the link below ! <br>
https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/blob/master/BIRDERS_CONTRIBUTING.md <br>

The first step is to construct a strong database  (under Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) licence (https://creativecommons.org/licenses/by-sa/4.0/)) that can be used for the project and can be reusable by any people wanted to work with bird sounds. 
The database is for the moment a servor to store the soundfiles you can find at this link : http://91.121.179.208/nextcloud/index.php/s/SW3BG4DJ8Y5MXqp

### For developers ###

However, this is not practical to only have a storage servor. We need to create a PostGre database (https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/3) that must be linked with a web platform in order to birders be able to enter data more easily and bioaccousticians to extract them. 

This is how **developers** start contributing !  

The features for the annotation platform are described and discussed here : https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/milestones/1 

In the mean time, developers can start the final platform/application that will allow anyone to have a NBM sotfware on its computer to analyse soundfiles : 

(Scheme how we represent it + Milestone)

Indeed, when the first results from the AI, trained by sound files, developers will have an idea of what and how to implement it, next step ! 

## Technologies ##

Annotations database : 

Annotations platform : 

AI : 

Editor : 

Central platform : 

## Licence ## 

• Licence : OpenSource - GPL-3.0
• Copyleft 2020-20XX - NBM Community - BioPhonia - Natural Solutions
 
