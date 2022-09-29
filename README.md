# Greener

## Contents

- [Greener](#Greener)
  - [Contents](#contents)
  - [Short description](#short-description)
    - [What's the problem?](#whats-the-problem)
    - [How can technology help?](#how-can-technology-help)
    - [The idea](#the-idea)
  - [Demo video](#demo-video)
  - [The architecture](#the-architecture)
  - [Long description](#long-description)
  - [Project roadmap](#project-roadmap)
  - [Built with](#built-with)
  - [Contributing](#contributing)
  - [Authors](#authors)
  - [License](#license)

## Short description

Greener is an application made for people who love the earth - to help them meet others like them! Host and join events that bring forth the power of the community to solve environmental problems, one event at a time.

### What's the problem?

Go Green is a motto that is slowly transitioning into a way of life for many people across continents. Everyone is aware of sustainable practices these days and wants to do their bit for the environment. But no social platform is available for existing or aspiring environmentalists. This makes it hard for people to stay motivated to Go Green due to the unavailability of public support.

### How can technology help?

Greener brings the community together by providing a platform to host and join events that help save the environment. Greener helps recommends these events to users by taking into account the users' preferences and the popularity of the events. 

### The idea

Currently, there are multiple community events hosted in multiple platforms, making it hard for interested users to get information and join them. Greener currently uses IBM Watson API and multiple Cloud Functions to scrape facebook events to feed its backend, and we have a recommendation system based on reinforcement learning that will filter these events and recommend a system based on the user preferences.

## Demo video

https://youtu.be/a9vU6QQGIlI

## The architecture

1. Our scraper process crawls Facebook events and gets a list of events related to volunteering.
2. Watson NLU API categorizes the information from the event descriptions, which we tag the events with and then process into our Cloudant database.
3. Our Recommendation System that is deployed in IBM Cloud Functions acts as the backend of the Greener app.
4. Our frontend is deployed on IBM Cloud Object Storage (COS).

## Long description

According to a new study by the University of Gothenburg, most people are convinced they’re more eco-friendly than their friends and neighbours. This stems from the belief that “only I am doing my bit” to care for the environment. But all these do-good-ers need a platform that connects them to other people practicing environmentally friendly habits. We want the majority to know that Greener is where you realise the eco-friendly population is much larger than you think. 
The Greener UI is based on web technology and it's multi-platform supported. The app can not only be easily packaged as an iOS or Android application for mobiles, but can also be deployed as a website. Users are able to access it via all platforms with all screen sizes. Greener Ul adapts its layout reactively according to the user's device, providing a consistent and enjoyable user experience.
We use customized algorithms - an event scraping tool in Python, IBM NLU classification, and a recommendation system based on reinforcement learning - that help suggest the list of events to people based on their preferences, what sustainable level they consider themselves at, location, and peer circle’s interests. It all comes together with the help of IBM Cloud Functions by leveraging the different actions, triggers and APIs. The events can come from NGO websites, Facebook, Twitter, or the users themselves, who may organize their own green events to boost engagement and promote eco-friendly habits. The organizations we look to partner with may also provide minor incentives for attending events, which are endorsements of eco-friendly organizations that give these businesses visibility and a potential customer pool.
We want to promote Greener as a platform because saving our earth is a collective task that becomes fun and efficient when done together!

## Project roadmap

The project currently does the following things:

- Scrapes events from facebook events, understand their context and store in the the Cloudant Database.
- Give event recommendations to users based on their past preferences and event popularity.
- Allow users to host and create their own events.

![11c039fe23e1a23c5a569680](https://user-images.githubusercontent.com/43481505/192821624-af90f650-3e68-4f68-8631-ef3d7a864951.jpg)

## Built with

- [IBM Cloudant](https://cloud.ibm.com/catalog/services/cloudant) - The NoSQL database used
- [IBM Cloud Functions](https://cloud.ibm.com/functions) - The compute platform for handing logic and recommendation system
- [IBM Watson NLU](https://cloud.ibm.com/catalog/services/natural-language-understanding) - The service used for classifying events
- [Vue]([http://www.dropwizard.io/1.0.2/docs/](https://vuejs.org/)) - The web framework used

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- Kaistha, Tushar
- Khanna, Pareen
- Sun, David
- Wei, Xiaomiao

## License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.
