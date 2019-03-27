# Guitar Data Explorer

## Introduction
Welcome! This tool's purpose is to allow exploration of guitar models to help you to find your dream instrument. It can also be used for general research purposes to answer questions such as:
1. What is a given brand's niche with regard to feature-set?
2. What features are most associated with higher-end models?
3. When comparing comparable instruments, how much of a premium is placed on American-made?

<img alt="Guitar Data Explorer" src="screenshot.png" width="75%">
[TRY IT](https://astronge.github.io) *Best viewed using a screen of resolution 1920x1080 or above.*

## Instructions
### Interacting
The dashboard contains a number of charts that display information related to features that may be found on a guitar, such as the body shape or fretboard material. Interact with the charts by clicking on them to filter for the features that you are interested in. Selecting a feature from a particular category will filter out all models that do not have the particular feature set you have selected for.  

### Filtering
Within a feature, selections are OR and between features selections are AND.  For example, selecting "Double Cutaway" from Body Shape and both "Maple" and "Rosewood" for fretboard material, the resulting filter would be equivalent to the following SQL query:
```
SELECT guitars 
  FROM guitar
 WHERE (body_shape = "Double Cutaway") 
   AND (fretboard_material = "Maple" OR fretboard_material = "Rosewood")
```
The number in the header bar refers to how many guitars meet your filtering criteria.

### Viewing Results
Once you are satisfied with your selections, clicking the RESULTS button will open the results panel for you to be able to scroll through the list of guitars that was returned. 

### Call to Action
Once you have identified the right instrument, clicking on its image will take you Musicians Friend website where you may complete your purchase. Go ahead, you deserve it!

## Project Design
### Components and Flow

The project is broken into 3 broad components:

1. Data ETL Pipeline: (a) Data Scraper; (b) Data Cleanser; (c) Data Pusher
2. Database
3. Data Visualization
<img alt="Program Flow" src="flow.png" width="50%">

#### ETL Pipeline
All ETL Pipeline components are written in Python.

The data scraper makes use of the BeautifulSoup and Selenium libraries and follows [ethical scraping principles](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01).  

The data cleanser utilizes the Pandas library, and Jupyter Notebook was used for data exploration and developing the data cleansing steps.

The Data Pusher uses the Firebase Admin library to delete the previous dataset and write the cleaned data to the database.

#### Database
The Google Cloud Firestore NoSQL database is used as the backend for this project.

#### Data Visualization
The data visualization is a web-based application (HTML/CSS/Javascript) that both fetches the data from the database and then renders it once the data have been fully retrieved.  Used libraries: d3.js, dc.js, crossfilter.js, Bootstrap 4, Bootstrap Material Design.

Description of Data 
-------------------
Category                          |  Description
----------------------------------|------------------------------------------------------------------------------------
Brand                             |  Manufacturer of the instrument.
Price                             |  Price of the instrument in US Dollars.
Country of Origin                 |  Where the instrument was manufactured.
Body - Shape                      |  The shape of the guitar body, with "Single Cutaway" meaning a cutout on the underside of the fretboard in the Fender Telecaster style.  "Double Cutaway" means a cutout both above and below the fretboard like a Fender Stratocaster.  "V" indicates a v-shaped body like the Gibson flying V, and "Z" indicates a z-type body like that of a Gibson Explorer.
Body - Type                       |  Whether the body is made of solid wood or whether it is semi-hollow, or hollow.
Neck - Joint                      |  The means of attaching the neck to the body.
Neck - Finish                     |  What type of finish is used on the neck, with "Gloss" referring to a thicker, higher sheen, typically through use of polyeurathane or similar.  "Satin" means a thinner, lower sheen finish.  "Oiled" means a simple finish
Fretboard - Material              |  The type of wood or other material used for the fretboard.
Fretboard - Number of Frets       |  How many frets are set in the fretboard.
Pickups - Configuration           |  The types of pickups used and in what positions. Placement is bridge -> neck; H = humbucker, S = single coil. Example: HSS means bridge humbucker, middle single coil, and neck single coil.
Pickups - Active or Passive       |  Whether the signals received from the pickups are boosted by an internal preamp. 







