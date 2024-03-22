# AdSight

AdSight pursues the goal to make the impact of billboard advertising more visible and approachable. To this end, it leverages location data provided by Cisco Spaces, and enhances it with DNS data and information on where the billboards are located. With this information, AdSight can analyze how many people werde looking at the advertisement (by using the location data) and how many of them interacted with the advertisement by visiting the advertiser's website afterwards (using the DNS data).

A dashboard showcasig the use case of Frankfurt Airport can be accessed at [http://adsight.space](http://adsight.space) 🚀 Feel free to visit the webpage, try AdSight and give us feedback!

![grafik](https://github.com/anneborcherding/AdSight/assets/55282902/4bc529c1-cb73-4639-9d35-31a05651c67d)


Background: This application was developed during STARTHack 2024 by obeilerding.

## Content

This repository contains the files created during STARTHack 2024 by the team obeilerding.

### Frontend

The main application represents the dashboard of AdSight which has been implemented using Python and [streamlit.io](https://streamlit.io/). The artificial data that we generated and used for this use case can be found in `data`. If you want to run the dashboard, you can clone the repository, install the pip requirements defined in the `requirements.txt` file and run the app with `streamlit run ./main.py`. If you want to skip this step, you can visit a running instance of the dashboard at [http://adsight.space](http://adsight.space).

### Backend

In addition, we implemented a backend which processes the data provided by Cisco Spaces and feeds it into a Kafka instance. Moreover, it provides the possibiliy to include additional Kafka producers to include more data sources, e.g. by Cisco Brella. In addition, the backend provides code to consume data provided by the Kafka instance to provide it for further processing and visualization. With this, our backend provides a scalable environment for data stream processing that could be extended by additional data streams. 

For the local implementation, we used a Kafka instance that we set up using [Cloudkarafka](https://www.cloudkarafka.com/). To be able to use the backend, you need to provide an API Key for Cisco Spaces and the credentials for a Kafka instance.

## Data Stream Visualization

Moreover, we implemented a two dimensional dynamic visualization of the location data provided by the Cisco Spaces data stream using Matplotlib. 
