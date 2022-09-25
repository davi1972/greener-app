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
  - [Getting started](#getting-started)
  - [Live demo](#live-demo)
  - [Built with](#built-with)
  - [Contributing](#contributing)
  - [Versioning](#versioning)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Short description

Greener is an application made for people who love the earth to meet others like them. Host and join events that bring for the power of community to solve enviromental problem, one event at a time.

### What's the problem?


### How can technology help?

Grener brings the community by providing a platform to host and join events that help save the environment. Greener help recommends these events to users by taking into account the users preferences and the popularity of the event. 

### The idea

Currently, there are multiple community events hosted in multiple platforms, making it hard for interested users to get information and join them. Greener currently uses IBM Watson API and multiple Cloud Functions to scrape facebook events to feed its backend, and we have a recommendation system based on reinforcement learning that will filter these events and recommend a system based on the user preferences.

## Demo video


## The architecture

1. Our scraper process crawls facebook events and gets a list of events that could be related to the environment.
2. Watson NLP API extracts the information from the event descriptions and process them into our Cloudant database.
3. Our Recommendation System that is deployed in IBM Cloud Functions act as the backed of the Greener app.

## Long description

## Project roadmap

The project currently does the following things.

- Scrapes events from facebook events, understand their context and store in the the Cloudant Database.
- Give event recommendations to users based on their past preferences and event popularity
- Allow users to host and create their own events 

## Getting started

In this section you add the instructions to run your project on your local machine for development and testing purposes. You can also add instructions on how to deploy the project in production.

- [sample-react-app](./sample-react-app/)
- [sample-angular-app](./sample-angular-app/)
- [Explore other projects](https://github.com/upkarlidder/ibmhacks)

## Live demo

## Built with

- [IBM Cloudant](https://cloud.ibm.com/catalog?search=cloudant#search_results) - The NoSQL database used
- [IBM Cloud Functions](https://cloud.ibm.com/catalog?search=cloud%20functions#search_results) - The compute platform for handing logic and recommendation System
- [IBM Watson NLP](https://www.ibm.com/hk-en/cloud/watson-natural-language-understanding) 
- [React](http://www.dropwizard.io/1.0.2/docs/) - The web framework used

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

## License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
