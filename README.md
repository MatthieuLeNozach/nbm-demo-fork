# NBM - Nocturnal Bird Migration

![SpeciesfromSound_birdfalloutRalphEldridgemachiassealisland_20200921160702_20200921141043__1_](/uploads/ec07a2b80dd785cfb1494efa40d25890/SpeciesfromSound_birdfalloutRalphEldridgemachiassealisland_20200921160702_20200921141043__1_.jpg)
Millions of bird are migrating by night everywhere on Earth - When conditions are not favorable, some are stopping where they can, as on the Machias Seal Island, this night of May 2011, the 24th (Picture from Ralph Eldridge)
Problem

Twice a year, millions of birds are migrating on every continents, this phenomenon is called migration and is well documented. However, nocturnal migration has been little studied because of the difficulty to follow birds by night and to identify them uniquely by the sound. Nowadays most of the flight call for the northern hemisphere species at least, are well documented and many researchers and birders are recording continuously migration activity by night, representing tons of data to treat. You understood the problem then : how to analyse hours of night recording automatically by identifying the sequence of interest, extracting it, making it corresponding with a species and store the data somewhere (and linking it to the weather ?) ?
Idea
This wonderful question has been studied at different steps, our job is to find a way to :

1/ Find and extract an audio sequence of interest during night migration and to store it properly (hour, characteristics). This will help people to first identify them directly without browsing the whole sequence

2/ Explore the characteristics of the sound and making it correspond to a species. Artificial intelligence !

Image alt: image Capture_decran_20200921_a_221022.jpg (0.5MB)


Night migration flight call identification principle

3/ Store the data properly. Indeed, once the bird has been identified, it is important to store its occurence somewhere. Imagine, putting all the observations of citizen recording in real time in a database and making it available to science ?

The construction of a GeoNature module could be a solution ? Xeno-Canto partnership ?

4/ And... finally.. all the interest is to put the observation in a context and particularly a climatic one : what is the weather and how is it linked to the data. Questions that could be answered with an information system.

Image alt: image Capture_decran_20200921_a_222406.jpg (0.4MB)

The absence of wind is great to have a good quality of recording. However, storms and westerly winds are particularly interesting to observe night migration because the bring lot of informations and unusual migrants which routes have been changed, allowing us to put this phenomenon in perspective
Papers
Salamon et al, 2016, Towards the Automatic Classification of Avian Flight Calls for Bioacoustic Monitoring : https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5120805/

The sound approach, 2020, The Sound Approach guide to nocturnal flight calls : https://soundapproach.co.uk/the-sound-approach-guide-to-nocturnal-flight-calls/

Trektellen, , A protocol for standardized nocturnal flight call monitoring : https://www.trektellen.nl/static/doc/Protocol_for_standardised_nocturnal_flight_call_monitoring_v01.pdf
Links
The full story of an extraordinary night of migration on the American continent : http://www.thenaturalistsnotebook.com/our-blog/migrating-bird-fallout-on-machias-seal-island

‘Nocmig’ (or Night Flight Call / NFC recording as it’s known in North America) is the nocturnal equivalent of visible migration watching, and typically employs sound recording equipment to capture the flight calls of migrating birds. Whether you’re interested in new birds for your garden list or keen to record migration more systematically, knowing where to start can seem baffling. Here we aim to collate information and tips about the developing – and captivating! – world of nocmig.With a modest investment in some recording equipment (as little as £10) and some free software to process recordings, you can start to identify birds migrating over your location each night. You’ll be amazed at the range of species you’ve been missing – you may have heard Redwings on calm autumn evenings but you should be able to add Blackbird, Song Thrush, Fieldfare and perhaps Ring Ouzel, waterbirds such as Coot, Moorhen and Water Rail, and passage waders like Whimbrel and Golden Plover. If you’re really lucky there are rarities like Bittern, Common Scoter and Ortolan Bunting for the finding. If you need more motivation, read more here.

Based on recommendations from current recordists, we’ve summarised the different equipment options available and offer tips for how, where and when to record. We provide step-by-step instructions for using free audio software to process your night-long recordings to find bird vocalisations of interest. And if you’re lucky enough to record a bird you don’t recognise, we maintain links to the latest identification information.This is very much a ‘work in progress’, so if there something obvious missing please tell us.Contributors and acknowledgmentsThese pages are written and maintained by Simon Gillings and Nick Moran. As relative newcomers to the nocmig world we’ve learnt a lot from experimentation and informed by tips from seasoned ‘nocmiggers’. In particular, we thank Joost van Bruggen, Patrick Franke, Nick Hopper, Mark Lewis, James Lidster, Tim Jones, Paul Morton and Magnus Robb. https://nocmig.com/


Data

Software plan
Therefore a software could be created and the process is as following :1/ Record a whole night with your microphone2/ Put your recording on your computer3/ Open the software and put your recording on it4/ Process5/ After few times, the software tells you each sequence it found6/ It associates each sequence with a species it it can. If not possible it tells you.7/ Therefore your have a table with as many lines as you have sequences and three columns : sequence, species identified and a third one : validation8/ Validation is the most important part : you have the choice either to let it as "not checked", validate it or not.If you validate it, you bring more data to the AI. If not, you can correct it by the species you identified9/ You have a submission button that send all your data to the database with is linked a collaborative platform (Trektellen in Europe ? eBird worldwide after having completed your metadata).10/ The database received all your sequencies and store them on Xeno-Canto for example, with an API. Moreover, it learns more and more how to recognize species.

Other plan

1/ Recorders cartography

As Trektellen does, we could imagine a cover from all recorders :